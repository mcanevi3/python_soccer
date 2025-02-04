class League:
    id=None
    name=""
    type=""
    country=""
    country_code=""
    country_flag=""
    seasons=[]
    def print(self):
        print(self.name+" ["+self.type+","+str(self.id)+"]")
        print(self.country+","+self.country_code)
        print(self.seasons)
        
class LeagueList:
    def __init__(self, json_obj:list):
        self.obj = json_obj
        self.extract()

    def extract(self):
        route_id=["league","id"]
        route_name=["league","name"]
        route_type=["league","type"]
        route_country=["country","name"]
        route_country_code=["country","code"]
        route_country_flag=["country","flag"]
        
        league=League()
        league.name=self.get_with_route(route_name)
        league.id=self.get_with_route(route_id)
        league.type=self.get_with_route(route_type)
        league.country=self.get_with_route(route_country)
        league.country_code=self.get_with_route(route_country_code)
        league.country_flag=self.get_with_route(route_country_flag)
        
        seasons=self.get_with_route(["seasons"])
        league.seasons=self.get_key_in_list(seasons,"year")
        
        league.print()

    def get_with_route(self,route:list):
        temp=self.obj[0]
        for part in route:
            temp=temp[part]
        return temp
    def get_key_in_list(self,vec:list,key:str):
        temp=[]
        for v in vec:
            temp.append(v[key])
        return temp