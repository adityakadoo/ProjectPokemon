from pokedex.api_calls import resource_calls
from pokedex.models import Resource, Endpoint

def run(*args):
    version_endpoint = Endpoint.objects.get(name='version')

    for version_resource in Resource.objects.filter(endpoint=version_endpoint):
        if resource_calls.update_resource('version',version_resource):
            print(".",end="")
        else:
            print("![#"+str(version_resource.index)+" "+version_resource.name+"]",end="")