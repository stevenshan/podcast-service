# central module for controlling views of website
# code for views are in separate files

###########################################################
# Views
###########################################################

# index page - /
from homepage import HomePage

# search page - /search
from search import Search, Tags

# Podcast - show details for podcast - /podcast
# Episodes - show full list of podcast episodes - /podcast/*/episodes
# Episode - show details of specific episode
from podcast import Podcast, Episodes, Episode

# Login screen - /login
from user_auth import Login, Register, Logout

# Devices list screen - /devices
from devices import Devices

# Dashboard screen - /dashboard
from dashboard import Dashboard

# Subscription actions
from subscription import Subscribe, Unsubscribe

# Suggestions endpoint
from suggestions import Suggestions

###########################################################
# Initialization - stuff to do when server starts
###########################################################

# import base for views in order to do initialization
from base import *
import redis

# initialize PickleDB for mapping podcast names to url
api.nameDB = redis.StrictRedis(host="localhost", port=6379, db=0)

# initialize DB for keeping track of searches
try:
    api.searchDB = json.load(open("database/searches.json"))

except Exception as e:
    api.searchDB = {"top": [], "lib": {}, "count": 0} 
