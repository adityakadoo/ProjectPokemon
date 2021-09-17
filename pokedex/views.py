from django.http.response import Http404
from django.shortcuts import render, HttpResponse
from django.views import View
from .models import Endpoint,Resource
from datetime import timedelta
from django.utils import timezone
from .api_calls import endpoint_calls, resource_calls

RENEWAL_PERIOD = 180

# Create your views here.
def home(request):
    for endpoint in Endpoint.objects.all():
        now = timezone.now()
        renewal_period = timedelta(days=RENEWAL_PERIOD)
        if endpoint.last_updated + renewal_period < now:
            endpoint_calls.update_endpoint(endpoint)
    response = "<html><body>Hello World</body></html>"
    return HttpResponse(response)

def pokemon(request,name):
    pokemon_endpoint = Endpoint.objects.get(name='pokemon')
    try:
        pokemon = Resource.objects.get(name=name, endpoint=pokemon_endpoint)
    except Resource.DoesNotExist:
        raise Http404
    now = timezone.now()
    renewal_period = timedelta(days=RENEWAL_PERIOD)
    if pokemon.last_updated + renewal_period < now:
        resource_calls.update_pokemon(pokemon)

    response = "<html><body>Hello World "+name+"</body></html>"
    return HttpResponse(response)