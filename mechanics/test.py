from asyncio.windows_events import NULL

from numpy import record
import gen1
import pandas as pd
import classes
import string

mon = 'bulbasaur'


print("==============TESTING CRIT=================")
for col in gen1.learnDex.columns:
    if col != 'index' and pd.notna(gen1.learnDex.at['bulbasaur', col]):
        print("%s: %s" % (col, gen1.calculateCritChance('bulbasaur', col)))
    
print("==============TESTING STAB=================") 
for col in gen1.learnDex.columns:
    if col != 'index' and pd.notna(gen1.learnDex.at['bulbasaur', col]) and gen1.moveDex.at[col,'category'] == 'attack':
        print("%s: %s" % (col, gen1.calculateSTAB('bulbasaur', col)))

print("==============TESTING TYPE BONUS=================") 
for col in gen1.learnDex.columns:
    if col != 'index' and pd.notna(gen1.learnDex.at['bulbasaur', col]) and gen1.moveDex.at[col,'category'] == 'attack':
        print("%s: %s vs %s" % (col, gen1.calculateTypeBonus(col, 'charmander'), 'charmander'))
        print("%s: %s vs %s" % (col, gen1.calculateTypeBonus(col, 'squirtle'), 'squirtle'))

print("==============TESTING ATT STAT=================") 
for col in gen1.learnDex.columns:
    if col != 'index' and pd.notna(gen1.learnDex.at['bulbasaur', col]) and gen1.moveDex.at[col,'category'] == 'attack':
        print("%s: %s" % (col, gen1.getAttackStat(col,'bulbasaur')))

print("==============TESTING DEF STAT=================") 
for col in gen1.learnDex.columns:
    if col != 'index' and pd.notna(gen1.learnDex.at['bulbasaur', col]) and gen1.moveDex.at[col,'category'] == 'attack':
        print("%s: %s" % (col, gen1.getDefenseStat(col,'bulbasaur')))

print("==============TESTING MOVE POWER=================") 
for col in gen1.learnDex.columns:
    if col != 'index' and pd.notna(gen1.learnDex.at['bulbasaur', col]) and gen1.moveDex.at[col,'category'] == 'attack' \
        and gen1.moveDex.at[col,'subcat'] not in ['suicide', 'counter', 'seed', 'rage', 'ko', 'random', 'status_dep']:
        print("%s: %s" % (col, gen1.getMovePower(col)))

print("==============TESTING MOVE POWER=================") 
bulbasaur = classes.Mon('bulbasaur', gen1.pokeDex)
squirtle = classes.Mon('squirtle', gen1.pokeDex)
charmander = classes.Mon('charmander', gen1.pokeDex)

# for col in gen1.learnDex.columns:
#     if col != 'index' and pd.notna(gen1.learnDex.at['bulbasaur', col]) \
#         and gen1.moveDex.at[col,'category'] == 'attack' \
#         and gen1.moveDex.at[col,'subcat'] not in ['suicide', 'counter', 'seed', 'rage', 'ko', 'random', 'status_dep'] \
#         and pd.notna(gen1.moveDex.at[col,'power']):
#         print("%s uses %s vs %s for %s/%s HP\n" % ('bulbasaur', col, 'charmander', gen1.calculateDamage(bulbasaur, col, charmander), gen1.pokeDex.at['charmander','hp']))
#         print("%s uses %s vs %s for %s/%s HP\n" % ('bulbasaur', col, 'squirtle', gen1.calculateDamage(bulbasaur, col, squirtle), gen1.pokeDex.at['charmander','hp']))


print("==============TESTING MOVE PICKER=================") 
# with open("log.txt","w") as f:
#     for pokemon in list(gen1.pokeDex.index):
#         opponent = classes.Mon(pokemon, gen1.pokeDex)

#         print('~~~~VERSUS %s~~~~\n' % pokemon, file=f)
#         print("Bulbasaur's optimal move is %s\n" % string.capwords(gen1.pickMove(bulbasaur, opponent)), file=f)
#         print("Charmander's optimal move is %s\n" % string.capwords(gen1.pickMove(charmander, opponent)), file=f)
#         print("Squirtle's optimal move is %s\n" % string.capwords(gen1.pickMove(squirtle, opponent)), file=f)


print("==============BATTLE SIMULATOR=================")

df = pd.DataFrame(columns=list(gen1.pokeDex.index))

for mon1 in list(gen1.pokeDex.index):
    recordLog = []

    totWins = 0

    for mon2 in list(gen1.pokeDex.index):
        wins = 0
        fights = 100

        for i in range(fights):
            pokemon = classes.Mon(mon1, gen1.pokeDex)
            opponent = classes.Mon(mon2, gen1.pokeDex)

            fightResults = gen1.battle(pokemon, opponent, log=False)

            if fightResults > 0:
                wins += 1
                totWins += 1

        recordLog.append(wins/float(fights))
        print('%s wins %s/%s times vs. %s' % (mon1, wins, fights, mon2))

    print('%s total win/loss ratio: %s' % (mon1, (float(totWins)/15100)))
    df[mon1] = recordLog

df.to_csv('results.csv')