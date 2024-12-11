# File: ultistats/urls.py
# Author: Zi Jun Jiang (zjiang48@bu.edu), 12/10/2024
# Description: Directs the urls to the correct function
# From the views.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import *

urlpatterns = [
    path('', HomepageView.as_view(), name='home'),  # Homepage
    
    # Stats  
    path('stats/', StatsPageView.as_view(), name='stats'),
    path('add-game-stats/<int:pk>/', AddGameStatsView.as_view(), name='add_game_stats'),

    
    # Teams
    path('teams/', TeamListView.as_view(), name='team_list'),
    path('teams/<int:pk>/', TeamDetailView.as_view(), name='team_detail'),
    path('team-rankings/', TeamRankingsView.as_view(), name='team_rankings'),
    path('team/<int:pk>/statistics/', TeamStatisticsView.as_view(), name='team_statistics'),
    
    # Players
    path('players/<int:pk>/', PlayerDetailView.as_view(), name='player_detail'),
    path('player-search/', PlayerListView.as_view(), name='player_search'),
    
    # Games
    path('games/', GameListView.as_view(), name='game_list'),
    path('games/<int:pk>/', GameDetailView.as_view(), name='game_detail'),
    path('add-game/', AddGameView.as_view(), name='add_game'),
    path('game/<int:pk>/delete/', GameDeleteView.as_view(), name='delete_game'),
    
    # Login and Logout
    path('login/', LoginView.as_view(template_name='ultistats/login.html', next_page='/ultistats'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/ultistats'), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),

    # Download
    path('download/<str:stat_type>/', DownloadStatsCSVView.as_view(), name='download_stats'),
   

]
