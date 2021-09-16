from django.contrib import admin
from .models import Endpoint, Resource

# Register your models here.
admin.site.register(Endpoint)
admin.site.register(Resource)