# contains information for connecting to gPodder API

from dateutil.parser import parse as parseDate # convert date string to object
from datetime import datetime
import requests # for making requests to api endpoints

# used for database mapping podcast name to url
import pickledb

import re # regular expressions
from lxml import etree # XML parsing for episode feed

# regex pattern to get name of podcast from url
podcastPat = re.compile("\/podcast\/([^\/]+)$") # matches exactly one level after podcast
podcastPatWhole = re.compile("\/podcast\/(.+)") # get everything after podcast
podcastPatBreak = re.compile("[^\/]+") # split by delimeter /

# regex pattern to get podcast feed url from gpodder html code
gPodderReverse = re.compile("<a href=\"([^\"]+)\" title=\"Feed\">")

###########################################################
# General Helpers
###########################################################

# sends get request with exception handling in case bad connection
def safeRequest(url, params = {}, headers = {}, cookies = {}):
    try:
        return requests.get(url, params=params, headers=headers, cookies=cookies) 
    except Exception as e:
        return None

def safePOST(url, auth = (), headers = {}, cookies = {}):
    try:
        return requests.post(url, auth=auth, headers=headers, cookies=cookies)
    except:
        return None;

def toDate(dateString):
    try:
        return parseDate(dateString)
    except:
        # return epoch on failure
        return datetime.fromtimestamp(0)

# converts XML feed from podcast url to list of episodes
def parseFeedXML(xml):
    result = []
    try:
        tree = etree.fromstring(xml)

        # all episodes are in "item" tag
        # url of each episode is in "enclosure" tag inside 
        # the url attribute

        # find all urls in XML
        items = tree.iter(tag="item")
        for episode in items:
            enclosures = episode.findall("enclosure")
            pubDate = episode.findall("pubDate")
            title = episode.findall("title")
            description = (episode.findall("description") +
                    episode.findall("itunes:summary", tree.nsmap))
            if (
                    len(enclosures) == 1 and 
                    len(pubDate) == 1 and
                    len(title) == 1 and
                    len(description) >= 1 and
                    "url" in enclosures[0].attrib
            ):
                date = toDate(pubDate[0].text)
                episodeDict = ({
                    "url": enclosures[0].attrib["url"], 
                    "title": title[0].text,
                    "description": description[0].text,
                    "released": date.strftime("%b %d, %Y"),
                    "timestamp": date
                })
                result.append(episodeDict)
    except:
        pass

    # sort urls by publication date
    key = lambda x: x["timestamp"] # get publication date from tuple
    result.sort(key=key,reverse=True)

    # enumerate episodes
    counter = 0
    for episode in result:
        episode["enumeration"] = len(result) - counter
        counter += 1

    return result

###########################################################
# Methods for interacting with gPodder API
###########################################################

# uri host for api
HOST = "https://gpodder.net"

# backups for testing without internet
class OfflineEndpoints:
    # Podcast Search Directory API
    @staticmethod
    def search(query, headers):
        if query == "empty" or query == "none":
            return ""
        file = open("website/views/examples/search-example.json").read()
        return file

    # Retrieve Podcast Data Directory API    
    @staticmethod
    def podcast(url, headers):
        file = open("website/views/examples/podcast-data-example.json").read()
        return file

    # Gets list of Episode URLs from podcast url
    @staticmethod
    def feedList(url, headers):
        file = open("website/views/examples/feed-xml-example.xml").read()
        return parseFeedXML(file)

    # Retrieve Episode Data Directory API
    @staticmethod 
    def episode(url, episode_url, headers):
        file = open("website/views/examples/episode-data-example.json").read()
        return file


