# File: mini_fb/models.py
# Author: Zi Jun Jiang (zjiang48@bu.edu), 10/2/2024
# Description: Model part of the MVC. This file allows admin
# to input data attributes for the Profile of each user.

from django.db import models
from django.shortcuts import render
from django.urls import reverse
from typing import Any
from django.contrib.auth.models import User 

# Create your models here.
class Profile(models.Model):
    '''Models the data attributes of individual Facebook users.'''
    
    # data attributes of an Facebook Profile:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    image_url = models.URLField(blank=True)
    
    # Every Facebook Profile has one user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        '''Return a string representation of this object.'''
        
        return f'{self.first_name} {self.last_name}\'s Profile'

        
    def get_status_messages(self):
        '''Get the status messages for each profile'''

        # retrieve all of the StatusMessage for the correct Profile and sort by newest first
        status_messages = StatusMessage.objects.filter(profile=self).order_by('-timestamp')
        
        return status_messages

    def get_absolute_url(self):
        '''Return the URL that will display an instance of this object'''
        
        profile = Profile.objects.get(pk=self.pk)
        return reverse('profile', kwargs={'pk':profile.pk})
    
    def get_friends(self):
        # '''Return's a list of friend's profiles'''

        # friend_list = list(Friend.objects.filter(profile1=self) | Friend.objects.filter(profile2=self))
        # return friend_list
        ''' Return all the friends of a Profile object in a list '''
        friends_profile1 = Friend.objects.filter(profile1=self)
        friends_profile2 = Friend.objects.filter(profile2=self)

        friends = []
        # If the current profile is profile1:
        for friend in friends_profile1:
            friends.append(friend.profile2)

         # If the current profile is profile2:
        for friend in friends_profile2:
            friends.append(friend.profile1)

        return friends
    
    def add_friend(self, other):
        ''' A method that takes a parameter other, which refers to another
            Profile and creates a Friend relation for the 2 Profiles '''
        if self == other:
            raise ValueError("A profile cannot friend itself.")
        
        existing_friend = Friend.objects.filter(profile1=self, profile2=other) | \
                            Friend.objects.filter(profile1=other, profile2=self)
        if existing_friend:
            print("Friend relationship already exists.")
        else:
            friend = Friend()
            friend.profile1 = self
            friend.profile2 = other
            friend.save()
            
    def get_friend_suggestions(self):
        ''' Returns a list of possible friends for a Profile '''        
        # Get the friends that already exist
        existing_friends = self.get_friends()
        existing_friends_pks = []
        for friend in existing_friends:
            existing_friends_pks.append(friend.pk)

        suggestions = []
        all_profiles = Profile.objects.all()

        # Exclude the current profile and existing friends from the list of all profiles
        for profile in all_profiles:
            if ((profile != self) and (profile not in existing_friends)):
                suggestions.append(profile)
                
        return suggestions
    
    def get_news_feed(self):
        ''' Creates a news feed: display the status messages and images associated to a 
            Profile and that of their friends '''

        pks = []
        # Add the pk of the profile itself
        pks.append(self.pk)

        friends = self.get_friends()
        # Add the pks of the friends
        for friend in friends:
            pks.append(friend.pk)
        # Filter the statusmessages for everyone associated with the profile
        news_feed = StatusMessage.objects.filter(profile__pk__in=pks).order_by('-timestamp')

        return news_feed
    
    def get_absolute_url(self):
        ''' Return the Profile '''
        return reverse('profile', kwargs={'pk': self.id})

        
    
class StatusMessage(models.Model):
    '''Models the data attributes of individual Facebook users.'''
    
    # data attributes of an Facebook Profile:
    timestamp = models.DateField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    
    def __str__(self):
        '''Return a string representation of this object.'''

        return f'{self.profile}: {self.message}'
    
    def get_images(self):
        '''Get the images for each status message'''
        
        # retrieve all of the images for the correct Profile and sort by newest first
        image = Image.objects.filter(status=self)
        
        return image
    
class Image(models.Model):
    '''Models the data attributes of the images'''
    
    # data attributes of an Facebook Image:
    timestamp = models.DateField(auto_now=True)
    image = models.ImageField(blank=True)
    status = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)

    
    def __str__(self):
        '''Return a string representation of this object.'''

        return f'image for {self.status}'
    
class Friend(models.Model):
    '''Models the data attributes of a Friend'''

    # data attributes of an Facebook Friend:
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this object.'''

        return f'{self.profile1} & {self.profile2}'