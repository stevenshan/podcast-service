from base import *

def readURL(url):
    matches = api.podcastPatWhole.findall(url)
    if matches == None or len(matches) != 1:
        return None

    match = api.podcastPatBreak.findall(matches[0])
    if len(match) != 0:
        return match
    return None

# View for podcast details page - /podcast

# podcast details page - only shows first 5 episodes
class Episodes(TemplateView):
    def retrieveData(self, request):
        # get user-agent
        userAgent = request.META['HTTP_USER_AGENT']

        headers = ({
            "User-Agent": userAgent
        })

        # get name of podcast being requested 
        url = request.build_absolute_uri('?')
        podcastName = readURL(url)[0]

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

        # get urls of episodes so we can get episode details
        episodeURLs = api.endpoints.feedList(url, headers)
        episodeCount = len(episodeURLs)

        firstGroup = episodeURLs[:5]

        variables = ({
            "podcast": content,
            "episodeCount": episodeCount,
            "episodes": firstGroup,
            "podcastName": podcastName
        })

        return variables

    # return page after making request for podcast details from API
    def get(self, request, **kwargs):
        variables = self.retrieveData(request)
        return render(request, 'podcast.html', context=variables)

# full episode list page
class Podcast(Episodes):
    pass
