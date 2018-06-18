from base import *

# import function to get list of subscriptions
from dashboard import getSubs

# home page showing top group of podcasts
class Suggestions(TemplateView):
    def get(self, request, **kwargs):

        auth = api.packAuth(request)

        if not auth["loggedIn"]:
            return redirect("/login")

        headers = api.genHeader(request)

        # get suggested podcasts
        podcastsRequest = api.endpoints.suggestions(auth["sessionid"], headers)

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

        # get subscriptions
        subscriptions = getSubs(auth, headers)

        # get aggregated text from all subscriptions
        text = ""
        for subscription in subscriptions:
            try:
                text += (subscription["title"] + " " + 
                        subscription["description"] + " ")
            except:
                pass

        phrases = api.keywords(text)

        variables = ({
            "results": content,
            "auth": auth,
            "phrases": phrases
        })

        return render(request, 'suggestions.html', context=variables)

