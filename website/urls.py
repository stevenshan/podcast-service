from django.conf.urls import url
from website import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'user/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, \
            {'template_name': 'user/logout.html', 'next_page': '/login'}, \
            name='logout'),
    url(r'^dashboard/$', views.Dashboard.as_view()),
    url(r'^search/$', views.Search.as_view()), # search
    url(r'^podcast/[^/]*$', views.Podcast.as_view()), # podcast information
    url(r'^$', views.HomePage.as_view()),
]
