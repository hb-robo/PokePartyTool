import pandas as pd

RBY = 1
GSC = 0
RSE = 0
COL = 0
FRLG = 0
XD = 0
DPP = 0
HGSS = 0
BW = 0
B2W2 = 0
XY = 0
ORAS = 0
SM = 0
USUM = 0
LGPLGE = 0
SS = 0
SSIA = 0
BDSP = 0

spectypes = ['fire', 'water', 'grass', 'electric', 'ice', 'psychic', 'dragon']
phystypes = ['normal', 'fighting', 'flying', 'poison', 'rock', 'ground', 'bug', 'ghost']

# import the gen1 type spread chart
df = pd.read_csv('data/gens2-5types_expanded.csv')
df = df.set_index('off_type')

# naively ranks best defensive types
#print(df.mean().sort_values())
# naively ranks best offensive types
#print(df.mean(axis=1).sort_values())

# generate list of existing type combinations in gen1
monDB = pd.read_csv('data/gsc/gsc_mons.csv')
typelist = []
typecounts = {}
for index, row in monDB.iterrows():
    # print(row)
    montype = ""
    if pd.isna(row['second_type']):
        montype = ("vs_%s" % (row['first_type']))
    else:
        montype = ("vs_%s_%s" % (row['first_type'], row['second_type']))

    if montype not in typelist:
        typelist.append(montype)

    if montype in typecounts:
        typecounts[montype] += 1
    else:
        typecounts[montype] = 1
# print(typelist)
# print(typecounts)

df2 = df[typelist]
# ranks best defensive types based on equal Gen 1 type spread
# print(df2.mean().sort_values())
# ranks best offensive types based on equal Gen 1 type spread
# print(df2.mean(axis=1).sort_values(ascending=False))

# generate "true" STAB offensive results for Gen 1
# offense_results = {}
# for index, row in df.iterrows():
#     off_score = 0
#     for deftype in typecounts:
#         off_score += row[deftype] * typecounts[deftype]
#     offense_results[index] = off_score / 151
# for x in sorted(offense_results.items(), key=lambda x: x[1], reverse=True):
#     print("%s - %f" % (x[0], x[1]))

# generate "true" STAB defensive results for Gen 1
# defense_results = {}
# for index, row in df.transpose().iterrows():
#     if index not in typecounts:
#         continue
#     def_score = 0
#     for index2, mon in monDB.iterrows():
#         best_damage = 0
#         if mon['first_stab']:
#             best_damage = row[mon['first_type']]
#         if pd.notna(mon['second_type']) and mon['second_stab'] == 1:
#             if row[mon['second_type']] > best_damage:
#                 best_damage = row[mon['second_type']]
#         def_score += best_damage
#     defense_results[index] = def_score / 151
# for x in sorted(defense_results.items(), key=lambda x: x[1]):
#     print("%s - %f" % (x[0], x[1]))

# generate all pokemon 1v1 matchups in gen 1

off_matchups = {}
def_matchups = {}

md = pd.read_csv('data/gsc/gsc_movedex_natural.csv')
md = md.drop('index', axis=1).set_index('mon_name')
print(md)

for index, mon in monDB.iterrows():

    off_matchups[mon['mon_name']] = {}
    def_matchups[mon['mon_name']] = {}
    montype = ""

    if pd.isnull(mon['second_type']):
        montype = "vs_%s" % (mon['first_type'])
    else:
        montype = "vs_%s_%s" % (mon['first_type'], mon['second_type'])

    for index2, vs_mon in monDB.iterrows():

        if pd.isnull(vs_mon['second_type']):
            opptype = "vs_%s" % (vs_mon['first_type'])
        else:
            opptype = "vs_%s_%s" % (vs_mon['first_type'], vs_mon['second_type'])

        # offensive matchup
        off_matchup = 0
        def_matchup = 0

        for column in md:
            attstat = 'sp att' if column in spectypes else 'attack'
            defstat = 'sp def' if attstat == 'sp att' else 'defense'

            move = md.at[mon['mon_name'], column]
            if pd.notnull(move):
                stab = 1
                if mon['first_type'] == column or mon['second_type'] == column:
                    stab = 1.5

                curr_dmg = (20*move*(mon[attstat]/vs_mon[defstat])/50 + 2)*stab*df2.at[column, opptype] / vs_mon['hp']
                if curr_dmg > off_matchup:
                    off_matchup = curr_dmg

            opp_move = md.at[vs_mon['mon_name'], column]
            if pd.notnull(opp_move):
                opp_stab = 1
                if vs_mon['first_type'] == column or vs_mon['second_type'] == column:
                    opp_stab = 1.5

                opp_dmg = (20*opp_move*(vs_mon[attstat]/mon[defstat])/50 + 2)*opp_stab*df2.at[column,montype] / mon['hp']
                if opp_dmg > def_matchup:
                    def_matchup = opp_dmg

        off_matchups[mon['mon_name']]["vs_%s" % (vs_mon['mon_name'])] = off_matchup
        def_matchups[mon['mon_name']]["vs_%s" % (vs_mon['mon_name'])] = def_matchup

# print(off_matchups)
# print(def_matchups)

offmons = pd.DataFrame.from_dict(off_matchups)
offmons = offmons.transpose()
offmons['off_avg'] = offmons.mean(numeric_only=True, axis=1)
defmons = pd.DataFrame.from_dict(def_matchups)
defmons = defmons.transpose()


scores = offmons
scores['def_avg'] = defmons.mean(numeric_only=True, axis=1)
scores = scores.iloc[:, -2:]
scores['ovr'] = (scores['off_avg']-1) + (1-scores['def_avg'])

scores.to_csv('gen2scores_natural.csv')