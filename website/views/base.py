# file that includes most imports that any view will need
# use "from base import *" when creating a new view

# standard imports for creating django views
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

# Django user authentication
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

import requests # to make http request to api

# contains settings for api connection and methods for endpoints
import api

import json # parse api response

