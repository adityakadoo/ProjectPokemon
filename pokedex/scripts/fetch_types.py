from pokedex.api_calls import resource_calls
from pokedex.models import Resource, Endpoint

def run(*args):
    type_endpoint = Endpoint.objects.get(name='type')

    for type_resource in Resource.objects.filter(endpoint=type_endpoint):
        if resource_calls.update_resource('type',type_resource):
            print(".",end="")
        else:
            print("![#"+str(type_resource.index)+" "+type_resource.name+"]",end="")