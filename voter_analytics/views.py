# File: voter_analytics/views.py
# Author: Zi Jun Jiang (zjiang48@bu.edu), 11/11/2024
# Description: Controller part of MVC as this file creates 
# functions/classes to connect urls to the correct templates
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import Min, Max
from django.db.models.functions import ExtractYear
from django.core.exceptions import ValidationError


import plotly
import plotly.graph_objects as go


# Create your views here.

class VoterListView(ListView):
    '''View to show a lists of voters.'''

    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100 # show 50 voters per page
    
    def get_queryset(self) -> QuerySet[Any]:
        '''Limit the Voters to a small number of records'''

        # default query set is all of the records:
        qs = super().get_queryset()
        
        # Handle search form/URL parameters
        party_affiliation = self.request.GET.get('party_affiliation')
        min_year = self.request.GET.get('min_dob_year')
        max_year = self.request.GET.get('max_dob_year')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        # Apply filters if each parameter is present in the GET request
        if party_affiliation:
            qs = qs.filter(party_affiliation__icontains=party_affiliation)

        if min_year:
            qs = qs.filter(dob__year__gte=min_year).order_by('dob')

        if max_year:
            qs = qs.filter(dob__year__lte=max_year).order_by('dob')

        if voter_score:
            qs = qs.filter(voter_score__icontains=voter_score)

        if v20state == '1':  # Check if value is '1'
            qs = qs.filter(v20state='TRUE')

        if v21town == '1':
            qs = qs.filter(v21town='TRUE')

        if v21primary == '1':
            qs = qs.filter(v21primary='TRUE')

        if v22general == '1':
            qs = qs.filter(v22general='TRUE')

        if v23town == '1':
            qs = qs.filter(v23town='TRUE')

        return qs
    
class VoterDetailView(DetailView):
    '''Display a single Result on it's own page.'''

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = "v"
    
class VoterGraphsView(ListView):
    '''Display Graphs for the voters.'''

    template_name = 'voter_analytics/graph.html'
    model = Voter
    context_object_name = 'voters'
    
    def get_queryset(self) -> QuerySet[Any]:
        '''Limit the Voters to a small number of records'''

        # default query set is all of the records:
        qs = super().get_queryset()
        
        # Handle search form/URL parameters
        party_affiliation = self.request.GET.get('party_affiliation')
        min_year = self.request.GET.get('min_dob_year')
        max_year = self.request.GET.get('max_dob_year')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        # Apply filters if each parameter is present in the GET request
        if party_affiliation:
            qs = qs.filter(party_affiliation__icontains=party_affiliation)

        if min_year:
            qs = qs.filter(dob__year__gte=min_year).order_by('dob')

        if max_year:
            qs = qs.filter(dob__year__lte=max_year).order_by('dob')

        if voter_score:
            qs = qs.filter(voter_score__icontains=voter_score)

        if v20state == '1':  # Check if value is '1'
            qs = qs.filter(v20state='TRUE')

        if v21town == '1':
            qs = qs.filter(v21town='TRUE')

        if v21primary == '1':
            qs = qs.filter(v21primary='TRUE')

        if v22general == '1':
            qs = qs.filter(v22general='TRUE')

        if v23town == '1':
            qs = qs.filter(v23town='TRUE')

        return qs
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''Gets the context data and displays graphs'''
        
        # Get the superclass version of context
        context = super().get_context_data(**kwargs)

        # Get the filtered queryset based on the user's search criteria
        qs = self.get_queryset()
        context['voters'] = qs  # Set the filtered voters in context

        # Get total number of voters based on the filtered queryset
        total_voters = qs.count()

        # Get the minimum and maximum year from the `dob` field in the filtered queryset
        min_year = qs.aggregate(min_dob_year=Min(ExtractYear('dob')))['min_dob_year']
        max_year = qs.aggregate(max_dob_year=Max(ExtractYear('dob')))['max_dob_year']
        
        # # Special case: user's max_year is less than min_year
        if (max_year and min_year) is None:
            fig = go.Bar(x=[], y=[])
            bar1_div = plotly.offline.plot({
                'data': [fig],
                "layout": go.Layout(
                    title=f"Voter Birth Year Distribution (n={total_voters})",
                    xaxis=dict(title="Birth Year"),
                    yaxis=dict(title="Number of Voters")
                )
            }, auto_open=False, output_type='div')

            # Add this to the context data for use in the template
            context['bar1_div'] = bar1_div
        
        else:
            # Create a bar chart with the number of voters by birth year
            x = list(range(min_year, max_year + 1))
            y = [qs.filter(dob__year=year).count() for year in x]

            fig = go.Bar(x=x, y=y)
            bar1_div = plotly.offline.plot({
                'data': [fig],
                "layout": go.Layout(
                    title=f"Voter Birth Year Distribution (n={total_voters})",
                    xaxis=dict(title="Birth Year"),
                    yaxis=dict(title="Number of Voters")
                )
            }, auto_open=False, output_type='div')

            # Add this to the context data for use in the template
            context['bar1_div'] = bar1_div

        # Get all unique values for the party_affiliation field in the filtered queryset
        unique_party_affiliations = qs.order_by('party_affiliation').values_list('party_affiliation', flat=True).distinct()

        # Create a pie chart of voters by party affiliation
        x = list(unique_party_affiliations)
        y = [qs.filter(party_affiliation=party_aff).count() for party_aff in x]

        fig = go.Pie(labels=x, values=y)
        bar2_div = plotly.offline.plot({
            'data': [fig],
            "layout": go.Layout(
                title=f"Voter Distribution by Party (n={total_voters})"
            )
        }, auto_open=False, output_type='div')

        # Add this to the context data for use in the template
        context['bar2_div'] = bar2_div


        # Create a bar chart with the number of voters who passed in specific elections
        election_fields = ['v20state', 'v21primary', 'v21town', 'v22general', 'v23town']
        x = election_fields
        y = [qs.filter(**{election: "TRUE"}).count() for election in election_fields]

        fig = go.Bar(x=x, y=y)
        bar3_div = plotly.offline.plot({
            'data': [fig],
            "layout": go.Layout(
                title=f"Voter Participation by Election Type (n={total_voters})",
                xaxis=dict(title="Election"),
                yaxis=dict(title="Number of Voters")
            )
        }, auto_open=False, output_type='div')

        # Add this to the context data for use in the template
        context['bar3_div'] = bar3_div

        return context

    
    