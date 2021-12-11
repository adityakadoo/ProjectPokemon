from django.http.response import Http404
from django.shortcuts import render, HttpResponse
from .models import Endpoint,Resource
from datetime import timedelta
from django.utils import timezone
from .api_calls import endpoint_calls, resource_calls

RENEWAL_PERIOD = -180

# Create your views here.
def home(request):
    context = {
        'endpoints' : [],
        'resources' : dict()
    }
    for endpoint in Endpoint.objects.all():
        now = timezone.now()
        renewal_period = timedelta(days=RENEWAL_PERIOD)
        if endpoint.last_updated + renewal_period < now:
            endpoint_calls.update_endpoint(endpoint)
        context['endpoints'].append(endpoint)
        context['resources'][endpoint.name] = []
        count = 0
        for resource in Resource.objects.filter(endpoint=endpoint).order_by('index'):
            context['resources'][endpoint.name].append(resource)
            count += 1
            if count>10:
                break
    return render(request,'pokedex/index.html',context)

def get_resource(request,endpoint_name,resource_name):
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
        resource_calls.update_resource(endpoint,resource)

    response = "<html><body>Hello World "+str(resource)+"</body></html>"
    return HttpResponse(response)