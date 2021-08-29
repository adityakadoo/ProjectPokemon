from django.db.models import base
import requests
from pokedex.models import Type
from pokedex.models import Version
from pokedex.models import Type_var

def run(*args):
    base_url = "https://pokeapi.co/api/v2/type/"

    i = 1
    while True:
        url = base_url+str(i)
        response = requests.get(url)
        
        if response.status_code!=200:
            if i<=10000:
                i=10001
                continue
            else:
                break

        response_dict = response.json()
        type_temp = Type(index=response_dict["id"],name=response_dict["name"])
        type_temp.save()
        i+=1
        
    i = 1 
    while True:
        url = base_url+str(i)
        response = requests.get(url)

        if response.status_code!=200:
            if i<=10000:
                i=10001
                continue
            else:
                break
        
        response_dict = response.json()
        type_temp2=Type.objects.get(index=response_dict["id"])

        """Linking the self related objects to each other"""        
        for e in response_dict["damage_relations"]["double_damage_to"]:
            temp3=Type.objects.filter(name=e["name"])
            type_temp2.super_eff_against.add(temp3[0])
            
        for e in response_dict["damage_relations"]["half_damage_to"]:
            temp3=Type.objects.filter(name=e["name"])
            type_temp2.half_damage_against.add(temp3[0])
        
        for e in response_dict["damage_relations"]["no_damage_to"]:
            temp3=Type.objects.filter(name=e["name"])
            type_temp2.ineff_against.add(temp3[0])
        
        generation_url = response_dict["generation"]["url"].split("/")
        generation = int(generation_url[-2])
        for e in Version.objects.all():
            Type_var_temp = Type_var(version=e,type=type_temp2)
            if e.generation<generation:
                continue
            Type_var_temp.save()
        i+=1