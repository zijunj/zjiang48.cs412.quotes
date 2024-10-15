# mini_fb/forms.py

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database'''

    class Meta:
        '''Associate this HTML form with the Profile data model'''
        model = Profile
        fields = ['first_name', 'last_name', 'city','email_address','image_url'] # which fields to include in the form
        
class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a Status Message to a specific profile to the database'''

    class Meta:
        '''Associate this HTML form with the Profile data model'''
        model = StatusMessage
        fields = ['message'] # which fields to include in the form
        
        
        