

token = '28xxxxx12:AAHxxxxxxxxxxxxxxxxxxxxxxxxxxxqEE' 

url = 'http://localhost:5000/next_loc?lat=%f&lon=%f'
garbage_collect = 300

pokemons = { 'BULBASAUR': 'Bulbasaur', 
    'IVYSAUR': 'Ivysaur', 
    'VENUSAUR': 'Venusaur', 
    'CHARMANDER': 'Charmander', 
    'CHARMELEON': 'Charmeleon', 
    'CHARIZARD': 'Charizard', 
    'SQUIRTLE': 'Squirtle', 
    'WARTORTLE': 'Wartortle', 
    'BLASTOISE': 'Blastoise', 
    'CATERPIE': 'Caterpie', 
    'METAPOD': 'Metapod', 
    'BUTTERFREE': 'Butterfree', 
    'WEEDLE': 'Weedle', 
    'KAKUNA': 'Kakuna', 
    'BEEDRILL': 'Beedrill', 
    'PIDGEY': 'Pidgey', 
    'PIDGEOTTO': 'Pidgeotto', 
    'PIDGEOT': 'Pidgeot', 
    'RATTATA': 'Rattata', 
    'RATICATE': 'Raticate', 
    'SPEAROW': 'Spearow', 
    'FEAROW': 'Fearow', 
    'EKANS': 'Ekans', 
    'ARBOK': 'Arbok', 
    'PIKACHU': 'Pikachu', 
    'RAICHU': 'Raichu', 
    'SANDSHREW': 'Sandshrew', 
    'SANDSLASH': 'Sandslash', 
    'NIDORAN_FEMALE': 'NidoranF', 
    'NIDORINA': 'Nidorina', 
    'NIDOQUEEN': 'Nidoqueen', 
    'NIDORAN_MALE': 'NidoranM', 
    'NIDORINO': 'Nidorino', 
    'NIDOKING': 'Nidoking', 
    'CLEFAIRY': 'Clefairy', 
    'CLEFABLE': 'Clefable', 
    'VULPIX': 'Vulpix', 
    'NINETALES': 'Ninetales', 
    'JIGGLYPUFF': 'Jigglypuff', 
    'WIGGLYTUFF': 'Wigglytuff', 
    'ZUBAT': 'Zubat', 
    'GOLBAT': 'Golbat', 
    'ODDISH': 'Oddish', 
    'GLOOM': 'Gloom', 
    'VILEPLUME': 'Vileplume', 
    'PARAS': 'Paras', 
    'PARASECT': 'Parasect', 
    'VENONAT': 'Venonat', 
    'VENOMOTH': 'Venomoth', 
    'DIGLETT': 'Diglett', 
    'DUGTRIO': 'Dugtrio', 
    'MEOWTH': 'Meowth', 
    'PERSIAN': 'Persian', 
    'PSYDUCK': 'Psyduck', 
    'GOLDUCK': 'Golduck', 
    'MANKEY': 'Mankey', 
    'PRIMEAPE': 'Primeape', 
    'GROWLITHE': 'Growlithe', 
    'ARCANINE': 'Arcanine', 
    'POLIWAG': 'Poliwag', 
    'POLIWHIRL': 'Poliwhirl', 
    'POLIWRATH': 'Poliwrath', 
    'ABRA': 'Abra', 
    'KADABRA': 'Kadabra', 
    'ALAKAZAM': 'Alakazam', 
    'MACHOP': 'Machop', 
    'MACHOKE': 'Machoke', 
    'MACHAMP': 'Machamp', 
    'BELLSPROUT': 'Bellsprout', 
    'WEEPINBELL': 'Weepinbell', 
    'VICTREEBEL': 'Victreebel', 
    'TENTACOOL': 'Tentacool', 
    'TENTACRUEL': 'Tentacruel', 
    'GEODUDE': 'Geodude', 
    'GRAVELER': 'Graveler', 
    'GOLEM': 'Golem', 
    'PONYTA': 'Ponyta', 
    'RAPIDASH': 'Rapidash', 
    'SLOWPOKE': 'Slowpoke', 
    'SLOWBRO': 'Slowbro', 
    'MAGNEMITE': 'Magnemite', 
    'MAGNETON': 'Magneton', 
    'FARFETCHD': 'Farfetch\d', 
    'DODUO': 'Doduo', 
    'DODRIO': 'Dodrio', 
    'SEEL': 'Seel', 
    'DEWGONG': 'Dewgong', 
    'GRIMER': 'Grimer', 
    'MUK': 'Muk', 
    'SHELLDER': 'Shellder', 
    'CLOYSTER': 'Cloyster', 
    'GASTLY': 'Gastly', 
    'HAUNTER': 'Haunter', 
    'GENGAR': 'Gengar', 
    'ONIX': 'Onix', 
    'DROWZEE': 'Drowzee', 
    'HYPNO': 'Hypno', 
    'KRABBY': 'Krabby', 
    'KINGLER': 'Kingler', 
    'VOLTORB': 'Voltorb', 
    'ELECTRODE': 'Electrode', 
    'EXEGGCUTE': 'Exeggcute', 
    'EXEGGUTOR': 'Exeggutor', 
    'CUBONE': 'Cubone', 
    'MAROWAK': 'Marowak', 
    'HITMONLEE': 'Hitmonlee', 
    'HITMONCHAN': 'Hitmonchan', 
    'LICKITUNG': 'Lickitung', 
    'KOFFING': 'Koffing', 
    'WEEZING': 'Weezing', 
    'RHYHORN': 'Rhyhorn', 
    'RHYDON': 'Rhydon', 
    'CHANSEY': 'Chansey', 
    'TANGELA': 'Tangela', 
    'KANGASKHAN': 'Kangaskhan', 
    'HORSEA': 'Horsea', 
    'SEADRA': 'Seadra', 
    'GOLDEEN': 'Goldeen', 
    'SEAKING': 'Seaking', 
    'STARYU': 'Staryu', 
    'STARMIE': 'Starmie', 
    'MR_MIME': 'Mr.Mime', 
    'SCYTHER': 'Scyther', 
    'JYNX': 'Jynx', 
    'ELECTABUZZ': 'Electabuzz', 
    'MAGMAR': 'Magmar', 
    'PINSIR': 'Pinsir', 
    'TAUROS': 'Tauros', 
    'MAGIKARP': 'Magikarp', 
    'GYARADOS': 'Gyarados', 
    'LAPRAS': 'Lapras', 
    'DITTO': 'Ditto', 
    'EEVEE': 'Eevee', 
    'VAPOREON': 'Vaporeon', 
    'JOLTEON': 'Jolteon', 
    'FLAREON': 'Flareon', 
    'PORYGON': 'Porygon', 
    'OMANYTE': 'Omanyte', 
    'OMASTAR': 'Omastar', 
    'KABUTO': 'Kabuto', 
    'KABUTOPS': 'Kabutops', 
    'AERODACTYL': 'Aerodactyl', 
    'SNORLAX': 'Snorlax', 
    'ARTICUNO': 'Articuno', 
    'ZAPDOS': 'Zapdos', 
    'MOLTRES': 'Moltres', 
    'DRATINI': 'Dratini', 
    'DRAGONAIR': 'Dragonair', 
    'DRAGONITE': 'Dragonite', 
    'MEWTWO': 'Mewtwo', 
    'MEW': 'Mew'
 }
 
