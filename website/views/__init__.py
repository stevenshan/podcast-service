# central module for controlling views of website
# code for views are in separate files

###########################################################
# Views
###########################################################

# index page - /
from .homepage import HomePage

# search page - /search
from .search import Search, Tags

# Podcast - show details for podcast - /podcast
# Episodes - show full list of podcast episodes - /podcast/*/episodes
# Episode - show details of specific episode
from .podcast import Podcast, Episodes, Episode

# Login screen - /login
from .user_auth import Login, Register, Logout

# Devices list screen - /devices
from .devices import Devices

# Dashboard screen - /dashboard
from .dashboard import Dashboard

# Subscription actions
from .subscription import Subscribe, Unsubscribe

# Suggestions endpoint
from .suggestions import Suggestions

