# File: mini_fb/views.py
# Author: Zi Jun Jiang (zjiang48@bu.edu), 10/2/2024
# Description: Controller part of MVC as this file creates 
# functions/classes to connect urls to the correct templates
from django.shortcuts import render
from django.urls import reverse
from typing import Any


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
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile' # context variable to use in the template
    
class CreateProfileView(CreateView):
    '''
    A view to create a Profile.
    on GET: send back the form to display
    on POST: read/process the form, and save new Profile to the database
    '''

    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"
    
class CreateStatusMessageView(CreateView):
    '''
    A view to create a Status Message for a specific Profile.
    on GET: send back the form to display
    on POST: read/process the form, and save new Status Message to the database
    '''
    
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        # get the context data from the superclass
        context =  super().get_context_data(**kwargs)

        # find the Profile identified by the PK from the URL pattern
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        
        # add the Profile referred to by the URL into this context
        context['profile'] = profile
        return context
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
       

        # find the Profile identified by the PK from the URL pattern
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return reverse('profile', kwargs={'pk':profile.pk})
        # return reverse('article', kwargs=self.kwargs)

    def form_valid(self, form):
        '''This method is called after the form is validated, 
        before saving data to the database.'''

        # find the Profile identified by the PK from the URL pattern
        profile = Profile.objects.get(pk=self.kwargs['pk'])

        # attach this Profile to the instance of the Status Message to set its FK
        form.instance.profile = profile 

        # delegate work to superclass version of this method
        return super().form_valid(form)
    


