# central module for controlling views of website
# code for views are in separate files

# index page - /
from homepage import HomePage

# search page - /search
from search import Search

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

from subscription import Subscribe, Unsubscribe

# import base for views in order to do initialization
from base import *

###########################################################
# Initialization - stuff to do when server starts
###########################################################

# initialize PickleDB for mapping podcast names to url
api.nameDB = api.pickledb.load("database/podcastMapping.db", False)
