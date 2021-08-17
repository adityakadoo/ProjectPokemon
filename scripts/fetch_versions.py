import requests
from pokedex.models import Version

def run(*args):
    base_url = "https://pokeapi.co/api/v2/version-group/"

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
        version_temp = Version(index = response_dict["id"],name = response_dict["name"])

        generation_url = response_dict["generation"]["url"].split('/')
        version_temp.generation = generation_url[len(generation_url)-2]

        version_temp.save()
        i = i+1