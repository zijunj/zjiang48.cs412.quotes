# File: voter_analytics/urls.py
# Author: Zi Jun Jiang (zjiang48@bu.edu), 11/11/2024
# Description: Directs the urls to the correct function
# From the views.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', VoterListView.as_view(), name="home"),
    path(r'voters', VoterListView.as_view(), name="voters"),
    path(r'voter/<int:pk>', VoterDetailView.as_view(), name="voter_detail"), 
    path(r'graphs', VoterGraphsView.as_view(), name="graphs"),

]