from base import *

class UserView(TemplateView):
    template = "template.html"
    env = "login"

    def get(self, request, **kwargs):
        loggedIn = api.endpoints.loggedIn(request)

        # if already logged in then redirect to dashboard
        if loggedIn:
            return redirect("/dashboard")

        return render(request, self.template, context={"env": self.env})

# view for login screen - /login
class Login(UserView):
    template = "user/login.html"
    env = "login"

    # authenticate user if POST request
    def post(self, request, **kwargs):

        # get user-agent
        userAgent = request.META['HTTP_USER_AGENT']

        headers = ({
            "User-Agent": userAgent
        })

        # try todele authenticate using API
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        response = api.endpoints.login(username, password, headers)

        try:
            if response.status_code == 200:
                sessionid = response.cookies["sessionid"]
                request.session["sessionid"] = sessionid
                request.session["username"] = username 

                # redirect to user dashboard if success
                return redirect("/dashboard")            
        except:
            pass

        variables = ({
            "env": "login",
            "error": True
        })
        return render(request, 'user/login.html', context=variables)

# view for register screen - /register
class Register(UserView):
    template = "user/register.html"
    env = "register"

# view for logout screen - /logout
class UserView(TemplateView):
    def get(self, request, **kwargs):
        # delete user session variables
        try:
            del request.session["sessionid"]  
        except:
            pass

        try:
            del request.session["username"]  
        except:
            pass

        # redirect to home page
        return redirect("/login")
