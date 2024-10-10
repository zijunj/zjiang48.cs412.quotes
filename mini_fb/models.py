# File: mini_fb/models.py
# Author: Zi Jun Jiang (zjiang48@bu.edu), 10/2/2024
# Description: Model part of the MVC. This file allows admin
# to input data attributes for the Profile of each user.

from django.db import models
from django.shortcuts import render
from django.urls import reverse
from typing import Any


# Create your models here.
class Profile(models.Model):
    '''Models the data attributes of individual Facebook users.'''
    
    # data attributes of an Facebook Profile:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    image_url = models.URLField(blank=True)
    
    def __str__(self):
        '''Return a string representation of this object.'''
        
        return f'{self.first_name} {self.last_name}\'s Profile'

        
    def get_status_messages(self):
        '''Get the status messages for each profile'''

        # retrieve all of the StatusMessage for the correct Profile and sort by newest first
        status_messages = StatusMessage.objects.filter(profile=self).order_by('-timestamp')
        
        return status_messages

    def get_absolute_url(self):
        # profile = Profile.objects.get(pk=self.kwargs['pk'])
        profile = Profile.objects.get(pk=self.pk)
        return reverse('profile', kwargs={'pk':profile.pk})
        
        # return reverse('profile', kwargs=self.kwargs)
    
class StatusMessage(models.Model):
    '''Models the data attributes of individual Facebook users.'''
    
    # data attributes of an Facebook Profile:
    timestamp = models.DateField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    
    def __str__(self):
        '''Return a string representation of this object.'''

        return f'{self.profile}: {self.message}'