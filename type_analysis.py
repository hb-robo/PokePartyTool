import pandas as pd

# import data relevant to the generation
pokeDex = pd.read_csv('data/rby/rby_pokedex.csv', index_col='mon_name')
moveDex = pd.read_csv('data/rby/rby_movedex.csv', index_col='move')
learnDex = pd.read_csv('data/rby/rby_move_access.csv', index_col='mon_name')
types = pd.read_csv('data/gen1types_expanded.csv', index_col='off_type')

typeCounter = {}

for pokemon in list(pokeDex.index):
    if pd.notna(pokeDex.at[pokemon,'second_type']):
        type = "%s_%s" % (pokeDex.at[pokemon,'first_type'],pokeDex.at[pokemon,'second_type'])
    else:
        type = pokeDex.at[pokemon,'first_type']

    if type not in typeCounter.keys():
        typeCounter[type] = 1
    else:
        typeCounter[type] += 1

print("=========OFFENSIVE TYPE ANALYSIS===========")
print("Representing the average offensive value of all typings in the game, \
based on the frequency of their advantages among the total Mon pool, \
accounting only for attacks of the same type as their user, \
assuming all types can do an equal amount of maximum expected damage, \
and that each Mon knows the optimal move for all of its types.")
offTypeMatchups = {}
off_avg_tb = {}

for type in typeCounter.keys():

    offTypeMatchup = {'4.0x':0, '2.0x':0, '1.0x':0, '0.5x':0, '0.25x':0, '0.0x':0}

    multSum = 0.0
    total = 0

    if "_" in type:
        typeslist = type.split("_")
    else:
        typeslist = [type]

    for opptype in typeCounter.keys():
        # OFFENSIVE ANALYSIS
        max_stab = 0
        for t in typeslist:
            stab = types.at[t, 'vs_%s' % opptype]
            if stab > max_stab:
                max_stab = stab
        # print(float(max_stab))
        multSum += max_stab
        total += 1
        max_stab_str = '%sx' % float(format(float(max_stab),'.2f'))
        offTypeMatchup[max_stab_str] += 1

    offTypeMatchups[type] = offTypeMatchup
    off_avg_tb[type] = multSum/total

for tuple in sorted( ((v,k) for k,v in off_avg_tb.items()), reverse=True):
    print('%s: %s' % (tuple[1], tuple[0]))


print("=========DEFENSIVE TYPE ANALYSIS===========")
print("Representing the average defensive value of all typings in the game, \
based on the frequency of their weaknesses among the total Mon pool, \
accounting only for attacks of the same type as their user, \
assuming all types can do an equal amount of maximum expected damage, \
and that each Mon knows the optimal move for all of its types.")
defTypeMatchups = {}
def_avg_tb = {}

for type in typeCounter.keys():

    defTypeMatchup = {'4.0x':0, '2.0x':0, '1.0x':0, '0.5x':0, '0.25x':0, '0.0x':0}

    multSum = 0.0
    total = 0

    for opptype in typeCounter.keys():
        if "_" in opptype:
            opptypes = opptype.split("_")
        else:
            opptypes = [opptype]

        # DEFENSIVE ANALYSIS
        max_stab = 0
        for t in opptypes:
            stab = types.at[t, 'vs_%s' % type]
            if stab > max_stab:
                max_stab = stab

        multSum += max_stab
        total += 1
        max_stab_str = '%sx' % float(format(float(max_stab),'.2f'))
        defTypeMatchup[max_stab_str] += 1

    defTypeMatchups[type] = defTypeMatchup
    def_avg_tb[type] = multSum/total

for tuple in sorted( ((v,k) for k,v in def_avg_tb.items()), reverse=False):
    print('%s: %s' % (tuple[1], tuple[0]))

