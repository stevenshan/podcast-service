from base import *

# get directory path from url
def readURL(url):
    matches = api.podcastPatWhole.findall(url)
    if matches == None or len(matches) != 1:
        return None

    match = api.podcastPatBreak.findall(matches[0])
    if len(match) != 0:
        return match
    return None

#
# Custom error to return a redirect
#

class Redirect(Exception):
    def __init__(self, redirectObj):
        super(Exception, self).__init__("")

        self.redirect = redirectObj

###########################################################
# Views
# Episode: show details for specific episode
#     |- Episodes: show summary level list of all episodes 
#         |- Podcast: show first 5 episodes and podcast summary
###########################################################

class Episode(TemplateView):
    template = "episode.html"

    # get podcast data from gpodder endpoint and then go
    # to feed of podcast and retrieve episodes list
    def retrieveData(self, request):

        headers = api.genHeader(request)

        # get name of podcast being requested 
        url = request.build_absolute_uri('?')
        urlParts = readURL(url)
        podcastName = urlParts[0]

        # get url of podcast
        url = api.nameMap.lookup(podcastName)

        # if can't find url of podcast using dictionary
        if url == None:
            # try reverse lookup on gpodder
            url = api.nameMap.reverseLookup(podcastName, headers)

        if url == None:
            return redirect("/search?q=" + podcastName)

        # make api request to get podcast details
        podcastRequest = api.endpoints.podcast(url, headers)

        # parse podcast details to json
        try:
            content = json.loads(podcastRequest)
        except Exception as e:
            content = []

        # get episode data from rss feed
        episodeData = api.endpoints.feedList(url, headers)
        episodeCount = len(episodeData)

        try:
            # filter out the episodes that shouldn't be displayed
            episodes = self.episodeFilter(episodeData, urlParts)
        except:
            raise Redirect(redirect("/podcast/" + urlParts[0]))

        variables = ({
            "podcast": content,
            "episodeCount": episodeCount,
            "episodes": episodes,
            "podcastName": podcastName
        })

        return variables

    # decides which episodes to return
    # by default return all of them for full episode list
    def episodeFilter(self, episodes, urlParts):
        # don't need to handle error, will be handled above
        reqEpisode = int(urlParts[2])
        if 0 <= reqEpisode - 1 < len(episodes):
            return [episodes[reqEpisode - 1]]
        raise Exception("redirect")

    # return page after making request for podcast details 
    # and list of episodes from api and rss feed
    def get(self, request, **kwargs):
        try:
            variables = self.retrieveData(request)
            variables["auth"] = api.packAuth(request)
        except Redirect as redirectObj:
            return redirectObj.redirect
        return render(request, self.template, context=variables)

# full episode list page
class Episodes(Episode):
    template = "episodes.html"

    # return all episodes to display full list of episodes
    def episodeFilter(self, episodes, urlParts):
        return episodes

# podcast details page - only shows first 5 episodes
class Podcast(Episodes):
    template = "podcast.html"

    # override to only return first 5 to avoid clutter
    def episodeFilter(self, episodes, urlParts):
        return episodes[:5]
