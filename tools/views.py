from os import stat
from django.shortcuts import render
from pokedex.models import Resource, Endpoint
from tools.models import Cluster
import json

# Create your views here.
def get_home(request):
    data = {
        'resources' : [],
        'filters': {
            'pokedexes' : [],
            'types' : [],
            'endpoints' : []
        }
    }
    endpoint = Endpoint.objects.get(name='pokemon')
    stats_raw = {
        'hp' : [],
        'attack' : [],
        'defense' : [],
        'sp_attack' : [],
        'sp_defense' : [],
        'speed' : [],
    }
    ids = []
    for resource in Resource.objects.filter(endpoint=endpoint).order_by('index'):
        temp = {
            'name': resource.name,
            'index': resource.index,
            'endpoint': endpoint.name,
            'data' : {
                'types' : resource.data['types'],
            },
            'imageURL' : resource.image.url
        }
        for key in stats_raw.keys():
            stats_raw[key].append(resource.data[key])
            temp['data'][key] = resource.data[key]
        ids.append(resource.name)
        data['resources'].append(temp)
    
    for c in Cluster.objects.all():
        data['filters']['pokedexes'].append({
            'name': c.name,
            'category': "Cluster",
            'pokemons' : c.elements,
            'version-groups' : []
        })

    context = {'context_str': json.dumps(data)}
    return render(request,'tools/index.html',context)