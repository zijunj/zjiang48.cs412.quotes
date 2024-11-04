# File: mini_fb/views.py
# Author: Zi Jun Jiang (zjiang48@bu.edu), 10/2/2024
# Description: Controller part of MVC as this file creates 
# functions/classes to connect urls to the correct templates
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from typing import Any


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, \
                                 View
from django.contrib.auth.mixins import LoginRequiredMixin ## forces certain views to require a  
                                                           # logged-in user 
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
    
    def get_login_url(self) -> str:
        ''' return the URL required for login '''
        return reverse('login')
    
    def form_valid(self, form):
        '''This method is called as part of the form processing.'''

        # find the user who is logged in
        user = self.request.user
        # attach that user as a FK to the new Article instance
        form.instance.user = user
        # let the superclass do the real work
        return super().form_valid(form)
    
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''
    A view to create a Status Message for a specific Profile.
    on GET: send back the form to display
    on POST: read/process the form, and save new Status Message to the database
    '''
    
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"
    
    def dispatch(self, *args, **kwargs):
        '''implement this method to add some debug tracing'''
        profile = get_object_or_404(Profile, user=self.request.user)
        print(f"CreateStatusMessage.dispatch; self.request.user={self.request.user}")
        print(f"Profile is: {profile.pk}")
        # let the superclass version of this method do its work:
        return super().dispatch(*args, **kwargs)\
            
    def get_object(self):
        '''Find the object for the corresponding profile'''
        
        # find the user who is logged in
        user = self.request.user
        
        # Find the profile that attached to the corresponding user    
        profile = Profile.objects.get(user = user)
        
        return get_object_or_404(Profile, user=user)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        # get the context data from the superclass
        context =  super().get_context_data(**kwargs)
        
        # find the user who is logged in
        user = self.request.user
        

        # find the Profile identified by the PK from the URL pattern
        profile = get_object_or_404(Profile, user=user)
        
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
        
        # saves the status message to database
        sm = form.save() 
        
        # read the file from the form
        files = self.request.FILES.getlist('files')
        
        # creating an Image object for each file
        for file in files:
            image = Image()  
            image.image = file  
            image.status = sm  
            image.save()  

        # delegate work to superclass version of this method
        return super().form_valid(form)
    
    

        
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    ''' a view to process the UpdateProfile form '''
    model = Profile 
    
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    
    
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    ''' a view to delete a status message '''
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "status_message"

    def get_success_url(self):
        ''' redirect back to the Profile page after successful deletion '''
        return reverse('profile', kwargs={'pk': self.object.profile.id})
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    ''' A view to update a status message '''
    
    model = StatusMessage
    form_class = CreateStatusMessageForm  # Reusing the form for creating/updating
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        ''' redirect back to the Profile page after successful update '''
        return reverse('profile', kwargs={'pk': self.object.profile.id})
    
class CreateFriendView(LoginRequiredMixin, View):
    ''' A view to create a Friend relation between two Profile objects '''

    def dispatch(self, request, *args, **kwargs):
        # Retrieve the Profiles from the URL parameters
        pk = self.kwargs.get('pk')
        other_pk = self.kwargs.get('other_pk')
        
        # Get the profiles based on the primary keys provided
        profile = Profile.objects.get(pk=pk)
        other_profile = Profile.objects.get(pk=other_pk)

        profile.add_friend(other_profile)

        # Redirect back to the profile page of the initiating profile
        return redirect(reverse('profile', kwargs={'pk': pk}))
    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    ''' A view to show all the friend suggestions '''

    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"
    
class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    ''' A view to show the newsfeed for a Profile '''
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"


