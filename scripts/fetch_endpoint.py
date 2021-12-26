from pokedex.api_calls import endpoint_calls
from pokedex.models import Endpoint
from django.utils import timezone

def run(*args):
    endpoint_names = ['pokemon', 'type', 'move', 'ability', 'version', 'version-group', 'pokedex']
    
    for endpoint_name in endpoint_names:
        endpoint, created = Endpoint.objects.get_or_create(name=endpoint_name)
        if created:
            endpoint.count = 0
        endpoint.last_updated = timezone.now()
        if endpoint_calls.update_endpoint(endpoint):
            print(endpoint_name+" endpoint updated!")
        else:
            print(endpoint_name+" endpoint not updated.")