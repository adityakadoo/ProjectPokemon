from pokedex.api_calls import resource_calls
from pokedex.models import Resource, Endpoint

def run(*args):
    ability_endpoint = Endpoint.objects.get(name='ability')

    for ability_resource in Resource.objects.filter(endpoint=ability_endpoint):
        if resource_calls.update_resource('ability',ability_resource):
            print(".",end="")
        else:
            print("![#"+str(ability_resource.index)+" "+ability_resource.name+"]",end="")