from django.urls import path

from . import views

app_name = 'pokedex'
urlpatterns = [
    # Home page
    path('', views.home, name='index'),
    # Pokemon detail view page
    path('<slug:endpoint_name>/<slug:resource_name>', views.get_resource, name='resource'),
]