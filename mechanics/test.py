from asyncio.windows_events import NULL
import gen1
import pandas as pd
import classes

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

for col in gen1.learnDex.columns:
    if col != 'index' and pd.notna(gen1.learnDex.at['bulbasaur', col]) \
        and gen1.moveDex.at[col,'category'] == 'attack' \
        and gen1.moveDex.at[col,'subcat'] not in ['suicide', 'counter', 'seed', 'rage', 'ko', 'random', 'status_dep'] \
        and pd.notna(gen1.moveDex.at[col,'power']):
        print("%s uses %s vs %s for %s/%s HP\n" % ('bulbasaur', col, 'charmander', gen1.calculateDamage(bulbasaur, col, charmander), gen1.pokeDex.at['charmander','hp']))
        print("%s uses %s vs %s for %s/%s HP\n" % ('bulbasaur', col, 'squirtle', gen1.calculateDamage(bulbasaur, col, squirtle), gen1.pokeDex.at['charmander','hp']))
