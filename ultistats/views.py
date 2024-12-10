# File: ultistats/views.py
# Author: Zi Jun Jiang (zjiang48@bu.edu), 11/11/2024
# Description: Controller part of MVC as this file creates 
# functions/classes to connect urls to the correct templates
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView, TemplateView, DeleteView, View
from django.db.models import Min, Max
from django.db.models.functions import ExtractYear
from django.core.exceptions import ValidationError
from django.http import Http404
from itertools import groupby
from operator import attrgetter
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateResponseMixin
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.mixins import LoginRequiredMixin
import csv
from django.http import HttpResponse

from django.contrib.auth.forms import UserCreationForm


from django.views.generic.edit import FormView, BaseFormView


from django.db.models import Sum, Count

from django.contrib import messages
from .forms import *

from .models import *
from django.db.models import Q


import plotly
import plotly.graph_objects as go
from colorthief import ColorThief
from django.contrib.auth import login



# Create your views here.

class HomepageView(TemplateView):
    template_name = 'ultistats/home.html'

    def get_context_data(self, **kwargs):
        # Use Django's built-in method to inject additional context into the template
        context = super().get_context_data(**kwargs)
        context['total_teams'] = Team.objects.count()
        context['total_players'] = Player.objects.count()
        context['total_games'] = Game.objects.count()
        return context
    
# Signup for a account
class SignupView(CreateView):
    template_name = 'ultistats/signup.html'
    form_class = UserCreationForm
    
    def form_valid(self, form):
        # Save the new user
        user = form.save()

        # Log the user in
        login(self.request, user)

        # Redirect to a success page
        return redirect('home')  # Replace 'home' with your desired URL name
    
# View for the links to the stats
class StatsPageView(TemplateView):
    template_name = 'ultistats/stats.html' 
    
# View for search of players
class PlayerListView(ListView):
    model = Player
    template_name = 'ultistats/player_search.html'  # The HTML template
    context_object_name = 'player'  # The variable name used in the template for pagination
    paginate_by = 25  # Number of players per page

    def get_queryset(self):
        # Get the search query from the request
        query = self.request.GET.get('q', '').strip()
        # Start with all players
        players = Player.objects.all()

        if query:
            # Split the query into parts (e.g., first and last name)
            query_parts = query.split()

            # If there are multiple parts (e.g., "John Doe"), search for both
            if len(query_parts) > 1:
                players = players.filter(
                    Q(first_name__icontains=query_parts[0]) & Q(last_name__icontains=query_parts[1])
                )
            else:
                # If there's only one part, search in both first_name and last_name
                players = players.filter(
                    Q(first_name__icontains=query) | Q(last_name__icontains=query)
                )

        return players

    def get_context_data(self, **kwargs):
        # Add the search query to the context
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Pass the search query to the template
        return context
    
# Detail view for a specific player
class PlayerDetailView(DetailView):
    model = Player
    template_name = 'ultistats/player_detail.html'
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = self.object

        # Fetch game statistics for the player
        player_game_stats = GameStats.objects.filter(player=player).select_related('game')

        # Calculate aggregated stats
        aggregated_stats = player_game_stats.aggregate(
            total_goals=Sum('goals_scored'),
            total_assists=Sum('assists'),
            total_blocks=Sum('blocks'),
            total_turnovers=Sum('turnovers')
        )
        
        context['player_game_stats'] = player_game_stats
        context['aggregated_stats'] = aggregated_stats
        return context



# List view for all teams
class TeamListView(ListView):
    model = Team
    template_name = 'team_list.html'  # Template to render the list
    context_object_name = 'teams'    # Name of the object in the template

    def get_context_data(self, **kwargs):
        # Get the default context from the superclass
        context = super().get_context_data(**kwargs)
        
        # Group teams by their college_region
        teams_by_region = defaultdict(list)
        for team in Team.objects.all():
            teams_by_region[team.college_region].append(team)
        
        # Add the grouped data to the context
        context['teams_by_region'] = dict(teams_by_region)  # Convert to a regular dict for template compatibility
        return context
    

