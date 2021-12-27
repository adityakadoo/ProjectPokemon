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
    }
    for endpoint in Endpoint.objects.all():
        now = timezone.now()
        renewal_period = timedelta(days=RENEWAL_PERIOD)
        if endpoint.last_updated + renewal_period < now:
            endpoint_calls.update_endpoint(endpoint)
    # count = 0
    for resource in Resource.objects.order_by("?"):
        endpoint = resource.endpoint
        temp = {
            'name': fixed_name(resource.name),
            'index': resource.index,
            'endpoint': fixed_name(endpoint.name),
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
        # count += 1
        # if count>=50:
        #     break
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