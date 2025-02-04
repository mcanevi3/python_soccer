import http.client
import json

conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")
headers = {'x-rapidapi-key': "ae117033ebmsh5ffd3dcd618e951p1ab50cjsn5abc16d907ab",'x-rapidapi-host': "api-football-v1.p.rapidapi.com"}

def save_to_file(filename:str,strdata:str):
    with open("raw_data/"+filename, "w") as f:
        f.write(strdata)
        f.close()

def get_countries():
    conn.request("GET", "/v3/countries", headers=headers)
    res = conn.getresponse()

    data=json.loads(res.read())
    response=data["response"]
    
    save_to_file("countries.json",json.dumps(response))

get_countries()