pokemon_id = {
    1: 'BULBASAUR', 
    2: 'IVYSAUR', 
    3: 'VENUSAUR', 
    4: 'CHARMANDER', 
    5: 'CHARMELEON', 
    6: 'CHARIZARD', 
    7: 'SQUIRTLE', 
    8: 'WARTORTLE', 
    9: 'BLASTOISE', 
    10: 'CATERPIE', 
    11: 'METAPOD', 
    12: 'BUTTERFREE', 
    13: 'WEEDLE', 
    14: 'KAKUNA', 
    15: 'BEEDRILL', 
    16: 'PIDGEY', 
    17: 'PIDGEOTTO', 
    18: 'PIDGEOT', 
    19: 'RATTATA', 
    20: 'RATICATE', 
    21: 'SPEAROW', 
    22: 'FEAROW', 
    23: 'EKANS', 
    24: 'ARBOK', 
    25: 'PIKACHU', 
    26: 'RAICHU', 
    27: 'SANDSHREW', 
    28: 'SANDSLASH', 
    29: 'NIDORAN_FEMALE', 
    30: 'NIDORINA', 
    31: 'NIDOQUEEN', 
    32: 'NIDORAN_MALE', 
    33: 'NIDORINO', 
    34: 'NIDOKING', 
    35: 'CLEFAIRY', 
    36: 'CLEFABLE', 
    37: 'VULPIX', 
    38: 'NINETALES', 
    39: 'JIGGLYPUFF', 
    40: 'WIGGLYTUFF', 
    41: 'ZUBAT', 
    42: 'GOLBAT', 
    43: 'ODDISH', 
    44: 'GLOOM', 
    45: 'VILEPLUME', 
    46: 'PARAS', 
    47: 'PARASECT', 
    48: 'VENONAT', 
    49: 'VENOMOTH', 
    50: 'DIGLETT', 
    51: 'DUGTRIO', 
    52: 'MEOWTH', 
    53: 'PERSIAN', 
    54: 'PSYDUCK', 
    55: 'GOLDUCK', 
    56: 'MANKEY', 
    57: 'PRIMEAPE', 
    58: 'GROWLITHE', 
    59: 'ARCANINE', 
    60: 'POLIWAG', 
    61: 'POLIWHIRL', 
    62: 'POLIWRATH', 
    63: 'ABRA', 
    64: 'KADABRA', 
    65: 'ALAKAZAM', 
    66: 'MACHOP', 
    67: 'MACHOKE', 
    68: 'MACHAMP', 
    69: 'BELLSPROUT', 
    70: 'WEEPINBELL', 
    71: 'VICTREEBEL', 
    72: 'TENTACOOL', 
    73: 'TENTACRUEL', 
    74: 'GEODUDE', 
    75: 'GRAVELER', 
    76: 'GOLEM', 
    77: 'PONYTA', 
    78: 'RAPIDASH', 
    79: 'SLOWPOKE', 
    80: 'SLOWBRO', 
    81: 'MAGNEMITE', 
    82: 'MAGNETON', 
    83: 'FARFETCHD', 
    84: 'DODUO', 
    85: 'DODRIO', 
    86: 'SEEL', 
    87: 'DEWGONG', 
    88: 'GRIMER', 
    89: 'MUK', 
    90: 'SHELLDER', 
    91: 'CLOYSTER', 
    92: 'GASTLY', 
    93: 'HAUNTER', 
    94: 'GENGAR', 
    95: 'ONIX', 
    96: 'DROWZEE', 
    97: 'HYPNO', 
    98: 'KRABBY', 
    99: 'KINGLER', 
    100: 'VOLTORB', 
    101: 'ELECTRODE', 
    102: 'EXEGGCUTE', 
    103: 'EXEGGUTOR', 
    104: 'CUBONE', 
    105: 'MAROWAK', 
    106: 'HITMONLEE', 
    107: 'HITMONCHAN', 
    108: 'LICKITUNG', 
    109: 'KOFFING', 
    110: 'WEEZING', 
    111: 'RHYHORN', 
    112: 'RHYDON', 
    113: 'CHANSEY', 
    114: 'TANGELA', 
    115: 'KANGASKHAN', 
    116: 'HORSEA', 
    117: 'SEADRA', 
    118: 'GOLDEEN', 
    119: 'SEAKING', 
    120: 'STARYU', 
    121: 'STARMIE', 
    122: 'MR_MIME', 
    123: 'SCYTHER', 
    124: 'JYNX', 
    125: 'ELECTABUZZ', 
    126: 'MAGMAR', 
    127: 'PINSIR', 
    128: 'TAUROS', 
    129: 'MAGIKARP', 
    130: 'GYARADOS', 
    131: 'LAPRAS', 
    132: 'DITTO', 
    133: 'EEVEE', 
    134: 'VAPOREON', 
    135: 'JOLTEON', 
    136: 'FLAREON', 
    137: 'PORYGON', 
    138: 'OMANYTE', 
    139: 'OMASTAR', 
    140: 'KABUTO', 
    141: 'KABUTOPS', 
    142: 'AERODACTYL', 
    143: 'SNORLAX', 
    144: 'ARTICUNO', 
    145: 'ZAPDOS', 
    146: 'MOLTRES', 
    147: 'DRATINI', 
    148: 'DRAGONAIR', 
    149: 'DRAGONITE', 
    150: 'MEWTWO', 
    151: 'MEW'
}

