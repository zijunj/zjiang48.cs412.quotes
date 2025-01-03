# File: mini_fb/urls.py
# Author: Zi Jun Jiang (zjiang48@bu.edu), 10/2/2024
# Description: Directs the urls to the correct function
# From the views.py
from django.urls import path

from django.conf import settings
from django.contrib.auth import views as auth_views 

from . import views


urlpatterns = [
    path(r'', views.ShowAllProfilesView.as_view(), name="home_page"),
    path(r'show_all_profiles', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name="profile"),
    path(r'create_profile', views.CreateProfileView.as_view(), name="create_profile"),
    path(r'status/create_status', views.CreateStatusMessageView.as_view(), name="create_status"),
    path(r'profile/update', views.UpdateProfileView.as_view(), name='update_profile'),
    path(r'status/<int:pk>/delete/', views.DeleteStatusMessageView.as_view(), name='delete_status'),
    path(r'status/update', views.UpdateStatusMessageView.as_view(), name='update_status'),
    path(r'profile/add_friend/<int:other_pk>/', views.CreateFriendView.as_view(), name='add_friend'),
    path(r'profile/friend_suggestions', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path(r'profile/news_feed', views.ShowNewsFeedView.as_view(), name='news_feed'),

    # authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html', next_page='show_all_profiles'), 
         name="login"), ## NEW
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), 
         name="logout"), ## NEW


]