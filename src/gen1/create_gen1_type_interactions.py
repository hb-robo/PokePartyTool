"""
One-time script to turn "type charts" into simple tables for SQL analysis.
"""

import pandas as pd
from src.gen1.gen1_constants import TYPES

gen1types = pd.read_csv('data/gen1/csv/gen1_type_chart.csv')
gen1types = gen1types.set_index('off_type')


type_interactions = []
for ptype, row in gen1types.iterrows():
    for key, value in dict(row).items():
        type_interactions.append({
            'off_type': ptype.capitalize(),
            'def_type': key[3:].capitalize(),
            'multiplier': value
        })

# print(type_interactions)
df = pd.DataFrame(type_interactions)
# print(df)
# df.to_csv('data/gen1/csv/gen1_type_interactions.csv')

# expand defensive typings
expanded_type_interactions = []
for ptype in TYPES:
    for deftype1 in TYPES:
        def1val = df.loc[
            (df['off_type'] == ptype)
            & (df['def_type'] == deftype1)
        ]
        def1mult = float(def1val['multiplier'])
        expanded_type_interactions.append({
            'off_type': ptype,
            'def_type1': deftype1,
            'def_type2': None,
            'multiplier': def1mult
        })

        for deftype2 in TYPES:
            if deftype1 == deftype2:
                continue
            def2val = df.loc[
                (df['off_type'] == ptype)
                & (df['def_type'] == deftype2)
            ]
            def2mult = float(def2val['multiplier'])
            expanded_type_interactions.append({
                'off_type': ptype,
                'def_type1': deftype1,
                'def_type2': deftype2,
                'multiplier': def1mult * def2mult
            })

df2 = pd.DataFrame(expanded_type_interactions)
print(df2)
# df2.to_csv('data/gen1/csv/gen1_expanded_type_interactions.csv')


# remove redundant pairs (e.g. Fire/Fighting, Fighting/Fire)
def sorted_type_triple(row):
    if row['def_type2'] is None:
        deftypepair = [row['def_type1']]
    else:
        deftypepair = [row['def_type1'], row['def_type2']]
        deftypepair.sort()
    deftypestr = "".join(str(s) for s in deftypepair)
    return f"{row['off_type']}vs{deftypestr}"


df2['sorted_type_pairs'] = df2.apply(sorted_type_triple, axis=1)
print(df2.duplicated(subset=['sorted_type_pairs']))

df2_deduplicated = df2[~df2.duplicated(subset=['sorted_type_pairs'])]
print(df2_deduplicated)
df2_deduplicated.to_csv('data/gen1/csv/gen1_expanded_type_interactions.csv')
