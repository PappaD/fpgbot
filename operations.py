import settings

def find_pokemon(name):
    r = []
    for pokemon in settings.pokemons:
       if name.lower() in settings.pokemons[pokemon].lower():
            r.append(pokemon) 

    return r
            