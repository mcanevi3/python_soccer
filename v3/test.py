import http.client
import json
import os

def save_to_file(path_name:str,strdata:str):
    with open(path_name, "w") as f:
        f.write(strdata)
        f.close()

def get_from_file(path_name:str):
    if os.path.exists(path_name):
        with open(path_name, "r") as f:
            return json.loads(f.read())
    else:
        return None

def get_from_api(command:str):
    conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")
    headers = {'x-rapidapi-key': "ae117033ebmsh5ffd3dcd618e951p1ab50cjsn5abc16d907ab",'x-rapidapi-host': "api-football-v1.p.rapidapi.com"}

    conn.request("GET", command, headers=headers)
    res = conn.getresponse()
    data = json.loads(res.read())
    return data

def find_dict_in_list_by_name(cmd_name:str,vec:list):
    res={}
    for i in range(0,len(vec)):
        obj=vec[i]
        if obj['name']==cmd_name:
            res=obj
            return res
    return res

commands=[
    {'name':'countries_','api_command':'/v3/countries','args':[]},
    {'name':'leagues_','api_command':'/v3/leagues?','args':['country']},
    {'name':'standings_','api_command':'/v3/standings?','args':['league','season']},
    ]
def run_cmd(cmd:str,arg_val:list):
    command=find_dict_in_list_by_name(cmd,commands)
    args=command['args']
    if not args:
        assert (not arg_val),"The command "+cmd+" should not have args!"
        file_name=command['name']+".json"
    else:
        assert arg_val,"The command "+cmd+" should have args "+'_'.join(arg_val)+" !"
        assert len(arg_val)==len(args),"Arg values and keys must be same length!"
        file_name=command['name']+'_'.join(arg_val)+".json"
    path_name="raw_data/"+file_name

    if os.path.exists(path_name):
        print("using file:"+path_name)
        data=get_from_file(path_name)
    else:
        api_args=''
        for i in range(0,len(arg_val)):
            if i==0:
                api_args+=args[i]+"="+arg_val[i]
            else:
                api_args+="&"+args[i]+"="+arg_val[i]

        api_command=command['api_command']+api_args
        data=get_from_api(api_command)
        save_to_file(path_name,json.dumps(data))
    return data

data=run_cmd("leagues_",['turkey'])
data=run_cmd("standings_",['203','2020'])
