from django.shortcuts import render, HttpResponse
from .models import Endpoint,Resource
from datetime import timedelta
from django.utils import timezone
import requests

# Create your views here.
def update_endpoint(endpoint):
    response = requests.get("https://pokeapi.co/api/v2/"+str(endpoint.name)+"?limit=1000000")
    if response.status_code != 200:
        return False
    response_dict = response.json()
    for i in range(endpoint.count,response_dict['count']):
        new_resource,is_new = Resource.objects.get_or_create(name=response_dict["results"][i]["name"],index=i+1)
        new_resource.endpoint = endpoint
        new_resource.last_updated = timezone.now()
        new_resource.save()
    endpoint.count = response_dict['count']
    endpoint.save()
    return True

def home(request):
    for endpoint in Endpoint.objects.all():
        now = timezone.now()
        renewal_period = timedelta(days=-1)
        if endpoint.last_updated + renewal_period < now:
            update_endpoint(endpoint)
    response = "<html><body>Hello World</body></html>"
    return HttpResponse(response)