import pandas as pd
import csv
import numpy as np

# open basic typing .csv and convert to dictionary
types = pd.read_csv('data/types/gen6-8types.csv')
types = types.set_index('off_type')

full_dex = pd.read_csv('data/types/pkmn.help type coverage.csv')
full_dex = full_dex.set_index('Name')

## OPTION 1: expand dictionary to include dual-typings
# alltypes = types.copy()

# for type1 in types:
#     for type2 in types:
#         if type1 == type2:
#             continue

#         newcol = "vs_%s_%s" % (type1.replace('vs_', ''), type2.replace('vs_', ''))

#         if newcol not in alltypes.columns:
#             alltypes[newcol] = ""

#         for index, row in alltypes.iterrows():
#             print(index)
#             alltypes.at[index, newcol] = float(alltypes.at[index, type1]) * float(alltypes.at[index, type2])

## OPTION 2: iterate over typings and make some calculations

# best hypothetical offensive mon

class Type:
    def __init__(self, type1, type2, avg_off_mult, avg_def_mult, avg_net, exists=True):
        self.type1 = type1
        self.type2 = type2
        self.avg_off_mult = avg_off_mult
        self.avg_def_mult = avg_def_mult
        self.avg_net = avg_net
        self.exists = exists


results = []

for type1 in types:
    for type2 in types:

        type1 = type1.replace('vs_', '')
        type2 = type2.replace('vs_', '')
        if type2 == type1:
            type2 = ''

        off_tot = 0
        def_tot = 0

        for j, opp in full_dex.iterrows():

            max_off = 0
            min_def = 0

            for mtype in [ type1, type2 ]:
                for opptype in [ opp['Type 1'], opp['Type 2'] ]:

                    if mtype == '' or opptype != opptype:
                        continue

                    off_m = float(types.at[mtype.lower(), "vs_%s" % opptype.lower()])
                    if off_m > max_off:
                        max_off = off_m

                    def_m = float(types.at[opptype.lower(), "vs_%s" % mtype.lower()])
                    if def_m > min_def:
                        min_def = def_m

            off_tot += max_off
            def_tot += min_def

        avg_off_mult = off_tot / full_dex.shape[0]
        avg_def_mult = def_tot / full_dex.shape[0]
        avg_net = avg_off_mult - avg_def_mult

        if type2 == '':
            exists = full_dex[( (full_dex['Type 1'] == type1.capitalize()) & (full_dex['Type 2'] != full_dex['Type 2']) )].shape[0] > 0
        else:
            exists = full_dex[( (full_dex['Type 1'] == type1.capitalize()) & (full_dex['Type 2'] == type2.capitalize()) )].shape[0] > 0

        results.append( Type( type1.capitalize(), type2.capitalize(), avg_off_mult, avg_def_mult, avg_net, exists) )

df = pd.DataFrame([o.__dict__ for o in results])
print(df)
df.to_csv('all_types_vs_gen9dex.csv')


# offtypes = {}
# deftypes = {}

# # select attacker
# for offtype1 in types:
#     for offtype2 in types:

#         offtype1 = offtype1.replace('vs_', '')
#         offtype2 = offtype2.replace('vs_', '')

#         #  to prevent taking non-existent mons into the equation
#         if full_dex[(full_dex['Type 1'] == offtype1.capitalize() & full_dex['Type 2'] == offtype2.capitalize())].shape[0] < 1:
#             continue

#         if offtype1 == offtype2:
#             offtype = offtype1
#         else:
#             offtype = "%s_%s" % (offtype1, offtype2)

#         offtypes[offtype] = {}

#         # select defender
#         for deftype1 in types:
#             for deftype2 in types:

#                 if full_dex[(full_dex['Type 1'] == deftype1.capitalize() & full_dex['Type 2'] == deftype2.capitalize())].shape[0] < 1:
#                     continue

#                 if deftype1 == deftype2:
#                     deftype = deftype1.replace('vs_', '')
#                     stab1 = float(types.at[offtype1, deftype1])
#                     stab2 = float(types.at[offtype2, deftype1])
#                 else:
#                     deftype = "%s_%s" % (deftype1.replace('vs_', ''), deftype2.replace('vs_', ''))                
#                     stab1 = float(types.at[offtype1, deftype1]) * float(types.at[offtype1, deftype2])
#                     stab2 = float(types.at[offtype2, deftype1]) * float(types.at[offtype2, deftype2])

#                 if deftype not in deftypes.keys():
#                     deftypes[deftype] = {}

#                 max_stab = max(stab1, stab2)
#                 offtypes[offtype][deftype] = max_stab
#                 deftypes[deftype][offtype] = max_stab

# nettypes = {}


# # for type in sorted(offtypes.keys()):
# #     for opptype in sorted(offtypes.keys()):

# #         off_res = offtypes[type][opptype]
# #         def_res = deftypes[type][opptype]

# #         if off_res == 4 and def_res == 0:
# #             net_res = 'perfect_win'
# #         elif off_res == 0 and def_res == 4:
# #             net_res = 'perfect_loss'
# #         elif off_res > 1 and def_res < 1:
# #             net_res = 'hard_win'
# #         elif off_res < 1 and def_res > 1:
# #             net_res = 'hard_loss'
# #         elif (off_res > 1 and def_res == 1) or (off_res == 1 and def_res < 1) or (off_res == 4 and def_res == 2) or (off_res == 0.5 and def_res == 0.25):
# #             net_res = 'soft_win'
# #         elif (def_res == 1 and off_res < 1) or (def_res > 1 and off_res == 1) or (def_res == 4 and off_res == 2) or (def_res == 0.5 and off_res == 0.25):
# #             net_res = 'soft_loss'
# #         elif off_res == def_res:
# #             net_res = 'trade'


# #         if opptype not in nettypes.keys():
# #             nettypes[opptype] = {}

# #         nettypes[opptype][type] = net_res


# df = pd.DataFrame.from_dict(nettypes)

# df.to_csv('nettypes_gens6-9.csv')