ignore_default = {
    'CATERPIE', 
    'METAPOD', 
    'BUTTERFREE', 
    'WEEDLE', 
    'KAKUNA', 
    'BEEDRILL', 
    'PIDGEY', 
    'PIDGEOTTO', 
    'PIDGEOT', 
    'RATTATA', 
    'RATICATE', 
    'SPEAROW', 
    'FEAROW', 
    'EKANS', 
    'ARBOK', 
    'SANDSHREW', 
    'SANDSLASH', 
    'NIDORAN_FEMALE', 
    'NIDORINA', 
    'NIDOQUEEN', 
    'NIDORAN_MALE', 
    'NIDORINO', 
    'NIDOKING', 
    'CLEFAIRY', 
    'CLEFABLE', 
    'JIGGLYPUFF', 
    'WIGGLYTUFF', 
    'ZUBAT', 
    'GOLBAT', 
    'PARAS', 
    'PARASECT', 
    'VENONAT', 
    'VENOMOTH', 
    'DIGLETT', 
    'DUGTRIO', 
    'MEOWTH', 
    'PERSIAN', 
    'PSYDUCK', 
    'GOLDUCK', 
    'MANKEY', 
    'PRIMEAPE', 
    'POLIWAG', 
    'POLIWHIRL', 
    'POLIWRATH', 
    'MACHOP', 
    'MACHOKE', 
    'MACHAMP', 
    'TENTACOOL', 
    'TENTACRUEL', 
    'GEODUDE', 
    'GRAVELER', 
    'GOLEM', 
    'PONYTA', 
    'RAPIDASH', 
    'SLOWPOKE', 
    'SLOWBRO', 
    'MAGNEMITE', 
    'MAGNETON', 
    'DODUO', 
    'DODRIO', 
    'SEEL', 
    'DEWGONG', 
    'SHELLDER', 
    'CLOYSTER', 
    'GASTLY', 
    'HAUNTER', 
    'GENGAR', 
    'DROWZEE', 
    'HYPNO', 
    'KRABBY', 
    'KINGLER', 
    'VOLTORB', 
    'ELECTRODE', 
    'KOFFING', 
    'WEEZING', 
    'RHYHORN', 
    'RHYDON', 
    'CHANSEY', 
    'HORSEA', 
    'SEADRA', 
    'GOLDEEN', 
    'SEAKING', 
    'STARYU', 
    'STARMIE', 
    'MAGIKARP'
}
