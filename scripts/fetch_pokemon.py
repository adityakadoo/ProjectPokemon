import requests
import os
from requests.api import request
from django.core.files import File
from pokedex.models import Ability, Version, Type, Move, Pokemon, Pokemon_var, Game, Pokedex_entries

def run(*args):
    base_url = "https://pokeapi.co/api/v2/pokemon/"

    i = 1
    max_name = 0
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
        pokemon_temp = Pokemon(index=response_dict["id"],name=response_dict["name"])
        if max_name < len(response_dict["name"]):
            max_name = len(response_dict["name"])
        pokemon_temp.base_experience = response_dict["base_experience"]
        pokemon_temp.height = response_dict["height"]
        pokemon_temp.weight = response_dict["weight"]
        pokemon_temp.species = response_dict["species"]["name"]
        pokemon_temp.hp = response_dict["stats"][0]["base_stat"]
        pokemon_temp.attack = response_dict["stats"][1]["base_stat"]
        pokemon_temp.defense = response_dict["stats"][2]["base_stat"]
        pokemon_temp.sp_attack = response_dict["stats"][3]["base_stat"]
        pokemon_temp.sp_defense = response_dict["stats"][4]["base_stat"]
        pokemon_temp.speed = response_dict["stats"][5]["base_stat"]
        
        image_url = response_dict["sprites"]["other"]["official-artwork"]["front_default"]
        if image_url==None:
            image_url = response_dict["sprites"]["other"]["dream_world"]["front_default"]
        if image_url==None:
            image_url = response_dict["sprites"]["front_default"]
        image_response = requests.get(image_url)
        with open("pokedex/images/temp.png",'wb') as f:
            f.write(image_response.content)
        pokemon_temp.official_artwork.save(response_dict['name']+".png",File(open("pokedex/images/temp.png",'rb')))
        os.remove("pokedex/images/temp.png")        
        # pokemon_temp.save()
        
        for e in response_dict["abilities"]:
            ability_url = e["ability"]["url"].split('/')
            ability_index = int(ability_url[-2])
            ability_temp = Ability.objects.get(index=ability_index)
            pokemon_temp.abilities.add(ability_temp)

        for e in response_dict["types"]:
            type_temp = Type.objects.get(name=e["type"]["name"])
            pokemon_temp.types.add(type_temp)

        i = i+1
    print(max_name)

    i = 1
    max_pokedex_entry = 0
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
        pokemon_temp = Pokemon.objects.get(index=response_dict["id"])

        species_url = response_dict["species"]["url"]
        species_response = requests.get(species_url)
        species_response_dict = species_response.json()

        if i<10000 and species_response_dict["evolves_from_species"]!=None:
            prev_pokemon = Pokemon.objects.filter(species=species_response_dict["evolves_from_species"]["name"])[0]
            pokemon_temp.prev_evolution = prev_pokemon
            pokemon_temp.save()

        generation_url = species_response_dict["generation"]["url"].split('/')
        generation = int(generation_url[-2])
        for e in Version.objects.all():
            if e.generation<generation:
                continue
            pokemon_var_temp = Pokemon_var(version=e,pokemon=pokemon_temp)
            for e1 in Game.objects.filter(version=e):
                for e2 in species_response_dict["flavor_text_entries"]:
                    if e2["language"]["name"]=="en" and e2["version"]["name"]==e1.name:
                        pokemon_var_temp.save()
                        pokedex_entry_temp = Pokedex_entries(game=e1,pokemon_var=pokemon_var_temp)
                        pokedex_entry_temp.entry = e2["flavor_text"]
                        if max_pokedex_entry<len(e2["flavor_text"]):
                            max_pokedex_entry = len(e2["flavor_text"])
                        pokedex_entry_temp.save()

                        for e1 in response_dict["moves"]:
                            for e2 in e1["version_group_details"]:
                                if  e.name == e2["version_group"]["name"]:
                                    move_temp = Move.objects.get(name=e1["move"]["name"])
                                    pokemon_var_temp.moves.add(move_temp)
                    break
        i = i+1
    print(max_pokedex_entry)