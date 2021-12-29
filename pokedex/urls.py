from django.urls import path

from . import views

app_name = 'pokedex'
urlpatterns = [
    # Home page
    path('', views.get_home, name='home'),
    # Pokemon detail view page
    path('pokemon/<slug:name>', views.get_pokemon, name='pokemon'),
    # Move detail view page
    path('move/<slug:name>', views.get_move, name='move'),
    # Type detail view page
    path('type/<slug:name>', views.get_type, name='type'),
    # Ability detail view page
    path('ability/<slug:name>', views.get_ability, name='ability'),
]