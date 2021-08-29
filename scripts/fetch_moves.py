from django.db.models import base
import requests
from requests.models import Response
from pokedex.models import Damage_class, Move
from pokedex.models import Version
from pokedex.models import Move_var
from pokedex.models import Type

def run(*args):
    base_url = "https://pokeapi.co/api/v2/move-damage-class/"


    base_url = "https://pokeapi.co/api/v2/move/"
    i=1
    while True:
        url=base_url+str(i)
        response=requests.get(url)
        
        if response.status_code!=200:
            if i<=10000:
                i=10001
                continue
            else:
                break
        response_dict = response.json()
        move_temp = Move(index=response_dict["id"],name=response_dict["name"])
        for e in response_dict["effect_entries"]:
            if e["language"]["name"]=="en":
                move_temp.info=e["effect"]
        #this above entry needs to be removed.
        move_temp.save()
        
        """Doing the Linking work"""
        # move_temp2=Move.objects.get()
        if response_dict["damage_class"]!=None:
            damage_class_url=response_dict["damage_class"]["url"].split("/")
            damage_class_index=int(damage_class_url[-2])
            damage_class_name=response_dict["damage_class"]["name"]
            # print(damage_class_name)
            # print(damage_class_index)
            # break
            damage_class_temp,created = Damage_class.objects.get_or_create(index=damage_class_index,name=damage_class_name)
            move_temp.damage_class = damage_class_temp

        generation_url = response_dict["generation"]["url"].split("/")
        generation = int(generation_url[-2])
        for e in Version.objects.all():
            move_var_temp = Move_var(version=e,move=move_temp)
            if e.generation<generation:
                continue
            move_var_temp.power=response_dict["power"]
            move_var_temp.accuracy=response_dict["accuracy"]
            move_var_temp.pp=response_dict["pp"]
            move_var_temp.priority=response_dict["priority"]

            """Adding the type of the pokemon in different versions"""
            type_name_for_now=response_dict["type"]["name"]
            new_temp=Type.objects.get(name=type_name_for_now)
            

            for e1 in response_dict["past_values"]:
                pos_url=e1["version_group"]["url"].split("/")
                pos=int(pos_url[-2])
                if pos<e.index:
                    if e1["accuracy"]!=None:
                        move_var_temp.accuracy=e1["accuracy"]
                    if e1["power"]!=None:
                        move_var_temp.power=e1["power"]
                    if e1["pp"]!=None:
                        move_var_temp.pp=e1["pp"]
                    # if e1["priority"]!=None:
                    #     move_var_temp.priority=e1["priority"]
                    if e1["type"]!=None:
                        new_type_name=e1["type"]["name"]
                        new_temp=Type.objects.get(name=new_type_name)

            """Linking the type as we have a final say on it"""
            move_var_temp.type=new_temp           
                        
            for e2 in response_dict["flavor_text_entries"]:
                if e2["language"]["name"]=="en" and e2["version_group"]["name"]==e.name:
                    move_var_temp.description=e2["flavor_text"]
            move_var_temp.save()
        i+=1

