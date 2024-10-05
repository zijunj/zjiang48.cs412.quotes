# File: mini_fb/views.py
# Author: Zi Jun Jiang (zjiang48@bu.edu), 10/2/2024
# Description: Controller part of MVC as this file creates 
# functions to connect urls to the correct templates
from django.shortcuts import render

from django.views.generic import ListView
from .models import * ## import the models (e.g., Profile)

# Create your views here.

class ShowAllProfilesView(ListView):
    '''the view to show all Profiles'''

    model = Profile # the model to display
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # context variable to use in the template
    
