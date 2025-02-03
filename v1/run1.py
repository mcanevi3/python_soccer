import hashlib
import time
import os
import http.client
import json
import numpy as np

def calculate_file_hash(file_path:str):
    with open(file_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return file_hash
def read_file_hash(file_path:str):
    hash_str=""
    if os.path.exists(file_path+".hash"):
        with open(file_path+".hash", "r") as f:
            hash_str=f.read()
    else:
        pass
    return hash_str
def write_file_hash(file_path:str):
    hash=calculate_file_hash(file_path)
    with open(file_path+".hash", "w") as f:
        f.write(hash)
        f.close()

def detect_file_change(file_path:str):
    old_hash=read_file_hash(file_path)
    new_hash=calculate_file_hash(file_path)
    if old_hash==new_hash:
        # file not changed
        return False
    else:
        # file changed
        return True


API_URL="api.collectapi.com"
API_KEY="apikey 4D0Q5Rm6Mu9Bcxhqsl4E93:3B3nXf3V2IO7FYQemKnKcz"
def sporapi_leaguesList():
    conn = http.client.HTTPSConnection(API_URL)
    headers = {'content-type': "application/json",'authorization': API_KEY}
    conn.request("GET", "/sport/leaguesList", headers=headers)
    res = conn.getresponse()
    data = res.read()
    with open("raw_data/leaguesList.resp", "w") as f:
        f.write(data.decode("utf-8"))
        f.close()
def sporapi_results(name:str):
    conn = http.client.HTTPSConnection(API_URL)
    headers = {'content-type': "application/json",'authorization': API_KEY}
    conn.request("GET", "/sport/results?data.league="+name, headers=headers)
    res = conn.getresponse()
    data = res.read()
    with open("raw_data/results"+name+".resp", "w") as f:
        f.write(data.decode("utf-8"))
        f.close()
def sporapi_league(name:str):
    conn = http.client.HTTPSConnection(API_URL)
    headers = {'content-type': "application/json",'authorization': API_KEY}
    conn.request("GET", "/sport/league?data.league="+name, headers=headers)
    res = conn.getresponse()
    data = res.read()
    with open("raw_data/league"+name+".resp", "w") as f:
        f.write(data.decode("utf-8"))
        f.close()
def sporapi_goalKings(name:str):
    conn = http.client.HTTPSConnection(API_URL)
    headers = {'content-type': "application/json",'authorization': API_KEY}
    conn.request("GET", "/sport/goalKings?data.league="+name, headers=headers)
    res = conn.getresponse()
    data = res.read()
    with open("raw_data/goalKings"+name+".resp", "w") as f:
        f.write(data.decode("utf-8"))
        f.close()

# def sporapi():
#     commands={"/sport/leaguesList","/sport/results?data.league=super-lig","/sport/league?data.league=super-lig","/sport/goalKings?data.league=super-lig"}    
#     sporapi_results("super-lig")
#     sporapi_league("super-lig")
#     sporapi_goalKings("super-lig")

def leaguesList_read_from_file():
    obj=[]
    with open("raw_data/leagueList.resp", "rb") as f:
        obj=json.loads(f.read())
        return obj['result']
        
def results_read_from_file(name:str):
    obj=[]
    with open("raw_data/results"+name+".resp", "rb") as f:
        obj=json.loads(f.read())
        return obj['result']

def league_read_from_file(name:str):
    obj=[]
    with open("raw_data/league"+name+".resp", "rb") as f:
        obj=json.loads(f.read())
        return obj['result']

def print_league():
    league=league_read_from_file("super-lig")  
    for i in range(0,len(league)):
        print(league[i])

def find_team_in_league(team_name:str):
    league=league_read_from_file("super-lig")    
    for i in range(0,len(league)):
        row=league[i]
        if(row['team']==team_name):
            return i,row
    return -1,{'rank': None, 'draw': None, 'lose': None, 'win': None, 'play': None, 'point': None, 'goalfor': None, 'goalagainst': None, 'goaldistance': None, 'team': None}

def normalize(vec):
    vmax=np.max(vec)
    vmin=np.min(vec)
    nvec=np.zeros(vec.shape)
    for i in range(0,len(vec)):
        nvec[i]=(vec[i]-vmin)/(vmax-vmin)
    return nvec

def predict_score(teamname1:str,teamname2:str):
    league=league_read_from_file("super-lig") 
    n=len(league)
    vec_rank=np.zeros((n,))
    vec_draw=np.zeros((n,))
    vec_lose=np.zeros((n,))
    vec_win=np.zeros((n,))
    vec_play=np.zeros((n,))
    vec_point=np.zeros((n,))
    vec_goalfor=np.zeros((n,))
    vec_goalagainst=np.zeros((n,))
    vec_goaldistance=np.zeros((n,))
    vec_team=[]
    for i in range(0,n):
        row=league[i]
        vec_rank[i]=int(row['rank'])
        vec_draw[i]=int(row['draw'])
        vec_lose[i]=int(row['lose'])
        vec_win[i]=int(row['win'])
        vec_play[i]=int(row['play'])
        vec_point[i]=int(row['point'])
        vec_goalfor[i]=int(row['goalfor'])
        vec_goalagainst[i]=int(row['goalagainst'])
        vec_goaldistance[i]=int(row['goaldistance'])
        vec_team.append(row['team'])

    nvec_rank=normalize(vec_rank)
    nvec_draw=normalize(vec_draw)
    nvec_lose=normalize(vec_lose)
    nvec_win=normalize(vec_win)
    nvec_play=normalize(vec_play)
    nvec_point=normalize(vec_point)
    nvec_goalfor=normalize(vec_goalfor)
    nvec_goalagainst=normalize(vec_goalagainst)
    nvec_goaldistance=normalize(vec_goaldistance)

    i_home,row_home=find_team_in_league(teamname1)
    i_away,row_away=find_team_in_league(teamname2)
    rank_home=nvec_rank[i_home]
    draw_home=nvec_draw[i_home]
    lose_home=nvec_lose[i_home]
    win_home=nvec_win[i_home]
    play_home=nvec_play[i_home]
    goalfor_home=nvec_goalfor[i_home]
    goalagainst_home=nvec_goalagainst[i_home]

    rank_away=nvec_rank[i_away]
    draw_away=nvec_draw[i_away]
    lose_away=nvec_lose[i_away]
    win_away=nvec_win[i_away]
    play_away=nvec_play[i_away]
    goalfor_away=nvec_goalfor[i_away]
    goalagainst_away=nvec_goalagainst[i_away]

    # rank draw lose win play
    coef=np.array([-0.1,4,-2,2,0.5,4,-2])
    val_home=coef[0]*rank_home+coef[1]*draw_home+coef[2]*lose_home+coef[3]*win_home+coef[4]*play_home
    val_home+=coef[5]*goalfor_home+coef[6]*goalagainst_home
    val_home=val_home/np.sqrt(np.sum(coef**2))
    val_away=coef[0]*rank_away+coef[1]*draw_away+coef[2]*lose_away+coef[3]*win_away+coef[4]*play_away
    val_away=val_away/np.sqrt(np.sum(coef**2))
    val_away+=coef[5]*goalfor_away+coef[6]*goalagainst_away

    thresh=0.02
    print("values: "+str(val_home)+" "+str(val_away))
    if val_home>val_away+thresh:
        return "home"
    elif val_home+thresh<val_away:
        return "away"
    else:
        return "draw"

games=results_read_from_file("super-lig")
for i in range(0,len(games)):
    the_game=games[i]
    team_home=the_game['home']
    team_away=the_game['away']
    i_home,row_home=find_team_in_league(team_home)
    i_away,row_away=find_team_in_league(team_away)
    game_date=the_game['date']
    print("Game: "+"("+str(i_home+1)+".)"+team_home+" vs "+"("+str(i_away+1)+".)"+team_away+" "+game_date)
    score=predict_score(team_home,team_away)
    if score=="home":
        print(team_home+" wins")
    elif score=="away":
        print(team_away+" wins")
    else:
        print("draw")
    print("")



