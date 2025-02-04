import http.client
import json

conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")
headers = {'x-rapidapi-key': "ae117033ebmsh5ffd3dcd618e951p1ab50cjsn5abc16d907ab",'x-rapidapi-host': "api-football-v1.p.rapidapi.com"}

def two_teams_history(team1:str,team2:str):
    # assume same country
    
    pass