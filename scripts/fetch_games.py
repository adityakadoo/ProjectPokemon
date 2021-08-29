import requests
from pokedex.models import Game, Version

def run(*args):
    base_url = "https://pokeapi.co/api/v2/version/"

    i = 1
    while True:
        url = base_url+str(i)
        response = requests.get(url)
        
        if response.status_code!=200:
            break

        response_dict = response.json()
        if response_dict["name"]=="colosseum" or response_dict["name"]=="xd":
            i = i+1
            continue
        game_temp = Game(index = response_dict["id"],name = response_dict["name"])
        version_temp = Version.objects.get(name=response_dict["version_group"]["name"])
        game_temp.version = version_temp

        game_temp.save()
        i = i+1