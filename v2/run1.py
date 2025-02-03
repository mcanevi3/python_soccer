import http.client
import json

# https://rapidapi.com/api-sports/api/api-football/playground/apiendpoint_0b842708-b991-455c-8aec-a98bfb048285

conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")
headers = {'x-rapidapi-key': "ae117033ebmsh5ffd3dcd618e951p1ab50cjsn5abc16d907ab",'x-rapidapi-host': "api-football-v1.p.rapidapi.com"}

def get_country_code(name:str):
    conn.request("GET", "/v3/countries", headers=headers)
    res = conn.getresponse()

    data=json.loads(res.read())

    response=data["response"]
    for i in range(0,len(response)):
        row=response[i]
        if row['name']==name:
            return row
        else:
            continue
    return ""

def get_leagues_by_country(name:str):
    conn.request("GET", "/v3/leagues?country="+name, headers=headers)
    res = conn.getresponse()

    data=json.loads(res.read())
    response=data['response']
    
    resp1=response[0]
    league_name=resp1['league']['name']
    league_id=resp1['league']['id']
    print(league_name)
    print(league_id)

# get_leagues_by_country("Turkey")
def get_leagues_by_country(name:str):
    conn.request("GET", "/v3/standings?league=203&season=2020", headers=headers)
    res = conn.getresponse()

    data=json.loads(res.read())
    response=data['response']
    for i in range(0,len(response)):
        print(response[i])

get_leagues_by_country("asd")