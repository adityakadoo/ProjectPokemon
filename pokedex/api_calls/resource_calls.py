import requests

def update_pokemon(pokemon):
    response = requests.get("https://pokeapi.co/api/v2/pokemon/"+str(pokemon.name))
    if response.status_code != 200:
        return False
    response_dict = response.json()
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
            pokemon_data['pokedex_entries'][e['version']['name']]=e['flavor_text']

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
    
    pokemon.data = pokemon_data
    pokemon.save()
    return True