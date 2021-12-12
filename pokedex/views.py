from django.http.response import Http404, HttpResponseNotModified
from django.shortcuts import render, HttpResponse
from .models import Endpoint,Resource
from datetime import timedelta
from django.utils import timezone
from .api_calls import endpoint_calls, resource_calls
import json

RENEWAL_PERIOD = 180

def get_home(request):
    data = {
        'endpoints' : [],
        'resources' : dict()
    }
    for endpoint in Endpoint.objects.all():
        now = timezone.now()
        renewal_period = timedelta(days=RENEWAL_PERIOD)
        if endpoint.last_updated + renewal_period < now:
            endpoint_calls.update_endpoint(endpoint)
        data['endpoints'].append(str(endpoint))
        data['resources'][endpoint.name] = []
        count = 0
        for resource in Resource.objects.filter(endpoint=endpoint).order_by('index'):
            data['resources'][endpoint.name].append(str(resource))
            count += 1
            if count>10:
                break
    context = {'context_str' : json.dumps(data)}
    return render(request,'pokedex/index.html',context)

def get_resource(endpoint_name,resource_index):
    try:
        endpoint = Endpoint.objects.get(name=endpoint_name)
    except Endpoint.DoesNotExist:
        raise Http404
    try:
        resource = Resource.objects.get(index=resource_index, endpoint=endpoint)
    except Resource.DoesNotExist:
        raise Http404
    now = timezone.now()
    renewal_period = timedelta(days=RENEWAL_PERIOD)
    if resource.last_updated + renewal_period < now:
        resource_calls.update_resource(endpoint_name,resource)
    return resource

def get_pokemon(request,index):
    pokemon = get_resource('pokemon', index)
    data = {
        'name' : pokemon.name,
        'index' : pokemon.index
    }
    context = {'context_str' : json.dumps(data)}
    return render(request,'pokedex/pokemon.html',context)

def get_move(request,index):
    move = get_resource('move', index)
    response = "<html><body>Hello "+str(move.name)+"</body></html>"
    return HttpResponse(response)

def get_type(request,index):
    type = get_resource('type', index)
    response = "<html><body>Hello "+str(type.name)+"</body></html>"
    return HttpResponse(response)

def get_ability(request,index):
    ability = get_resource('ability', index)
    response = "<html><body>Hello "+str(ability.name)+"</body></html>"
    return HttpResponse(response)