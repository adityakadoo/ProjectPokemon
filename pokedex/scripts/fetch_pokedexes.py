from pokedex.api_calls import resource_calls
from pokedex.models import Resource, Endpoint

def run(*args):
    pokedex_endpoint = Endpoint.objects.get(name='pokedex')

    for pokedex_resource in Resource.objects.filter(endpoint=pokedex_endpoint):
        if resource_calls.update_resource('pokedex',pokedex_resource):
            print(".",end="")
        else:
            print("![#"+str(pokedex_resource.index)+" "+pokedex_resource.name+"]",end="")