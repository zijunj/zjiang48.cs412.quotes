# File: ultistats/models.py
# Author: Zi Jun Jiang (zjiang48@bu.edu), 12/10/2024
# Description: Model part of the MVC. This file allows admin
# to input data models for the UltiStat application.

from django.db import models
from datetime import date
from django.utils.text import slugify



# Create your models here.

from django.db import models

class Team(models.Model):
    '''
    Team data attributes
    '''
    name = models.CharField(max_length=255)
    coach = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    rank = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    college_region = models.CharField(max_length=255)
    college_conference = models.CharField(max_length=255)
    logo = models.ImageField(blank=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    '''
        Player data attributes
    '''
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    jersey_number = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.team})"


class Game(models.Model):
    '''
        Game data attributes
    '''
    
    date_played = models.DateField()
    location = models.CharField(max_length=255)
    team_a = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='team_a_games')
    team_b = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='team_b_games')
    score_team_a = models.IntegerField()
    score_team_b = models.IntegerField()
    winning_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='winning_games', null=True, blank=True)
    tournament = models.CharField(max_length=255)


    def __str__(self):
        return f"{self.team_a.name} vs {self.team_b.name} on {self.date_played}"



class GameStats(models.Model):
    '''
        GameStats data attributes 
    '''
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_stats')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_stats')
    goals_scored = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    blocks = models.IntegerField(default=0)
    turnovers = models.IntegerField(default=0)

    def __str__(self):
        return f"Stats for {self.player} in {self.game}"

    
def load_players():
    '''Load data records from a CSV file into model instances.'''
    
    # open the file for reading:
    filename = r'C:\Users\Victor\Downloads\trash\players_washu.csv'
    f = open(filename)
    headers = f.readline() # read/discard the headers
    print(headers)
    
    # loop to read all the lines in the file
    for line in f:
        
        # provide protection around code that might generate an exception
            fields = line.split(',') # create a list of fields
            
            team = Team.objects.get(name='Washington University')
            
            # create a new instance of Player object with this record from CSV
            player = Player(
                            first_name = fields[0],
                            last_name = fields[1],
                            team = team,
                            jersey_number = fields[2],
                        )
            player.save() # save this instance to the database.
            
def load_teams():
    '''Load data records from a CSV file into model instances.'''
    
    # open the file for reading:
    filename = r'C:\Users\Victor\Downloads\trash\all_teams.csv'
    f = open(filename)
    headers = f.readline() # read/discard the headers
    print(headers)
    
    # loop to read all the lines in the file
    for line in f:
        
        # provide protection around code that might generate an exception
            fields = line.split(',') # create a list of fields
                
            # create a new instance of Team object with this record from CSV
            team = Team(
                            name = fields[0],
                            coach = fields[1],
                            city = fields[2],
                            rank = fields[3],
                            wins = fields[4],
                            losses = fields[5],
                            college_region = fields[6],
                            college_conference = fields[7],
                        )
            team.save() # save this instance to the database.
            
def load_game_stats():
    '''Load data records from a CSV file into model instances.'''

    
    # open the file for reading:
    filename = r'c:\Users\Victor\Downloads\trash\washu_georgiaVSwashu.csv'
    f = open(filename)
    headers = f.readline() # read/discard the headers
    print(headers)
    
    # loop to read all the lines in the file
    for line in f:
        
        # provide protection around code that might generate an exception
            fields = line.split(',') # create a list of fields
            
            
            # Filter player in the game stats
            player = Player.objects.get(first_name=fields[0], last_name = fields[1])
            
            # Fetch the team instance for team_a
            team_a = Team.objects.get(name="Georgia (Jojah)")
            
            # create a new instance of Gamestats object with this record from CSV
            gamestats = GameStats(
                            game = Game.objects.get(date_played = date(2024, 5, 24), team_a=team_a),
                            player = player,
                            goals_scored = fields[2],
                            assists = fields[3],
                            blocks = fields[4],
                            turnovers = fields[5],
                        )
            gamestats.save() # save this instance to the database.
            



