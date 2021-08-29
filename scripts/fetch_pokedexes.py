import requests
from pokedex.models import Pokedex, Version, Pokemon

def run(*args):
    base_url = "https://pokeapi.co/api/v2/pokedex/"

    i = 1
    while True:
        url = base_url+str(i)
        response = requests.get(url)
        
        if response.status_code!=200:
            if i==10:
                i= i+1
                continue
            else:
                break

        response_dict = response.json()
        if response_dict["name"]=="conquest-gallery":
            i = i+1
            continue
        pokedex_temp = Pokedex(index = response_dict["id"],name = response_dict["name"])
        pokedex_temp.save()

        for e in response_dict["pokemon_entries"]:
            pokemon_temp = Pokemon.objects.filter(species=e["pokemon_species"]["name"])
            pokedex_temp.pokemon_entries.add(pokemon_temp[0])

        for e in response_dict["version_groups"]:
            version_temp = Version.objects.get(name=e["name"])
            pokedex_temp.versions.add(version_temp)
        i = i+1