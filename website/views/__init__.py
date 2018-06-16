# central module for controlling views of website

from search import Search
from homepage import HomePage
from podcast import Podcast

# User dashboard as front page for logged in users
from base import *

class Dashboard(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'dashboard.html', context=None)

# initialize PickleDB for mapping podcast names to url
api.nameDB = api.pickledb.load("podcastMapping.db", False)
