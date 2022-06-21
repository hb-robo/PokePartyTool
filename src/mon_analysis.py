from http.client import NOT_IMPLEMENTED
import utils.classes as g1
import pandas as pd
import os

cur_path = os.path.dirname(__file__)
new_path = os.path.relpath('..\\data\\')


# import data relevant to the generation
pokeDex = pd.read_csv('../data/rby/rby_pokedex.csv', index_col='mon_name')
moveDex = pd.read_csv('../data/rby/rby_movedex.csv', index_col='move')
learnDex = pd.read_csv('../data/rby/rby_move_access.csv', index_col='mon_name')
types = pd.read_csv('../data/gen1types_expanded.csv', index_col='off_type')

LEVEL = 50
MOVELIST = 'full'
NOTIMPLEMENTED = ['counter','ko','random','reflect','trap','suicide']
results = pd.DataFrame(columns=[
                                'avg_phys_off', 'avg_spec_off', 'avg_off',
                                'avg_phys_def', 'avg_spec_off', 'avg_def'
                                ])

for pokemon, row in pokeDex.iterrows():

    physOffTotal = 0
    specOffTotal = 0
    offTotal = 0
    physDefTotal = 0
    specDefTotal = 0
    defTotal = 0

    for opponent, row2 in pokeDex.iterrows():

        mon = g1.Gen1Mon(pokemon, 50)
        opp = g1.Gen1Mon(opponent, 50)
        b = g1.Gen1Battle(mon, opp)

        physOffMax = 0
        specOffMax = 0
        offMax = 0
        physDefMax = 0
        specDefMax = 0
        defMax = 0

        for move in list(moveDex.index.values):
            # OFFENSIVE ANALYSIS
            if moveDex.at[move,'category'] == 'attack' and moveDex.at[move,'subcat'] not in NOTIMPLEMENTED and pd.notna(learnDex.at[pokemon,move]):
                # PHYSICAL OFFENSE
                if moveDex.at[move,'type'] in b.PHYSTYPES:
                    dmg = b.processMove(mon, move, opp, expected=True)
                    if dmg > physOffMax:
                        physOffMax = dmg
                    if dmg > offMax:
                        offMax = dmg
                # SPECIAL OFFENSE
                elif moveDex.at[move,'type'] in b.SPECTYPES:
                    dmg = b.processMove(mon, move, opp, expected=True)
                    if dmg > specOffMax:
                        specOffMax = dmg
                    if dmg > offMax:
                        offMax = dmg
            # DEFENSIVE ANALYSIS
            if moveDex.at[move,'category'] == 'attack' and moveDex.at[move,'subcat'] not in NOTIMPLEMENTED  and pd.notna(learnDex.at[opponent,move]):
                # PHYSICAL DEFENSE
                if moveDex.at[move,'type'] in b.PHYSTYPES:
                    dmg = b.processMove(opp, move, mon, expected=True)
                    if dmg > physDefMax:
                        physDefMax = dmg
                    if dmg > defMax:
                        defMax = dmg
                # SPECIAL DEFENSE
                elif moveDex.at[move,'type'] in b.SPECTYPES:
                    dmg = b.processMove(opp, move, mon, expected=True)
                    if dmg > specDefMax:
                        specDefMax = dmg
                    if dmg > defMax:
                        defMax = dmg

        physOffTotal += (physOffMax / opp.stats['hp'])
        specOffTotal += (specOffMax / opp.stats['hp'])
        offTotal += (offMax / opp.stats['hp'])
        physDefTotal += (physDefMax / mon.stats['hp'])
        specDefTotal += (specDefMax / mon.stats['hp'])
        defTotal += (defMax / opp.stats['hp'])


    physOffAvg = physOffTotal / 151
    specOffAvg = specOffTotal / 151
    offAvg = offTotal / 151
    physDefAvg = physDefTotal / 151
    specDefAvg = specDefTotal / 151
    defAvg = defTotal / 151

    results.loc[pokemon] = [physOffAvg, specOffAvg, offAvg, physDefAvg, specDefAvg, defAvg]
    print('finished processing %s' % pokemon)


results.to_csv('../data/results/Mon Analysis - LVL%s, %s Moveset.csv' % (LEVEL, MOVELIST))