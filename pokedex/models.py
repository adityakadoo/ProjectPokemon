from django.db import models
from django.db.models.aggregates import Max
from django.db.models.base import Model
from django.db.models.fields import CharField

# Create your models here.

class Version(models.Model):
    """Models a pokemon game version"""
    index = models.IntegerField(null=True)
    name = models.CharField(max_length=50,null=True)
    generation = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class Game(models.Model):
    index = models.IntegerField(null=True)
    name = models.CharField(max_length=50,null=True)
    version = models.ForeignKey(Version,on_delete=models.CASCADE)

    def __str__(self):
        return self.name.title()

class Ability(models.Model):
    """Models a pokemon ability"""
    index = models.IntegerField(null=True)
    name = models.CharField(max_length=30,null=True)
    effect = models.CharField(max_length=2000,null=True)
    versions = models.ManyToManyField(Version, through='Ability_var')

    def __str__(self):
        return self.name.title()

class Ability_var(models.Model):
    """Models the variations of a pokemon ablility between different versions"""
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE,null=True)
    version = models.ForeignKey(Version, on_delete=models.CASCADE,null=True)
    description = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.ability.name.title()+"(ver.: "+self.version.name+")"

class Type(models.Model):
    """The different families of Pokemons"""
    index=models.IntegerField(null=True)
    name=models.CharField(max_length=30,null=True)
    super_eff_against=models.ManyToManyField('self',related_name='super_eff_from')
    half_damage_against=models.ManyToManyField('self',related_name='half_damage_from',symmetrical=False)
    ineff_against=models.ManyToManyField('self',related_name='ineff_from',symmetrical=False)
    color=models.CharField(max_length=10,null=True)
    versions=models.ManyToManyField(Version,through='Type_var')

    def __str__(self):
        return self.name.upper()

class Type_var(models.Model):
    """Just to link things unique to their own variations"""
    type=models.ForeignKey(Type, on_delete=models.CASCADE,null=True)
    version=models.ForeignKey(Version,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.type.name.upper()+"(ver.: "+self.version.name+")"

class Damage_class(models.Model):
    """to refer the 3 types of damage class"""
    index=models.IntegerField(null=True)
    name=models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.name

class Move(models.Model):
    """Different moves performed by a Pokemon"""
    index=models.IntegerField(null=True)
    name=models.CharField(max_length=50,null=True)
    info=models.TextField(null=True)
    damage_class=models.ForeignKey(Damage_class,on_delete=models.CASCADE,null=True)
    versions=models.ManyToManyField(Version,through='Move_var')

    def __str__(self):
        return self.name.title()

class Move_var(models.Model):
    """Linking moves with its versions"""
    description=models.CharField(max_length=2000,null=True)
    power=models.IntegerField(null=True)
    accuracy=models.IntegerField(null=True)
    pp=models.IntegerField(null=True)
    priority=models.IntegerField(null=True)
    move=models.ForeignKey(Move,on_delete=models.CASCADE,null=True)
    type=models.ForeignKey(Type,on_delete=models.CASCADE,null=True)
    version=models.ForeignKey(Version,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.move.name.title()+"(ver.: "+self.version.name+")"

class Pokemon(models.Model):
    """Models a pokemon"""
    index = models.IntegerField(null=True)
    name = models.CharField(max_length=50,null=True)
    base_experience = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    species = models.CharField(max_length=50,null=True)
    official_artwork = models.ImageField(upload_to = f"pokedex/images/",null=True)
    #stats
    hp = models.IntegerField(null=True)
    attack = models.IntegerField(null=True)
    defense = models.IntegerField(null=True)
    sp_attack = models.IntegerField(null=True)
    sp_defense = models.IntegerField(null=True)
    speed = models.IntegerField(null=True)
    #linked data
    abilities = models.ManyToManyField(Ability)
    versions = models.ManyToManyField(Version, through='Pokemon_var')
    prev_evolution = models.ForeignKey('self',null=True,related_name="evolutions",on_delete=models.CASCADE)
    types = models.ManyToManyField(Type)

    def __str__(self):
        return self.name.title()

class Pokemon_var(models.Model):
    """Models the variations in a pokemon between different versions"""
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE,null=True)
    version = models.ForeignKey(Version, on_delete=models.CASCADE,null=True)
    moves = models.ManyToManyField(Move)
    game_entries = models.ManyToManyField(Game,through='Pokedex_entries')

    def __str__(self):
        return self.pokemon.name.title()+"(ver.: "+self.version.name+")"

class Pokedex_entries(models.Model):
    """Models the connection between Pokemon_var and Game to store pokedex entries"""
    pokemon_var = models.ForeignKey(Pokemon_var,null=True,on_delete=models.CASCADE)
    game = models.ForeignKey(Game,null=True,on_delete=models.CASCADE)
    entry = models.CharField(max_length=1000,null=True)

class Pokedex(models.Model):
    index = models.IntegerField(null=True)
    name = models.CharField(max_length=30,null=True)
    pokemon_entries = models.ManyToManyField(Pokemon)
    versions = models.ManyToManyField(Version)

    def __str__(self):
        return self.name
        