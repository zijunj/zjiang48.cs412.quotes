import json
from usau_scraper import *


def test_load_roster(school_name, team_name):
    print(f"Fetching roster for {school_name} - {team_name}...")
    
    data = getTeamRoster(teamURI="/teams/events/Eventteam/?TeamId=bxY3sCvAV7guXxmb9DOQy0I0ut4%2fypKD1DOBpQMZA48%3d")

    
    if data['res'] != 'OK' or not data['teams']:
        print("No team data found.")
        return

    for team_data in data['teams']:
        print(f"\n✅ Team: {team_data['teamName']} ({team_data['schoolName']})")

        for player in team_data['roster']:
            try:
                name = player.get('name', '').strip()
                jersey = player.get('no', '').strip()

                if " " in name:
                    first, last = name.split(" ", 1)
                else:
                    first, last = name, ''

                print(f"First: {first}, Last: {last}, Jersey #: {jersey}")
            except Exception as e:
                print(f"Error processing player: {player} — {e}")

test_load_roster("Harvard", "Red Line")

