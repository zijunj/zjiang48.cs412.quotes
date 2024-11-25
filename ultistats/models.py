from django.db import models
from datetime import date


# Create your models here.

from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=255)
    coach = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    win_count = models.IntegerField(default=0)
    loss_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Player(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    jersey_number = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.team})"


class Game(models.Model):
    date_played = models.DateField()
    location = models.CharField(max_length=255)
    team_a = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='team_a_games')
    team_b = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='team_b_games')
    score_team_a = models.IntegerField()
    score_team_b = models.IntegerField()
    winning_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='winning_games', null=True, blank=True)

    def __str__(self):
        return f"{self.team_a.name} vs {self.team_b.name} on {self.date_played}"



class GameStats(models.Model):
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
    filename = r'c:\Users\Victor\Downloads\trash\players_brown.csv'
    f = open(filename)
    headers = f.readline() # read/discard the headers
    print(headers)
    
    # loop to read all the lines in the file
    for line in f:
        
        # provide protection around code that might generate an exception
            fields = line.split(',') # create a list of fields
            
            team = Team.objects.get(name='Brownian Motion')
            
            # create a new instance of Result object with this record from CSV
            player = Player(
                            first_name = fields[0],
                            last_name = fields[1],
                            team = team,
                            jersey_number = fields[2],
                        )
            player.save() # save this instance to the database.
            
def load_game_stats():
    '''Load data records from a CSV file into model instances.'''

    
    # open the file for reading:
    filename = r'C:\Users\Victor\Downloads\trash\players_stats.csv'
    f = open(filename)
    headers = f.readline() # read/discard the headers
    print(headers)
    
    # loop to read all the lines in the file
    for line in f:
        
        # provide protection around code that might generate an exception
            fields = line.split(',') # create a list of fields
            
            player = Player.objects.get(first_name=fields[0], last_name = fields[1])
            
            # create a new instance of Result object with this record from CSV
            gamestats = GameStats(
                            game = Game.objects.get(date_played = date(2024, 5, 27)),
                            player = player,
                            goals_scored = fields[2],
                            assists = fields[3],
                            blocks = fields[4],
                            turnovers = fields[5],
                        )
            gamestats.save() # save this instance to the database.
            



