import requests
from pokedex.models import Version, Ability, Ability_var

def run(*args):
    base_url = "https://pokeapi.co/api/v2/ability/"

    i = 1
    max_name = 0
    max_effect = 0
    max_description = 0
    while True:
        url = base_url+str(i)
        response = requests.get(url)
        
        if response.status_code!=200:
            if i < 10000:
                i = 10001
                continue
            else:
                break

        response_dict = response.json()
        ability_temp = Ability(index=response_dict["id"],name=response_dict["name"])
        if max_name < len(response_dict["name"]):
            max_name = len(response_dict["name"])

        for e in response_dict["effect_entries"]:
            if e["language"]["name"]=="en":
                ability_temp.effect = e["effect"]
                if max_effect < len(e["effect"]):
                    max_effect = len(e["effect"])

        ability_temp.save()

        generation_url = response_dict["generation"]["url"].split('/')
        generation = int(generation_url[-2])
        for e in Version.objects.all():
            ability_var_temp = Ability_var(version=e,ability=ability_temp)
            if e.generation<generation:
                continue
            for e1 in response_dict["flavor_text_entries"]:
                if e1["language"]["name"]=="en" and e1["version_group"]["name"]==e.name:
                    ability_var_temp.description = e1["flavor_text"]
                    if max_description <len(e1["flavor_text"]):
                        max_description = len(e1["flavor_text"])
                    ability_var_temp.save()
                    break

        i = i+1
    print("Max length of name field: ",max_name)
    print("Max length of effect field: ",max_effect)
    print("Max length of description field: ",max_description)