import requests
from django.utils import timezone
import os
from django.core.files import File

def remove_escape_chars(s):
    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    t = s.translate(translator)
    return t

def get_filename(s):
    return s.replace('-','_')

def update_resource(endpoint_name,resource):
    response = requests.get("https://pokeapi.co/api/v2/"+str(endpoint_name)+"/"+str(resource.name))
    if response.status_code != 200:
        return False
    response_dict = response.json()

    if endpoint_name == 'pokemon':
        pokemon_data = {
            'base_experience': response_dict["base_experience"],
            'height': response_dict["height"],
            'weight': response_dict["weight"],
            'species': response_dict["species"]["name"],
            'hp': response_dict["stats"][0]["base_stat"],
            'attack': response_dict["stats"][1]["base_stat"],
            'defense': response_dict["stats"][2]["base_stat"],
            'sp_attack': response_dict["stats"][3]["base_stat"],
            'sp_defense': response_dict["stats"][4]["base_stat"],
            'speed': response_dict["stats"][5]["base_stat"],
        }

        pokemon_data['abilities'] = []
        for e in response_dict["abilities"]:
            pokemon_data['abilities'].append(e['ability']['name'])
        
        pokemon_data['types'] = []
        for e in response_dict['types']:
            pokemon_data['types'].append(e['type']['name'])
        
        species_url = response_dict["species"]["url"]
        species_response = requests.get(species_url)
        species_response_dict = species_response.json()

        if species_response_dict["evolves_from_species"] is None:
            pokemon_data['prev_evolution'] = None
        else:
            pokemon_data['prev_evolution'] = species_response_dict["evolves_from_species"]["name"]

        pokemon_data['pokedex_entries'] = dict()
        for e in species_response_dict["flavor_text_entries"]:
            if e["language"]["name"]=="en":
                pokemon_data['pokedex_entries'][e['version']['name']]=remove_escape_chars(e['flavor_text'])

        pokemon_data['moves'] = dict()
        for e1 in response_dict["moves"]:
            for e2 in e1["version_group_details"]:
                if e2['version_group']['name'] not in pokemon_data['moves'].keys():
                    pokemon_data['moves'][e2['version_group']['name']] = []
                move_dict = {
                    'name': e1['move']['name'],
                    'level': e2['level_learned_at'],
                    'method': e2['move_learn_method']['name'],
                }
                pokemon_data['moves'][e2['version_group']['name']].append(move_dict)

        image_url = response_dict["sprites"]["other"]["official-artwork"]["front_default"]
        if image_url==None:
            image_url = response_dict["sprites"]["other"]["dream_world"]["front_default"]
        if image_url==None:
            image_url = response_dict["sprites"]["front_default"]
        if image_url != None:
            image_response = requests.get(image_url)
            with open("temp.png",'wb') as f:
                f.write(image_response.content)
            os.remove("static/images/pokemon/"+get_filename(response_dict['name']+".png"))
            resource.image.save(get_filename("pokemon/"+response_dict['name']+".png"),File(open("temp.png",'rb')))
            os.remove("temp.png")

        resource.data = pokemon_data
    elif endpoint_name == 'ability':
        ability_data = {}

        for e in response_dict['effect_entries']:
            if e['language']['name']=='en':
                ability_data['effect'] = remove_escape_chars(e['effect'])
        
        ability_data['flavor_entries'] = dict()
        for e1 in response_dict["flavor_text_entries"]:
            if e1["language"]["name"]=="en":
                if e1["version_group"]["name"] not in ability_data['flavor_entries'].keys():
                    ability_data['flavor_entries'][e1['version_group']['name']] = []
                desp = remove_escape_chars(e1["flavor_text"])
                ability_data['flavor_entries'][e1['version_group']['name']].append(desp)

        ability_data['pokemons'] = [e['pokemon']['name'] for e in response_dict['pokemon']]

        resource.data = ability_data
    elif endpoint_name == 'version-group':
        generation_url = response_dict["generation"]["url"].split('/')
        version_group_data = {
            'generation': int(generation_url[len(generation_url)-2])
        }
        resource.data = version_group_data
    elif endpoint_name == 'pokedex':
        pokedex_data = {}

        for e in response_dict['descriptions']:
            if e['language']['name']=='en':
                pokedex_data['description'] = remove_escape_chars(e['description'])

        pokedex_data['version-groups'] = []
        for e in response_dict['version_groups']:
            pokedex_data['version-groups'].append(e['name'])

        pokedex_data['pokemons'] = []
        for e in response_dict['pokemon_entries']:
            pokedex_data['pokemons'].append(e['pokemon_species']['name'])

        resource.data = pokedex_data
    elif endpoint_name == 'version':
        version_data = {
            'version-group': response_dict["version_group"]["name"]
        }

        resource.data = version_data
    elif endpoint_name == 'type':
        generation_url = response_dict["generation"]["url"].split("/")
        type_data = {
            'generation': int(generation_url[-2])
        }

        for r in response_dict['damage_relations'].keys():
            type_data[r] = [e['name'] for e in response_dict['damage_relations'][r]]

        type_data['pokemons'] = [e['pokemon']['name'] for e in response_dict['pokemon']]
        type_data['moves'] = [e['name'] for e in response_dict['moves']]

        url_dict = {
            'normal': "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Normal_Type_Icon.svg",
            'fighting': "https://upload.wikimedia.org/wikipedia/commons/b/be/Pok%C3%A9mon_Fighting_Type_Icon.svg",
            'flying': "https://upload.wikimedia.org/wikipedia/commons/e/e0/Pok%C3%A9mon_Flying_Type_Icon.svg",
            'poison': "https://upload.wikimedia.org/wikipedia/commons/c/c4/Pok%C3%A9mon_Poison_Type_Icon.svg",
            'ground': "https://upload.wikimedia.org/wikipedia/commons/8/8d/Pok%C3%A9mon_Ground_Type_Icon.svg",
            'rock': "https://upload.wikimedia.org/wikipedia/commons/b/bb/Pok%C3%A9mon_Rock_Type_Icon.svg",
            'bug': "https://upload.wikimedia.org/wikipedia/commons/3/3c/Pok%C3%A9mon_Bug_Type_Icon.svg",
            'ghost': "https://upload.wikimedia.org/wikipedia/commons/a/a0/Pok%C3%A9mon_Ghost_Type_Icon.svg",
            'steel': "https://upload.wikimedia.org/wikipedia/commons/3/38/Pok%C3%A9mon_Steel_Type_Icon.svg",
            'fire': "https://upload.wikimedia.org/wikipedia/commons/5/56/Pok%C3%A9mon_Fire_Type_Icon.svg",
            'water': "https://upload.wikimedia.org/wikipedia/commons/0/0b/Pok%C3%A9mon_Water_Type_Icon.svg",
            'grass': "https://upload.wikimedia.org/wikipedia/commons/f/f6/Pok%C3%A9mon_Grass_Type_Icon.svg",
            'electric': "https://upload.wikimedia.org/wikipedia/commons/a/a9/Pok%C3%A9mon_Electric_Type_Icon.svg",
            'psychic': "https://upload.wikimedia.org/wikipedia/commons/a/ab/Pok%C3%A9mon_Psychic_Type_Icon.svg",
            'ice': "https://upload.wikimedia.org/wikipedia/commons/8/88/Pok%C3%A9mon_Ice_Type_Icon.svg",
            'dragon': "https://upload.wikimedia.org/wikipedia/commons/a/a6/Pok%C3%A9mon_Dragon_Type_Icon.svg",
            'dark': "https://upload.wikimedia.org/wikipedia/commons/0/09/Pok%C3%A9mon_Dark_Type_Icon.svg",
            'fairy': "https://upload.wikimedia.org/wikipedia/commons/0/08/Pok%C3%A9mon_Fairy_Type_Icon.svg",
        }
        image_url = None
        if resource.name in url_dict.keys():
            image_url = url_dict[resource.name]
        if image_url != None:
            image_response = requests.get(image_url)
            with open("temp.svg",'wb') as f:
                f.write(image_response.content)
            os.remove("static/images/type/"+get_filename(response_dict['name']+".png"))
            resource.image.save(get_filename("type/"+response_dict['name']+".svg"),File(open("temp.svg",'rb')))
            os.remove("temp.svg")

        resource.data = type_data
    elif endpoint_name == 'move':
        generation_url = response_dict["generation"]["url"].split("/")
        move_data = {
            'type': response_dict['type']['name'],
            'generation': int(generation_url[-2])
        }

        for e in response_dict['effect_entries']:
            if e['language']['name']=='en':
                move_data['effect'] = remove_escape_chars(e['effect'])

        if response_dict["damage_class"]!=None:
            move_data['damage_class']=response_dict["damage_class"]["name"]
        else:
            move_data['damage_class']=None

        move_data['pokemons'] = [e['name'] for e in response_dict['learned_by_pokemon']]

        '''Add the stats and other version changes here'''
        move_data['power'] = {'latest': response_dict['power']}
        move_data['accuracy'] = { 'latest': response_dict['accuracy']}
        move_data['pp'] = { 'latest': response_dict['pp']}
        move_data['priority']=response_dict['priority']
        for e in response_dict['past_values']:
            move_data['power'][e['version_group']['name']]=e['power']
            move_data['accuracy'][e['version_group']['name']]=e['accuracy']
            move_data['pp'][e['version_group']['name']]=e['pp']
        resource.data = move_data

    resource.last_updated = timezone.now()
    resource.save()
    return True