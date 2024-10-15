# File: mini_fb/urls.py
# Author: Zi Jun Jiang (zjiang48@bu.edu), 10/2/2024
# Description: Directs the urls to the correct function
# From the views.py
from django.urls import path

from django.conf import settings

from . import views


urlpatterns = [
    path(r'', views.ShowAllProfilesView.as_view(), name="home_page"),
    path(r'show_all_profiles', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name="profile"),
    path(r'create_profile', views.CreateProfileView.as_view(), name="create_profile"),
    path(r'profile/<int:pk>/create_status', views.CreateStatusMessageView.as_view(), name="create_status"), 



]