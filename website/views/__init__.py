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
from user_auth import Login, Register

# User dashboard as front page for logged in users
from base import *

class Dashboard(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'dashboard.html', context=None)

###########################################################
# Initialization - stuff to do when server starts
###########################################################

# initialize PickleDB for mapping podcast names to url
api.nameDB = api.pickledb.load("database/podcastMapping.db", False)
