from .base import *

# home page showing top group of podcasts
class HomePage(TemplateView):
    def get(self, request, **kwargs):

        headers = api.genHeader(request)

        # make api request for top podcasts 
        podcastsRequest = api.endpoints.topPodcasts(headers)

        # parse search results to json
        try:
            content = json.loads(podcastsRequest)
        except Exception as e:
            content = []

        # retrieve podcast names
        for podcast in content:
            try:
                name = api.nameMap.checkout(
                    podcast["mygpo_link"],
                    podcast["url"]
                )
            except:
                name = ""
            podcast["idName"] = name

        # get top genres
        try:
            genresRaw = api.endpoints.getGenres(headers)
            genreList = json.loads(genresRaw)
        except:
            genreList = []

        variables = ({
            "results": content,
            "topSearches": api.searches.retrieve(),
            "topGenres": genreList,
            "auth": api.packAuth(request)
        })

        return render(request, 'homepage.html', context=variables)

