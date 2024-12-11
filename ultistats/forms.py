# File: ultistats/forms.py
# Author: Zi Jun Jiang (zjiang48@bu.edu), 12/10/2024
# Description: Creates forms for user to submit to the web application.

from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from .models import *

class GameForm(forms.ModelForm):
    '''A form to add a Game to the database'''
    class Meta:
        '''Associate this HTML form with the Game data model'''
        model = Game
        fields = ['date_played', 'location', 'team_a', 'team_b', 'score_team_a', 'score_team_b', 'winning_team', 'tournament']
        widgets = {
            'date_played': forms.DateInput(attrs={'type': 'date'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter game location'}),
            'tournament': forms.TextInput(attrs={'placeholder': 'Tournament name'}),
        }
        
class CustomGameStatsFormSet(BaseInlineFormSet):
    """
    A custom inline formset for GameStats that dynamically filters the player field.
    """

    def __init__(self, *args, **kwargs):
        form_kwargs = kwargs.pop('form_kwargs', {})
        self.game = form_kwargs.get('game', None)
        super().__init__(*args, **kwargs)

    def add_fields(self, form, index):
        """
        Add fields to each form, allowing for dynamic filtering of the player field.
        """
        super().add_fields(form, index)
        if self.game:
            # Dynamically filter players based on the game teams
            form.fields['player'].queryset = Player.objects.filter(team__in=[self.game.team_a, self.game.team_b])
            form.fields['player'].widget.attrs.update({'class': 'form-control form-control-sm'})



# Create the inline formset using the custom formset class
GameStatsFormSet = inlineformset_factory(
    Game,
    GameStats,
    fields=['player', 'goals_scored', 'assists', 'blocks', 'turnovers'],
    extra=1,
    can_delete=True,
    formset=CustomGameStatsFormSet  # Use the custom formset class
)