# List view for team rankings
class TeamRankingsView(ListView):
    model = Team
    template_name = 'ultistats/team_rankings.html'  # Template to render the list
    context_object_name = 'teams'  # Name of the object in the template
    paginate_by = 25  # Number of teams per page

    def get_queryset(self):
        # Start with all teams
        queryset = Team.objects.all()

        # Apply filters based on GET parameters
        college_region = self.request.GET.get('college_region', '')
        college_conference = self.request.GET.get('college_conference', '')
        school_name = self.request.GET.get('school_name', '')

        if college_region:
            queryset = queryset.filter(college_region=college_region)
        if college_conference:
            queryset = queryset.filter(college_conference=college_conference)
        if school_name:
            queryset = queryset.filter(name__icontains=school_name)

        # Sort by rank
        return queryset.order_by('rank')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = [
            'New England', 'Atlantic Coast', 'Southwest', 'South Central', 
            'Northwest', 'North Central', 'Southeast', 'Ohio Valley', 
            'Great Lakes', 'Metro East'
        ]
        context['conferences'] = [
            'Metro Boston DI', 'Greater New England DI', 'Carolina DI', 'SoCal DI', 
            'Rocky Mountain DI', 'Cascadia DI', 'Northwoods DI', 
            'Southern Appalachian DI', 'West Penn DI', 'South Texas DI', 
            'Michigan DI', 'NorCal DI', 'Big Sky DI', 'Gulf Coast DI', 
            'Ozarks DI', 'Western NY DI', 'Lake Superior DI', 'Ohio DI', 
            'Illinois DI', 'Virginia DI', 'Florida DI', 'East Penn DI', 
            'West Plains DI', 'East Plains DI', 'Colonial DI', 'Desert DI', 
            'North New England DIII', 'Hudson Valley DI', 'Metro NY DI', 
            'North Texas DI'
        ]
        context['college_region'] = self.request.GET.get('college_region', '')
        context['college_conference'] = self.request.GET.get('college_conference', '')
        context['school_name'] = self.request.GET.get('school_name', '')
        return context

# Detail view for a specific team
class TeamDetailView(DetailView):
    model = Team
    template_name = 'ultistats/team_detail.html'
    context_object_name = 'team'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        # get the context data from the superclass
        context =  super().get_context_data(**kwargs)
        
        # find the Team identified by the PK from the URL pattern
        team = Team.objects.get(pk=self.kwargs['pk'])
        
        # find all the players associated to that team
        players = Player.objects.filter(team=team)
        
        # add the Team referred to by the URL into this context
        context['players'] = players
        
        # Extract the dominant color if a logo exists
        if team.logo:
            color_thief = ColorThief(team.logo.path)
            dominant_color = color_thief.get_color(quality=1)  # Returns (R, G, B)
            context['dominant_color'] = f'rgb({dominant_color[0]}, {dominant_color[1]}, {dominant_color[2]})'
        else:
            # Default color if no logo
            context['dominant_color'] = '#f9f9f9'  
        
        return context
 
