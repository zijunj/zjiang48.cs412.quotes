# mini_fb/admin.py
from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Profile)
admin.site.register(StatusMessage   )
admin.site.register(Image)
admin.site.register(Friend)