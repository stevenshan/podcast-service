# contains information for connecting to gPodder API

import requests # for making requests to api endpoints

# used for database mapping podcast name to url
import pickledb

import re # regular expressions

# regex pattern to get name of podcast from url
podcastPat = re.compile("\/podcast\/([^\/]+)$")

###########################################################
# Methods for interacting with gPodder API
###########################################################

HOST = "https://gpodder.net"

# backups for testing without internet
class OfflineEndpoints:
    @staticmethod
    def search(query, headers):
        if query == "empty" or query == "none":
            return ""
        file = open("website/views/search-example.json").read()
        return file

# actual methods for connecting to api endpoints
class OnlineEndpoints(OfflineEndpoints):
    @staticmethod
    def search(query, headers):
        request = requests.get(
            HOST + "/search.json",
            params={"q": query},
            headers=headers
        )

        if request.status_code == 200:
            return request.content
        else:
            return None

# change between OfflineEndpoints and OnlineEndpoints
endpoints = OfflineEndpoints 

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

# simple interface to serve as wrapper for nameDB
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
        