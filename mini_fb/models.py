# File: mini_fb/models.py
# Author: Zi Jun Jiang (zjiang48@bu.edu), 10/2/2024
# Description: Model part of the MVC. This file allows admin
# to input data attributes for the Profile of each user.

from django.db import models

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