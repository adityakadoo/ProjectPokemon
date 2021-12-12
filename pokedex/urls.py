from django.urls import path

from . import views

app_name = 'pokedex'
urlpatterns = [
    # Home page
    path('', views.get_home, name='home'),
    # Pokemon detail view page
    path('pokemon/<int:index>', views.get_pokemon, name='pokemon'),
    # Move detail view page
    path('move/<int:index>', views.get_move, name='move'),
    # Type detail view page
    path('type/<int:index>', views.get_type, name='type'),
    # Ability detail view page
    path('ability/<int:index>', views.get_ability, name='ability'),
]