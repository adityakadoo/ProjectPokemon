from django.urls import path

from . import views

app_name = 'pokedex'
urlpatterns = [
    # Home page
    path('', views.home, name='index'),
    # Pokemon detail view page
    path('pokemon/<slug:name>', views.pokemon, name='pokemon'),
]