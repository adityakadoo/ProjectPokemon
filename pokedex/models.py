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

class Ability(models.Model):
    """Models a pokemon ability"""
    index = models.IntegerField(null=True)
    name = models.CharField(max_length=50,null=True)
    effect = models.CharField(max_length=2000,null=True)
    versions = models.ManyToManyField(Version, through='Ability_var',null=True)

class Ability_var(models.Model):
    """Models the variations of a pokemon ablility between different versions"""
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE,null=True)
    version = models.ForeignKey(Version, on_delete=models.CASCADE,null=True)
    description = models.CharField(max_length=500,null=True)
    is_present = models.BooleanField(null=True)