# Detail view for the team statistics 
class TeamStatisticsView(DetailView):
    model = Team
    template_name = 'ultistats/team_statistics.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.object

        # Calculate total games played
        total_games = team.wins + team.losses
        
        win_percentage = round((team.wins / total_games) * 100, 2) if total_games > 0 else 0


        # Aggregate team statistics from all players
        team_stats = GameStats.objects.filter(player__team=team).aggregate(
            total_goals=Sum('goals_scored'),
            total_assists=Sum('assists'),
            total_blocks=Sum('blocks'),
            total_turnovers=Sum('turnovers')
        )

        # Add aggregated statistics to the context
        context['total_games'] = total_games
        context['team_stats'] = team_stats
        context['win_percentage'] = win_percentage
        
        # Add list of other teams for comparison
        other_teams = Team.objects.exclude(pk=team.pk)  # Exclude the current team
        context['other_teams'] = other_teams
        
        # Add logic for head-to-head comparison
        other_team_id = self.request.GET.get('other_team')  # Get other team ID from query parameter
        if other_team_id:
            other_team = Team.objects.get(pk=other_team_id)

            # Calculate total games and win percentage for the other team
            total_games_other = other_team.wins + other_team.losses
            win_percentage_other = round((other_team.wins / total_games_other) * 100, 2) if total_games_other > 0 else 0

            # Aggregate statistics for the other team
            other_team_stats = GameStats.objects.filter(player__team=other_team).aggregate(
                total_goals=Sum('goals_scored'),
                total_assists=Sum('assists'),
                total_blocks=Sum('blocks'),
                total_turnovers=Sum('turnovers')
            )

            # Add other team's statistics to the context
            context['other_team'] = other_team
            context['other_team_stats'] = other_team_stats
            context['win_percentage_other'] = win_percentage_other
            
        # Get all teams (including the selected team for comparison)
        all_teams = Team.objects.all()
        context['other_teams'] = all_teams

        return context
    
    



    

# List view for all games
class GameListView(ListView):
    model = Game
    template_name = 'game_list.html'
    context_object_name = 'games'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Fetch all games and order them by tournament for grouping
        games = Game.objects.order_by('tournament', 'date_played')

        # Group games by tournament using groupby
        grouped_games = {
            tournament: list(games_in_tournament)
            for tournament, games_in_tournament in groupby(games, attrgetter('tournament'))
        }

        # Add the grouped games to the context
        context['grouped_games'] = grouped_games
        return context


# Detail view for a specific game
class GameDetailView(DetailView):
    model = Game
    template_name = 'ultistats/game_detail.html'
    context_object_name = 'game'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.object
        # Separate stats for each team
        context['team_a_stats'] = game.game_stats.filter(player__team=game.team_a)
        context['team_b_stats'] = game.game_stats.filter(player__team=game.team_b)
        return context
    
class AddGameView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Game
    form_class = GameForm
    template_name = 'ultistats/add_game.html'
    success_url = reverse_lazy('game_list')
    success_message = "Game and stats added successfully!"
    
class GameDeleteView(LoginRequiredMixin, DeleteView):
    model = Game
    template_name = 'ultistats/delete_game.html'
    success_url = reverse_lazy('game_list')  # Redirect to the game list after deletion
    

