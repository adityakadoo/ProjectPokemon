from django.http.response import Http404, HttpResponseNotModified
from django.shortcuts import render, HttpResponse
from .models import Endpoint,Resource
from datetime import timedelta
from django.utils import timezone
from .api_calls import endpoint_calls, resource_calls
import json

RENEWAL_PERIOD = 180

def fixed_name(s):
    return s.replace('-',' ')

def get_home(request):
    data = {
        'resources' : [],
        'filters': {
            'pokedexes' : [],
            'types' : [],
            'endpoints' : ['pokemon', 'move', 'type', 'ability']
        }
    }
    for endpoint in Endpoint.objects.all():
        now = timezone.now()
        renewal_period = timedelta(days=RENEWAL_PERIOD)
        if endpoint.last_updated + renewal_period < now:
            endpoint_calls.update_endpoint(endpoint)
    
    for resource in Resource.objects.exclude(
            endpoint__name='pokedex').exclude(
            endpoint__name='version-group').exclude(
            endpoint__name='version').order_by("?"):
        endpoint = resource.endpoint
        temp = {
            'name': resource.name,
            'index': resource.index,
            'endpoint': endpoint.name,
            'data' : None
        }
        if endpoint.name == 'pokemon':
            if resource.data != None:
                temp['data'] = {
                    'types' : resource.data['types'],
                }
            temp['imageURL'] = resource.image.url
        elif endpoint.name == 'move':
            if resource.data != None:
                temp['data'] = {
                    'type' : resource.data['type'],
                    'power' : resource.data['power']['latest'],
                    'accuracy' : resource.data['accuracy']['latest'],
                    'damage_class' : resource.data['damage_class']
                }
        data['resources'].append(temp)
        
    for resource in Resource.objects.filter(endpoint__name='pokedex'):
        data['filters']['pokedexes'].append({
            'name': fixed_name(resource.name),
            'pokemons' : resource.data['pokemons'],
            'version-groups' : resource.data['version-groups']
        })
    
    for resource in Resource.objects.filter(endpoint__name='type'):
        data['filters']['types'].append(resource.name)
    
    context = {'context_str' : json.dumps(data)}
    return render(request,'pokedex/index.html',context)

def get_resource(endpoint_name,resource_name):
    try:
        endpoint = Endpoint.objects.get(name=endpoint_name)
    except Endpoint.DoesNotExist:
        raise Http404
    try:
        resource = Resource.objects.get(name=resource_name, endpoint=endpoint)
    except Resource.DoesNotExist:
        raise Http404
    now = timezone.now()
    renewal_period = timedelta(days=RENEWAL_PERIOD)
    if resource.last_updated + renewal_period < now:
        resource_calls.update_resource(endpoint_name,resource)
    return resource

def get_pokemon(request,name):
    pokemon = get_resource('pokemon', name)
    data = {
        'name' : pokemon.name,
        'index' : pokemon.index
    }
    context = {'context_str' : json.dumps(data)}
    return render(request,'pokedex/pokemon.html',context)

def get_move(request,name):
    move = get_resource('move', name)
    response = "<html><body>Hello "+str(move.name)+"</body></html>"
    return HttpResponse(response)

def get_type(request,name):
    type = get_resource('type', name)
    response = "<html><body>Hello "+str(type.name)+"</body></html>"
    return HttpResponse(response)

def get_ability(request,name):
    ability = get_resource('ability', name)
    response = "<html><body>Hello "+str(ability.name)+"</body></html>"
    return HttpResponse(response)