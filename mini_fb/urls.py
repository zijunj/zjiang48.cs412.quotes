# File: mini_fb/urls.py
# Author: Zi Jun Jiang (zjiang48@bu.edu), 10/2/2024
# Description: Directs the urls to the correct function
# From the views.py
from django.urls import path

from django.conf import settings

from . import views


urlpatterns = [
    path(r'', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),
   

]