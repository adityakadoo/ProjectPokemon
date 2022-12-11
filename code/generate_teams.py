import requests
import asyncio
import aiohttp
import json
import random
from queue import Queue
import numpy as np
from pprint import pprint

def get_from_api(url):
    response = requests.api.get(f"{url}")
    if(response.status_code != 200):
        print(f"{url} : {response.status_code}")
        raise KeyError()
    return json.loads(response.content)


async def get_from_api_bulk(url, session):
    try:
        async with session.get(url=url) as response:
            resp = await response.read()
            return json.loads(resp)
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))

async def gets_from_api(urls):
    async with aiohttp.ClientSession() as session:
        res = await asyncio.gather(*[get_from_api_bulk(url, session) for url in urls])
    return res

def stat_total(pokemon):
    return sum(stat['base_stat'] for stat in pokemon['stats'])

def get_types(pokemon, generation):
    past_types = pokemon['past_types']
    past_types.sort(key=lambda x: x['generation']['url'].split("/")[-2])
    for past_type in past_types:
        if generation <= past_type['generation']['url'].split("/")[-2]:
            return [type_['type']['name'] for type_ in past_type['types']]
    return [type_['type']['name'] for type_ in pokemon['types']]

async def main():
    versions = get_from_api("https://pokeapi.co/api/v2/version-group?limit=100")['results']
    
    for index, version in enumerate(versions):
        print(f"{index+1} : {version['name']}")
    version_id = int(input("Select one pokedex : "))-1
    
    version = get_from_api(versions[version_id]['url'])

    generation = version['generation']['url'].split("/")[-2]

    pokedexes = [get_from_api(pokedex['url']) for pokedex in version['pokedexes']]
    pokedex_names = [pokedex['name'] for pokedex in pokedexes]

    pokedex_inverted = dict()
    for pokedex in pokedexes:
        for entry in pokedex['pokemon_entries']:
            pokedex_inverted[entry['pokemon_species']['name']] = entry['entry_number']
        entries = [entry['pokemon_species'] for entry in pokedex['pokemon_entries']]
    all_species = await gets_from_api([entry['url'] for entry in entries])
    
    chain_urls = set()
    for specie in all_species:
        if not (specie['is_legendary'] or specie['is_mythical']):
            chain_urls.add(specie['evolution_chain']['url'])
    chains = await gets_from_api(chain_urls)
    
    filtered_urls = set()
    queue = Queue(0)
    for chain in chains:
        queue.put(chain['chain'])
        while not queue.empty():
            top = queue.get()
            if len(top['evolves_to']) == 0:
                filtered_urls.add(top['species']['url'])
            else:
                for child in top['evolves_to']:
                    if child['evolution_details'][0]['trigger']['name'] == 'trade':
                        continue
                    queue.put(child)
    filtered_species = await gets_from_api(filtered_urls)

    pokemon_urls = set()
    for specie in filtered_species:
        exists = False
        for pokedex_number in specie['pokedex_numbers']:
            if pokedex_number['pokedex']['name'] in pokedex_names:
                exists = True
        if exists and not (specie['is_legendary'] or specie['is_mythical']):
            for variety in specie['varieties']:
                if variety['is_default']:
                    pokemon_urls.add(variety['pokemon']['url'])
    pokemons = await gets_from_api(pokemon_urls)

    pokemons.sort(key=lambda x:pokedex_inverted[x['species']['name']])

    # for index, pokemon in enumerate(pokemons):
    #     print(f"{index+1} : {pokemon['name'].capitalize()}")
    # starter_id = int(input("Select starter pokemon : "))-1

    teams = [[0], [1], [2]]
    stats = [sum([stat_total(pokemons[id_]) for id_ in ids]) for ids in teams]
    while len(teams)>0:
        if(len(teams[0]) == 6):
            break
        new_teams = []
        new_stats = []
        for i, team in enumerate(teams):
            used_types = set()
            for member_id in team:
                for type_ in get_types(pokemons[member_id], generation):
                    used_types.add(type_)
            for index, pokemon in enumerate(pokemons):
                found = False if (len(get_types(pokemon, generation))==2) and (len(team)<=1 or index>max((2,team[-1]))) else True
                for type_ in get_types(pokemon, generation):
                    if type_ in used_types:
                        found = True
                if found:
                    continue
                new_stats.append(stats[i]+stat_total(pokemon))
                new_teams.append(teams[i]+[index])
        teams = new_teams
        stats = new_stats

    sort_order = np.argsort(np.array(stats))

    for index in sort_order[-10:]:
        print(f"team {index+1} :\t\t{stats[index]/6:.2f}")
        for member_id in teams[index]:
            print(f"{pokemons[member_id]['name']} [{']['.join([type_.upper()[:3] for type_ in get_types(pokemons[member_id], generation)])}]\t: {stat_total(pokemons[member_id])}")
        print("*"*40)

if __name__=="__main__":
    asyncio.run(main())

