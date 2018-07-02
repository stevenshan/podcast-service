from .base import *


###########################################################
# Helper to generate json containing subscription delta
###########################################################

def genJSONDelta(request, key, pattern):
    # get name of podcast being requested 
    url = request.build_absolute_uri('?')
    urlParts = api.readURL(url, pattern)
    podcastName = urlParts[0]

    result = {}
    result[key] = [api.nameMap.lookup(podcastName)]

    return result, podcastName

class Subscribe(TemplateView):
    def get(self, request, **kwargs):
        try:
            jsonDelta, podcastName = \
                genJSONDelta(request, "add", api.subscribePatWhole)
            auth = api.packAuth(request)
            headers = api.genHeader(request)
            api.endpoints.subscriptionChange(
                auth["username"], auth["sessionid"],
                auth["device"], headers, jsonDelta)
        except:
            pass
        return redirect("/podcast/" + podcastName)

class Unsubscribe(TemplateView):
    def get(self, request, **kwargs):
        try:
            jsonDelta, podcastName = \
                genJSONDelta(request, "remove", api.unsubscribePatWhole)
            auth = api.packAuth(request)
            headers = api.genHeader(request)
            api.endpoints.subscriptionChange(
                auth["username"], auth["sessionid"],
                auth["device"], headers, jsonDelta)
        except:
            pass
        return redirect("/podcast/" + podcastName)
