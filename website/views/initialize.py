###########################################################
# Fields 
###########################################################

# gets set by __init__.py to actual database
nameDB = None # to map podcast name to url
searchDB = None # to keep track of all searches
searchDBTop = None # to keep track of top searches
badWords = None # list of bad words for filtering

###########################################################
# Initialization - stuff to do when server starts
###########################################################

# import base for views in order to do initialization
from base import *
import redis
from base64 import b64decode
import re
import json

# initialize DB connection for mapping podcast names to url
nameDB = redis.StrictRedis(host="localhost", port=6379, db=0)

# initialize DB connection for keeping track of searches
searchDB = redis.StrictRedis(host="localhost", port=6379, db=1)
searchDBTop = redis.StrictRedis(host="localhost", port=6379, db=2)

# get list of bad words
try:
    # decode bad words file
    badWordsFile = b64decode(open('lib/bad_words.txt', 'r').read())
    # split file by lines
    badWordsFile = [x for x in badWordsFile.split("\n") if x != ""]

    # process file
    badWords = set(line.strip('\n') for line in badWordsFile)
    badWords = '(%s)' %'|'.join(badWords)
    badWords = re.compile(badWords, re.IGNORECASE)
except:
    pass

###########################################################
# Database methods - maps podcast name to url
###########################################################

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

# interface to serve as wrapper for searchDB 
class searches:
    # get item from redis database as json
    @staticmethod
    def getJSON(x):
        return json.loads(searchDBTop.get(x))

    @staticmethod
    def filter(query):
        filtered = badWords.sub("", query)
        # if word filtered out inappropriate
        return filtered.strip(" ") != query

    # get mapping for podcast name
    @staticmethod
    def add(query):
        # make sure query is appropriate to be saved
        if searches.filter(query):
            return

        query = query[:25] # limit length of query

        # helper method for interacting with database
        getInt = lambda x: int(searchDB.get(x))
        increment = lambda x: searchDB.set(x, getInt(x) + 1)

        # retrieve stuff from database
        libKeys = searchDB.keys()

        top = [searches.getJSON(x) for x in searchDBTop.keys()]

        query = query.lower()
        if query in libKeys:
            increment(query)
        else:
            searchDB.set(query, 1)
        queryVal = getInt(query)

        # recount top searches
        top.sort(key=(lambda x: x[0]))
        keys = [x[1] for x in top]

        if query not in keys:
            if len(top) < 20:
                top.append([queryVal, query])
            elif top[0][0] < queryVal:
                top[0] = [queryVal, query]
        else:
            i = keys.index(query) 
            if i != -1:
                top[i] = [queryVal, query]

        # update database
        for i in range(len(top)):
            searchDBTop.set(i, json.dumps(top[i]))

    # retrieve top 20 mappings
    @staticmethod
    def retrieve():
        top = [searches.getJSON(x) for x in searchDBTop.keys()]
        print(top)
        top.sort(key=(lambda x: x[0]), reverse=True)
        return [x[1] for x in top]
