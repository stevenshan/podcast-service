from base import *

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
    url = ""

    # get podcast data from gpodder endpoint and then go
    # to feed of podcast and retrieve episodes list
    def retrieveData(self, request):

        headers = api.genHeader(request)

        # get name of podcast being requested 
        fullURL = request.build_absolute_uri('?')
        urlParts = api.readURL(fullURL)

        # if invalid url (such as missing podcast name)
        if len(urlParts) == 0:
            return redirect("/")

        podcastName = urlParts[0]

        # get url of podcast
        url = api.nameMap.lookup(podcastName)

        # if can't find url of podcast using dictionary
        if url == None:
            # try reverse lookup on gpodder
            url = api.nameMap.reverseLookup(podcastName, headers)

        if url == None:
            raise Redirect(redirect("/search?q=" + podcastName))

        self.url = url

        # make api request to get podcast details
        podcastRequest = api.endpoints.podcast(url, headers)

        # parse podcast details to json
        try:
            content = json.loads(podcastRequest)
            if content["logo_url"] == None and content["scaled_logo_url"] == None:
                content["logo_url"] = "http://bestsellerexperiment.com/wp-content/uploads/2016/10/itunes-podcast-app-logo-square-220x220.png"
            elif content["logo_url"] == None:
                content["logo_url"] = content["scaled_logo_url"]
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

    # give children classes change to add variables to context
    def context(self, request, variables):
        return variables 

    # return page after making request for podcast details 
    # and list of episodes from api and rss feed
    def get(self, request, **kwargs):
        try:
            variables = self.retrieveData(request)
            variables["auth"] = api.packAuth(request)
            self.context(request, variables)
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

    # add subscribe/unsubscribe to context
    # add keyword extracted tags
    def context(self, request, variables):
        subscribed = False
        try:
            auth = variables["auth"]
            if not auth["loggedIn"]:
                raise Exception("not subscribed")
                
            headers = api.genHeader(request)
            subscriptions = json.loads(api.endpoints.subscriptions(
                auth["username"], auth["sessionid"], 
                auth["device"], headers))
            urls = [x["url"] for x in subscriptions]
            if self.url in urls:
                subscribed = True
        except Exception as e:
            pass
        variables["subscribed"] = subscribed 

        # extract keywords
        text = ""
        try:
            # add podcast data
            text += (variables["podcast"]["title"] + " " +
                variables["podcast"]["description"] + " ")

            # add each episode data
            for episode in variables["episodes"]:
                text += (episode["title"] + " " +
                    episode["description"] + " ")
            variables["keywords"] = api.keywords(text, 1)[:20]
            variables["keywords"].sort(key=lambda x: len(x), reverse=True)
        except:
            pass

    # override to only return first 5 to avoid clutter
    def episodeFilter(self, episodes, urlParts):
        return episodes[:5]
