# File: mini_fb/views.py
# Author: Zi Jun Jiang (zjiang48@bu.edu), 10/2/2024
# Description: Controller part of MVC as this file creates 
# functions/classes to connect urls to the correct templates
from django.shortcuts import render
from django.urls import reverse


from django.views.generic import ListView, DetailView, CreateView
from .models import * ## import the models (e.g., Profile)
from .forms import * ## import the forms (e.g., CreateProfileForm)

# Create your views here.

class ShowAllProfilesView(ListView):
    '''the view to show all Profiles'''

    model = Profile # the model to display
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # context variable to use in the template
    
class ShowProfilePageView(DetailView):
    '''the view to show one Profile'''

    model = Profile # the model to display
    template_name = 'mini_fb/show_profile_page.html'
    context_object_name = 'profile' # context variable to use in the template
    
class CreateProfileView(CreateView):
    '''
    A view to create a Comment on an Article.
    on GET: send back the form to display
    on POST: read/process the form, and save new Comment to the database
    '''

    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"
    
    


