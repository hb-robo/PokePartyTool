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
types = pd.read_csv('../data/types/gen1types_expanded.csv', index_col='off_type')

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

        # OFFENSIVE ANALYSIS
        physOffTotal += b.pickMove( mon, opp, damageOnly=True, validTypes=b.PHYSTYPES, ret='dmg') / opp.stats['hp']
        specOffTotal += b.pickMove( mon, opp, damageOnly=True, validTypes=b.SPECTYPES, ret='dmg') / opp.stats['hp']
        offTotal += b.pickMove( mon, opp, damageOnly=True, ret='dmg') / opp.stats['hp']

        # DEFENSIVE ANALYSIS
        physDefTotal += b.pickMove( opp, mon, damageOnly=True, validTypes=b.PHYSTYPES, ret='dmg') / mon.stats['hp']
        specDefTotal += b.pickMove( opp, mon, damageOnly=True, validTypes=b.SPECTYPES, ret='dmg') / mon.stats['hp']
        defTotal += b.pickMove( opp, mon, damageOnly=True, ret='dmg') / mon.stats['hp']

    physOffAvg = physOffTotal / 151
    specOffAvg = specOffTotal / 151
    offAvg = offTotal / 151
    physDefAvg = physDefTotal / 151
    specDefAvg = specDefTotal / 151
    defAvg = defTotal / 151

    results.loc[pokemon] = [physOffAvg, specOffAvg, offAvg, physDefAvg, specDefAvg, defAvg]
    print('finished processing %s' % pokemon)


results.to_csv('../results/Mon Analysis - LVL%s, %s Moveset.csv' % (LEVEL, MOVELIST))