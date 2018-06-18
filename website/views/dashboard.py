from base import *

# view for user dashboard page - /dashboard
class Dashboard(TemplateView):
    def get(self, request, **kwargs):
        loggedIn = api.endpoints.loggedIn(request)

        if not loggedIn:
            return redirect("/login")

        auth = api.packAuth(request)
        headers = api.genHeader(request)

        # make api request for subscriptions
        subsRequest = api.endpoints.subscriptions(
                auth["username"], auth["sessionid"], 
                auth["device"], headers)

        # parse search results to json
        try:
            content = json.loads(subsRequest)
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
            "results": content,
            "auth": auth
        })

        return render(request, 'dashboard.html', context=variables)

