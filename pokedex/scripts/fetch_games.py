from pokedex.api_calls import resource_calls
from pokedex.models import Resource, Endpoint

def run(*args):
    game_endpoint = Endpoint.objects.get(name='version-group')

    for game_resource in Resource.objects.filter(endpoint=game_endpoint):
        if resource_calls.update_resource('version-group',game_resource):
            print(".",end="")
        else:
            print("![#"+str(game_resource.index)+" "+game_resource.name+"]",end="")