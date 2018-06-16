from base import *

import re # regex for getting parts of url

# to get the name of the podcast being requested
namePattern = re.compile("\/podcast\/([^\/]+)$")

def readURL(url):
    match = namePattern.findall(url)
    if match != None and len(match) == 1:
        return match[0]
    else:
        return None

# search page for podcasts
class Podcast(TemplateView):
    def get(self, request, **kwargs):
        url = request.build_absolute_uri('?')
        podcastName = readURL(url)
        variables = ({
            "test": podcastName 
        })
        return render(request, 'podcast.html', context=variables)
