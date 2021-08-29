from pokedex.models import Version
from django.contrib import admin
from .models import Ability, Ability_var, Damage_class, Game, Move, Move_var, Pokedex, Pokedex_entries, Pokemon, Pokemon_var, Type, Type_var, Version

# Register your models here.
admin.site.register(Version)
admin.site.register(Ability)
admin.site.register(Ability_var)
admin.site.register(Type)
admin.site.register(Type_var)
admin.site.register(Damage_class)
admin.site.register(Move)
admin.site.register(Move_var)
admin.site.register(Pokemon)
admin.site.register(Pokemon_var)
admin.site.register(Pokedex)
admin.site.register(Game)
admin.site.register(Pokedex_entries)