print("=========NET TYPE ANALYSIS===========")
print("Representing the average net value of all typings in the game, \
based on the frequency of their weaknesses and advantages among the total Mon pool, \
accounting only for attacks of the same type as their user, \
assuming all types can do an equal amount of maximum expected damage, \
and that each Mon knows the optimal move for all of its types.")
net_avg_tb = {}
for type in typeCounter.keys():
    net_avg_tb[type] = off_avg_tb[type] - def_avg_tb[type]

for tuple in sorted( ((v,k) for k,v in net_avg_tb.items()), reverse=True):
    print('%s: %s' % (tuple[1], tuple[0]))

print("=========TYPE EXPECTED MAXIMUM DAMAGE===========")
print("Representing the maximum expected damage across all attacks of a given type.")

type_max_dmg = {
    'normal': 150,
    'fire': 153,
    'water': 144,
    'grass': 105,
    'electric': 142,
    'ice': 162,
    'psychic': 150,
    'bug': 75,
    'fighting': 114,
    'flying': 120,
    'poison': 97,
    'ground': 150,
    'rock': 101,
    'ghost': 30,
    'dragon': 40
}

for tuple in sorted( ((v,k) for k,v in type_max_dmg.items()), reverse=True):
    print('%s: %s' % (tuple[1], tuple[0]))


print("=========ADJ. OFF TYPE ANALYSIS===========")
print("Representing the average offensive value of all typings in the game, \
based on the frequency of their advantages among the total Mon pool, \
accounting only for attacks of the same type as their user, \
adjusted for differences in maximum expected damage from each type, \
assuming each Mon knows the optimal move for all of its types.")

off_avg_tb = {}

for type in typeCounter.keys():

    multSum = 0.0
    total = 0

    if "_" in type:
        typeslist = type.split("_")
    else:
        typeslist = [type]

    for opptype in typeCounter.keys():
        max_stab = 0
        for t in typeslist:
            stab = types.at[t, 'vs_%s' % opptype]
            adj_stab = stab * type_max_dmg[t]
            if adj_stab > max_stab:
                max_stab = adj_stab
        multSum += max_stab
        total += 1

    off_avg_tb[type] = multSum/total

for tuple in sorted( ((v,k) for k,v in off_avg_tb.items()), reverse=True):
    print('%s: %s' % (tuple[1], tuple[0]))

print("=========ADJ. DEF TYPE ANALYSIS===========")
print("Representing the average defensive value of all typings in the game, \
based on the frequency of their weaknesses among the total Mon pool, \
accounting only for attacks of the same type as their user, \
adjusted for differences in maximum expected damage from each type, \
and assuming each Mon knows the optimal move for all of its types.")
def_avg_tb = {}

for type in typeCounter.keys():

    multSum = 0.0
    total = 0

    for opptype in typeCounter.keys():
        if "_" in opptype:
            opptypes = opptype.split("_")
        else:
            opptypes = [opptype]

        # DEFENSIVE ANALYSIS
        max_stab = 0
        for t in opptypes:
            stab = types.at[t, 'vs_%s' % type]
            adj_stab = stab * type_max_dmg[t]
            if adj_stab > max_stab:
                max_stab = adj_stab

        multSum += max_stab
        total += 1

    def_avg_tb[type] = multSum/total

for tuple in sorted( ((v,k) for k,v in def_avg_tb.items()), reverse=False):
    print('%s: %s' % (tuple[1], tuple[0]))

print("=========ADJ. NET TYPE ANALYSIS===========")
print("Representing the average adjust net value of all typings in the game, \
based on the frequency of their weaknesses and advantages among the total Mon pool, \
accounting only for attacks of the same type as their user, \
adjusted for differences in maximum expected damage from each type, \
and assuming each Mon knows the optimal move for all of its types.")
net_adj_tb = {}
for type in typeCounter.keys():
    net_adj_tb[type] = off_avg_tb[type] - def_avg_tb[type]

for tuple in sorted( ((v,k) for k,v in net_adj_tb.items()), reverse=True):
    print('%s: %s' % (tuple[1], tuple[0]))