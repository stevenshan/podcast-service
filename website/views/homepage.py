from base import *

class HomePage(TemplateView):
    def get(self, request, **kwargs):
        variables = ({
            "auth": api.packAuth(request)
        })
        return render(request, 'template.html', context=variables)