class AddGameStatsView(LoginRequiredMixin, FormView):
    template_name = 'ultistats/add_gamestats.html'

    def get_context_data(self, **kwargs):
        context = {}
        game = get_object_or_404(Game, pk=self.kwargs['pk'])
        context['game'] = game

        # Get players for each team
        team1_players = Player.objects.filter(team=game.team_a)
        team2_players = Player.objects.filter(team=game.team_b)

        # Pass teams and players to context
        context['team1'] = game.team_a
        context['team1_players'] = team1_players
        context['team2'] = game.team_b
        context['team2_players'] = team2_players

        # Initialize formsets for each team
        if self.request.POST:
            formset_team1 = GameStatsFormSet(self.request.POST, prefix='team1', instance=game)
            formset_team2 = GameStatsFormSet(self.request.POST, prefix='team2', instance=game)
            
            # Restrict queryset for each team
            for form in formset_team1:
                form.fields['player'].queryset = team1_players
            for form in formset_team2:
                form.fields['player'].queryset = team2_players
        else:
            formset_team1 = GameStatsFormSet(queryset=GameStats.objects.filter(player__team=game.team_a), prefix='team1', instance=game)
            formset_team2 = GameStatsFormSet(queryset=GameStats.objects.filter(player__team=game.team_b), prefix='team2', instance=game)

            # Restrict queryset for each team
            for form in formset_team1:
                form.fields['player'].queryset = team1_players
            for form in formset_team2:
                form.fields['player'].queryset = team2_players


        context['formset_team1'] = formset_team1
        context['formset_team2'] = formset_team2

        return context

    def post(self, request, *args, **kwargs):
        game = get_object_or_404(Game, pk=self.kwargs['pk'])
        team1_players = Player.objects.filter(team=game.team_a)
        team2_players = Player.objects.filter(team=game.team_b)

        # Bind formsets with POST data
        formset_team1 = GameStatsFormSet(request.POST, prefix='team1', instance=game)
        print(len(formset_team1))
        formset_team2 = GameStatsFormSet(request.POST, prefix='team2', instance=game)
        
        print("Team 1 Management Form Data:", formset_team1.management_form.data)
        print("Team 2 Management Form Data:", formset_team2.management_form.data)
        # Restrict queryset for validation
        for form in formset_team1:
            form.fields['player'].queryset = team1_players
        for form in formset_team2:
            form.fields['player'].queryset = team2_players
            
        # Validate and save both formsets
        if formset_team1.is_valid() and formset_team2.is_valid():
            formset_team1.save()
            formset_team2.save()
            messages.success(request, 'Stats for both teams added successfully!')
            return redirect('game_detail', pk=game.pk)
        else:
            # Debug invalid forms
            print("Team 1 Formset Errors:", formset_team1.errors)
            print("Team 2 Formset Errors:", formset_team2.errors)
            messages.error(request, 'There was an error with your submission.')
            return self.render_to_response(self.get_context_data())

class DownloadStatsCSVView(View):
    
    def get(self, request, stat_type, *args, **kwargs):
        # Create the HttpResponse object with the appropriate CSV header
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{stat_type}_stats.csv"'

        # Determine the type of data to export
        if stat_type == 'players':
            self.download_player_stats(response)
        elif stat_type == 'teams':
            self.download_team_stats(response)
        elif stat_type == 'games':
            self.download_game_stats(response)
        else:
            response.status_code = 400
            response.write("Invalid stat type")
            return response

        return response

    def download_player_stats(self, response):
        writer = csv.writer(response)
        writer.writerow(['Player Name', 'Team', 'Total Goals', 'Total Assists', 'Total Blocks', 'Total Turnovers'])
        players = Player.objects.all()
        for player in players:
            total_goals = GameStats.objects.filter(player=player).aggregate(models.Sum('goals_scored'))['goals_scored__sum'] or 0
            total_assists = GameStats.objects.filter(player=player).aggregate(models.Sum('assists'))['assists__sum'] or 0
            total_blocks = GameStats.objects.filter(player=player).aggregate(models.Sum('blocks'))['blocks__sum'] or 0
            total_turnovers = GameStats.objects.filter(player=player).aggregate(models.Sum('turnovers'))['turnovers__sum'] or 0
            writer.writerow([
                f"{player.first_name} {player.last_name}",
                player.team.name,
                total_goals,
                total_assists,
                total_blocks,
                total_turnovers,
            ])

    def download_team_stats(self, response):
        writer = csv.writer(response)
        writer.writerow(['Team Name', 'Coach', 'City', 'Rank', 'Wins', 'Losses', 'College Region', 'College Conference'])
        teams = Team.objects.all()
        for team in teams:
            writer.writerow([
                team.name,
                team.coach,
                team.city,
                team.rank,
                team.wins,
                team.losses,
                team.college_region,
                team.college_conference,
            ])

    def download_game_stats(self, response):
        writer = csv.writer(response)
        writer.writerow(['Date Played', 'Location', 'Team A', 'Team B', 'Score Team A', 'Score Team B', 'Winning Team', 'Tournament'])
        games = Game.objects.all()
        for game in games:
            writer.writerow([
                game.date_played,
                game.location,
                game.team_a.name,
                game.team_b.name,
                game.score_team_a,
                game.score_team_b,
                game.winning_team.name if game.winning_team else 'N/A',
                game.tournament,
            ])
    