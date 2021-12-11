from pokedex.models import Resource
from django.utils import timezone
from django.core.files import File
import requests

def get_filename(s):
    return s.replace('-','_')

def update_endpoint(endpoint):
    response = requests.get("https://pokeapi.co/api/v2/"+str(endpoint.name)+"?limit=1000000")
    if response.status_code != 200:
        return False
    response_dict = response.json()
    for i in range(endpoint.count,response_dict['count']):
        new_resource,is_new = Resource.objects.get_or_create(name=response_dict["results"][i]["name"],index=i+1)
        new_resource.endpoint = endpoint
        new_resource.last_updated = timezone.now()
        new_resource.image.save(get_filename(endpoint.name+"/"+response_dict['results'][i]['name']+".png"),File(open("static/images/default.png",'rb')))
        new_resource.save()
    endpoint.count = response_dict['count']
    endpoint.save()
    return True