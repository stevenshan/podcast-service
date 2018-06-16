from base import *

class HomePage(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'template.html', context=None)
