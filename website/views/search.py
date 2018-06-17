from base import *

# View for search page - /search

# search page for podcasts
class Search(TemplateView):
    # return search page after making query to API
    def get(self, request, **kwargs):

        # anonymous function to simplify syntax of getting GET data
        get = lambda x: request.GET.get(x)

        # get search query
        query = get("q")
        # get user-agent
        userAgent = request.META['HTTP_USER_AGENT']

        # make sure a valid search query was inputed
        if query == None or query.strip(" ") == "":
            return redirect("/")

        headers = ({
            "User-Agent": userAgent
        })

        # make api request for search
        searchRequest = api.endpoints.search(query, headers)

        # parse search results to json
        try:
            content = json.loads(searchRequest)
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

        variables = ({
            "query": query,
            "results": content
        })

        return render(request, 'search.html', context=variables)
