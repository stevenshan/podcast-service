from base import *

# access devices api endpoint
def getDevices(request):
    result = []
    try:
        header = api.genHeader(request)
        username = request.session["username"]
        sessionid = request.session["sessionid"]

        # request list of devices
        response = api.endpoints.devices(username, sessionid, header)

        # try to parse api response to json
        result = json.loads(response)
    except:
        pass
    return result

class Devices(TemplateView):
    template = "user/devices.html"

    # render page showing options for devices to choose
    def get(self, request, **kwargs):
        loggedIn = api.endpoints.loggedIn(request)

        # must be logged in to view devices
        if not loggedIn:
            return redirect("/login")

        devices = getDevices(request)

        auth = api.packAuth(request)

        # make sure device is in valid range
        if (auth["device"] < 0 or auth["device"] >= len(devices)):
            auth["device"] = 0
            try:
                request.session["device"] = 0
            except:
                pass

        variables = ({
            "auth": auth,
            "env": "none",
            "devices": devices
        })

        return render(request, self.template, context=variables)

    # receive post request to change active device
    def post(self, request, **kwargs):

        headers = api.genHeader(request)

        device = request.POST.get("device", 0)

        loggedIn = api.endpoints.loggedIn(request)

        # must be logged in to change active device
        if not loggedIn:
            return redirect("/login")

        try:
            request.session["device"] = int(device) 
        except:
            pass

        return redirect("/dashboard")