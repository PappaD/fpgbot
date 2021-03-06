#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from peewee import *
from datetime import datetime, timedelta

db = SqliteDatabase('users.db')

class BaseModel(Model):
    class Meta:
        database = db
        
class User(BaseModel):
    id = IntegerField(primary_key=True)
    latitude = FloatField()
    longitude = FloatField()
    active = BooleanField()
    normal_distance = IntegerField(default=200)
    alert_distance = IntegerField(default=0)
    lastupdated = DateTimeField(null = True)
    
class UserPokemons(BaseModel):
    user = ForeignKeyField(User)
    pokemon = CharField()
    
    
class Encounter(BaseModel):
    encounter = CharField()
    expires = DateTimeField()

db.connect()

for tbl in [User, UserPokemons, Encounter]:
    if not tbl.table_exists():
        db.create_tables([tbl])

def user_exists(id):
    try:
        u = User.get(User.id == id)
        return True
    except User.DoesNotExist:
        return False
            
def get_user(id):
    user = User.select().where(User.id == id).get()
    return user            

def get_active_users():
    user = User.select().where(User.active == True)
    return user 

def get_or_create_user(id, defaults):
    u, created = User.get_or_create(id=id, defaults=defaults)
    u.save()

    return u, created

def get_user_pokemons(id):
    return UserPokemons.select().join(User).where(User.id == id)    

def get_or_create_userpokemons(user, pokemon):
    up, created = UserPokemons.get_or_create(user = user, pokemon = pokemon) 
    up.save()

    return up, created

def delete_userpokemons(user, pokemon):
    query = UserPokemons.delete().where(UserPokemons.user == user, UserPokemons.pokemon == pokemon)
    return query.execute()         

def delete_all_userpokemons(user):
    query = UserPokemons.delete().where(UserPokemons.user == user)
    return query.execute()   

def garbage_collect():
    c = Encounter.select().where(Encounter.expires < datetime.now()).count()
    t = Encounter.select().count()

    query = Encounter.delete().where(Encounter.expires < (datetime.now()-timedelta(hours = 1)))
    query.execute()
    return c, t           

def get_all_users():
    return User.select().where(User.active == True)     

def get_or_create_encounters(encounter, expires):
    ue, created = Encounter.get_or_create(encounter = encounter, expires = expires)    
    ue.save()

    return ue, created

def check_user_pokemon_whitelist(user, pokemon):
    try:
        up = UserPokemons.get(UserPokemons.user == user, UserPokemons.pokemon == pokemon)
        return False
    except UserPokemons.DoesNotExist:
        return True

def check_user_pokemon_blacklist(user, pokemon):
    return not check_user_pokemon_whitelist(user, pokemon)