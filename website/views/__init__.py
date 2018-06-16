# central module for controlling views of website
# code for views are in separate files

# index page - /
from homepage import HomePage

# search page - /search
from search import Search

# show details for podcast - /podcast
from podcast import Podcast

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
