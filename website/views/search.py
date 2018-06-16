from base import *

# search page for podcasts
class Search(TemplateView):
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
        search = api.endpoints.search(query, headers)

        # parse search results to json
        try:
            content = json.loads(search)
        except Exception as e:
            content = []

        variables = ({
            "query": query,
            "results": content
        })

        return render(request, 'search.html', context=variables)