# actual methods for connecting to api endpoints
class OnlineEndpoints(OfflineEndpoints):
    # shared method for getting content with http request
    @staticmethod
    def processRequest(request):
        if request == None or request.status_code != 200:
            return None
        else:
            return request.content 

    # Login Authentication API - returns request response
    @staticmethod
    def login(username, password, headers):
        request = safePOST(
            HOST + "/api/2/auth/" + username + "/login.json",
            auth=(username, password),
            headers=headers
        )
        return request

    # check if user is logged in
    @staticmethod
    def loggedIn(request):
        try:
            # get credentials from session
            username = request.session["username"]
            sessionid = request.session["sessionid"]
            userAgent = request.META["HTTP_USER_AGENT"]

            headers = ({
                "User-Agent": userAgent     
            })

            request = safePOST(
                HOST + "/api/2/auth/" + username + "/login.json",
                cookies={"sessionid": sessionid},
                headers=headers
            )

            return request.status_code == 200
        except:
            return False

    # send logout request to api
    @staticmethod
    def logout(username, sessionid, headers):
        request = safePOST(
            HOST + "/api/2/auth/" + username + "/logout.json",
            cookies={"sessionid": sessionid},
            headers=headers
        )

    # Podcast Search Directory API
    @staticmethod
    def search(query, headers):
        request = safeRequest(
            HOST + "/search.json",
            params={"q": query},
            headers=headers
        )
        return OnlineEndpoints.processRequest(request)

    # Retrieve Podcast Data Directory API    
    @staticmethod
    def podcast(url, headers):
        request = safeRequest(
            HOST + "/api/2/data/podcast.json",
            params={"url": url},
            headers=headers
        )
        return OnlineEndpoints.processRequest(request)

    # Gets list of Episode URLs from podcast url
    @staticmethod
    def feedList(url, headers):
        request = requests.get(url, headers=headers)
        return parseFeedXML(OnlineEndpoints.processRequest(request))

    # Retrieve Episode Data Directory API
    @staticmethod
    def episode(url, episode_url, headers):
        request = safeRequest(
            HOST + "/api/2/data/episode.json",
            params={"podcast": url, "url": episode_url},
            headers=headers
        )
        return OnlineEndpoints.processRequest(request)

    # Retrieve devices from List Devices API
    @staticmethod
    def devices(username, sessionid, headers):
        request = safeRequest(
            HOST + "/api/2/devices/" + username + ".json",
            cookies={"sessionid": sessionid},
            headers=headers
        )
        return OnlineEndpoints.processRequest(request)


# change between OnlineEndpoints and OfflineEndpoints for testing
# endpoints = OfflineEndpoints 
endpoints = OnlineEndpoints

###########################################################
# Shared Methods 
###########################################################

# get authentication information to send to template for render
def packAuth(request):
    package = ({
        "loggedIn": False,
        "username": ""
    })

    package["loggedIn"] = endpoints.loggedIn(request)
    if package["loggedIn"]:
        try:
            package["username"] = request.session["username"]
            package["device"] = request.session["device"]
        except Exception as e:
            pass

    return package

# returns generic header
def genHeader(request):
    header = {}
    try:
        # get user-agent
        userAgent = request.META['HTTP_USER_AGENT']
        header["User-Agent"] = userAgent
    except:
        pass
    return header

###########################################################
# Database methods - maps podcast name to url
###########################################################

# dummy pickledb database fallback
class DummyDB:
    def set(this, key, value):
        return True

    def get(this, key):
        return None

    def dump(this):
        pass

# gets set by __init__.py to actual database
nameDB = DummyDB()

# interface to serve as wrapper for nameDB
class nameMap:
    # retrieve name given mygpo_link
    @staticmethod
    def getNameFromGPodderURL(url):
        name = podcastPat.findall(url)
        try:
            return name[0]
        except:
            return None

    # get mapping for podcast name
    @staticmethod
    def lookup(name):
        request = nameDB.get(name)
        return request

    # add a new mapping
    @staticmethod
    def add(gPodderName, url):
        nameDB.set(gPodderName, url)
        nameDB.dump()

    # check if a mapping already exists and adds it if it doesn't
    # returns gPodderName
    # combines getNameFromGPodderURL with add
    @staticmethod
    def checkout(gPodderURL, url):
        gPodderName = nameMap.getNameFromGPodderURL(gPodderURL)
        if gPodderName != None and nameMap.lookup(gPodderName) == None:
            nameMap.add(gPodderName, url)
        return gPodderName
        
    # go to gPodder website to try to get podcast feed url
    @staticmethod
    def reverseLookup(gPodderName, headers):
        gPodderURL = HOST + "/podcast/" + gPodderName
        request = safeRequest(gPodderURL, headers=headers)
        content = OnlineEndpoints.processRequest(request)

        if content == None:
            return None

        matches = gPodderReverse.findall(content)

        if len(matches) != 1:
            return None
        else:
            match = matches[0]

        if endpoints.podcast(match, headers) != None:
            nameMap.checkout(gPodderURL, match)
            return match

        return None


