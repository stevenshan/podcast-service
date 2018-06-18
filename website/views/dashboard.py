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
            podcast["freq"] = 0

            # get frequency of episodes in terms of episodes/day
            try:
                episodes = api.endpoints.feedList(podcast["url"], headers)
                convert = lambda x: int(x.strftime("%s"))

                deltas = []
                for i in range(len(episodes) - 1):

                    deltas.append(abs(convert(episodes[i]["timestamp"]) - 
                        convert(episodes[i + 1]["timestamp"])))

                avg = (3600 * 24) / (float(sum(deltas)) / len(deltas))
                avg = round(avg, 1)
                podcast["freq"] = avg
            except:
                pass

        variables = ({
            "results": content,
            "auth": auth
        })

        return render(request, 'dashboard.html', context=variables)

