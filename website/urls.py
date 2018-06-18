from django.conf.urls import url
from website import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', views.Login.as_view()), # login screen
    url(r'^register/$', views.Register.as_view()), # login screen
    url(r'^logout/$', auth_views.logout, \
            {'template_name': 'user/logout.html', 'next_page': '/login'}, \
            name='logout'),
    url(r'^dashboard/$', views.Dashboard.as_view()),
    url(r'^search/$', views.Search.as_view()), # search
    url(r'^podcast/[^/]*$', views.Podcast.as_view()), # podcast information
    url(r'^podcast/[^/]*/episodes$', views.Episodes.as_view()), # podcast episode list
    url(r'^podcast/[^/]*/episodes/[^/]*$', views.Episode.as_view()), # specific episode
    url(r'^$', views.HomePage.as_view()),
]
