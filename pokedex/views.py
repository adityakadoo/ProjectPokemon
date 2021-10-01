from django.http.response import Http404
from django.shortcuts import render, HttpResponse
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