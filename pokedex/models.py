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

class Ability(models.Model):
    """Models a pokemon ability"""
    index = models.IntegerField(null=True)
    name = models.CharField(max_length=50,null=True)
    effect = models.CharField(max_length=2000,null=True)
    versions = models.ManyToManyField(Version, through='Ability_var',null=True)

    def __str__(self):
        return self.name.title()

class Ability_var(models.Model):
    """Models the variations of a pokemon ablility between different versions"""
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE,null=True)
    version = models.ForeignKey(Version, on_delete=models.CASCADE,null=True)
    description = models.CharField(max_length=500,null=True)
    is_present = models.BooleanField(null=True)

class Type(models.Model):
    """The different families of Pokemons"""
    index=models.IntegerField(null=True)
    name=models.CharField(max_length=30,null=True)
    super_eff_against=models.ManyToManyField('self',null=True)
    half_damage_against=models.ManyToManyField('self',null=True)
    ineff_against=models.ManyToManyField('self',null=True)
    color=models.CharField(max_length=10,null=True)
    versions=models.ManyToManyField(Version,through='Type_var',null=True)

    def __str__(self):
        return self.name.upper()

class Type_var(models.Model):
    """Just to link things unique to their own variations"""
    type=models.ForeignKey(Type, on_delete=models.CASCADE,null=True)
    is_present=models.BooleanField(default=False,null=True)
    version=models.ForeignKey(Version,on_delete=models.CASCADE,null=True)

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
    versions=models.ManyToManyField(Version,through='Move_var',null=True)

    def __str__(self):
        return self.name.title()

class Move_var(models.Model):
    """Linking moves with its versions"""
    description=models.CharField(max_length=2000,null=True)
    is_present=models.BooleanField(default=False)
    power=models.IntegerField(null=True)
    accuracy=models.IntegerField(null=True)
    pp=models.IntegerField(null=True)
    priority=models.IntegerField(null=True)
    move=models.ForeignKey(Move,on_delete=models.CASCADE,null=True)
    type=models.ForeignKey(Type,on_delete=models.CASCADE,null=True)
    version=models.ForeignKey(Version,on_delete=models.CASCADE,null=True)