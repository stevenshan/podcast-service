from base import *

# view for login screen - /login
class Login(TemplateView):
    # return login page if GET request
    def get(self, request, **kwargs):
        return render(request, 'user/login.html', context={"env": "login"})

    # authenticate user if POST request
    def post(self, request, **kwargs):
        variables = ({
            "env": "login",
            "error": True
        })
        return render(request, 'user/login.html', context=variables)

class Register(TemplateView):
    # return login page if GET request
    def get(self, request, **kwargs):
        return render(request, 'user/register.html', context={"env": "register"})
