from pokedex.api_calls import resource_calls
from pokedex.models import Resource, Endpoint

def run(*args):
    pokemon_endpoint = Endpoint.objects.get(name='pokemon')

    for pokemon_resource in Resource.objects.filter(endpoint=pokemon_endpoint):
        if resource_calls.update_resource('pokemon',pokemon_resource):
            print(".",end="")
        else:
            print("![#"+str(pokemon_resource.index)+" "+pokemon_resource.name+"]",end="")