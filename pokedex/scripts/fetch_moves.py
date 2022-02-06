from pokedex.api_calls import resource_calls
from pokedex.models import Resource, Endpoint

def run(*args):
    move_endpoint = Endpoint.objects.get(name='move')

    for move_resource in Resource.objects.filter(endpoint=move_endpoint):
        if resource_calls.update_resource('move',move_resource):
            print(".",end="")
        else:
            print("![#"+str(move_resource.index)+" "+move_resource.name+"]",end="")