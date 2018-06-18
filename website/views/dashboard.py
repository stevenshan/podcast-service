from base import *

# view for user dashboard page - /dashboard
class Dashboard(TemplateView):
    def get(self, request, **kwargs):
        loggedin = api.endpoints.loggedIn(request)
        variables = ({
            "auth": api.packAuth(request)     
        })
        return render(request, 'dashboard.html', context=variables)
