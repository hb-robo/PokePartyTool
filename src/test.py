import pandas as pd
import utils.classes as g

mon1 = g.Gen1Mon('tauros', 50)
mon2 = g.Gen1Mon('chansey', 50)
mon3 = g.Gen1Mon('charmander', 50)

arena = g.Gen1Battle(mon1, mon2)

testingCrit = 0
if testingCrit:
    print("==============TESTING CRIT=================")
    for col in arena.learnDex.columns:
        if col != 'index' and pd.notna(arena.learnDex.at[mon1.name, col]) and (arena.learnDex.at[mon1.name, col] in ['HM','TM','RTM'] or int(arena.learnDex.at[mon1.name, col]) <= mon1.level):
            print("Crit chance of %s using %s: %s" % (mon1.name, col, arena.calculateCritChance(mon1, col)))

        if col != 'index' and pd.notna(arena.learnDex.at[mon2.name, col]) and (arena.learnDex.at[mon2.name, col] in ['HM','TM','RTM'] or int(arena.learnDex.at[mon2.name, col]) <= mon2.level):
            print("Crit chance of %s using %s: %s" % (mon2.name, col, arena.calculateCritChance(mon2, col)))

    
testingSTAB = 0
if testingSTAB:
    print("==============TESTING STAB=================") 
    for col in arena.learnDex.columns:
        if col != 'index' and pd.notna(arena.learnDex.at[mon1.name, col]) and arena.moveDex.at[col,'category'] == 'attack':
            print("STAB of %s using %s: %s" % (mon1.name, col, arena.calculateSTAB(mon1, col)))

        if col != 'index' and pd.notna(arena.learnDex.at[mon2.name, col]) and arena.moveDex.at[col,'category'] == 'attack':
            print("STAB of %s using %s: %s" % (mon2.name, col, arena.calculateSTAB(mon2, col)))

testingTB = 0
if testingTB:
    print("==============TESTING TYPE BONUS=================") 
    for col in arena.learnDex.columns:
        if col != 'index' and pd.notna(arena.learnDex.at[mon1.name, col]) and arena.moveDex.at[col,'category'] == 'attack':
            print("Type Bonus of %s using %s vs %s: %s" % (mon1.name, col, mon2.name, arena.calculateTypeBonus(col, mon2)))
        
        if col != 'index' and pd.notna(arena.learnDex.at[mon2.name, col]) and arena.moveDex.at[col,'category'] == 'attack':
            print("Type Bonus of %s using %s vs %s: %s" % (mon2.name, col, mon1.name, arena.calculateTypeBonus(col, mon1)))

testingAttStat = 0
if testingAttStat:
    print("==============TESTING ATT STAT=================") 
    for col in arena.learnDex.columns:
        if col != 'index' and pd.notna(arena.learnDex.at[mon1.name, col]) and arena.moveDex.at[col,'category'] == 'attack':
            print("Attack Stat for %s using move %s: %s" % (mon1.name, col, arena.getAttackStat(col,mon1)))

        if col != 'index' and pd.notna(arena.learnDex.at[mon2.name, col]) and arena.moveDex.at[col,'category'] == 'attack':
            print("Attack Stat for %s using move %s: %s" % (mon2.name, col, arena.getAttackStat(col,mon2)))

testingDefStat = 0
if testingDefStat:
    print("==============TESTING DEF STAT=================") 
    for col in arena.learnDex.columns:
        if col != 'index' and pd.notna(arena.learnDex.at[mon1.name, col]) and arena.moveDex.at[col,'category'] == 'attack':
            print("Defense Stat for %s defending against move %s: %s" % (mon2.name, col, arena.getDefenseStat(col,mon2)))

        if col != 'index' and pd.notna(arena.learnDex.at[mon2.name, col]) and arena.moveDex.at[col,'category'] == 'attack':
            print("Defense Stat for %s defending against move %s: %s" % (mon1.name, col, arena.getDefenseStat(col,mon1)))

testingMovePower = 0
if testingMovePower:
    print("==============TESTING MOVE POWER=================") 
    for col in arena.learnDex.columns:
        if col != 'index' and pd.notna(arena.learnDex.at[mon1.name, col]) and arena.moveDex.at[col,'category'] == 'attack' \
            and arena.moveDex.at[col,'subcat'] not in ['suicide', 'counter', 'rage', 'random', 'status_dep']:
            print("Move Power of %s: %s" % (col, arena.getMovePower(col)))

        elif col != 'index' and pd.notna(arena.learnDex.at[mon2.name, col]) and arena.moveDex.at[col,'category'] == 'attack' \
            and arena.moveDex.at[col,'subcat'] not in ['suicide', 'counter', 'rage', 'random', 'status_dep']:
            print("Move Power of %s: %s" % (col, arena.getMovePower(col)))

testingMoveAcc = 0
if testingMoveAcc:
    print("==============TESTING MOVE ACCURACY=================") 
    for col in arena.learnDex.columns:
        if col != 'index' and pd.notna(arena.learnDex.at[mon1.name, col]) and arena.moveDex.at[col,'category'] == 'attack' \
            and arena.moveDex.at[col,'subcat'] not in ['suicide', 'counter', 'rage', 'random', 'status_dep']:
            print("Move Accuracy of %s: %s" % (col, arena.getMoveAccuracy(col)))

        elif col != 'index' and pd.notna(arena.learnDex.at[mon2.name, col]) and arena.moveDex.at[col,'category'] == 'attack' \
            and arena.moveDex.at[col,'subcat'] not in ['suicide', 'counter', 'rage', 'random', 'status_dep']:
            print("Move Accuracy of %s: %s" % (col, arena.getMoveAccuracy(col)))

testingMovesFirst = 0
if testingMovesFirst:
    print("==============TESTING MOVES FIRST=================") 
    print("Does %s move first vs. %s? %s" % (mon1.name, mon2.name, ("Yes" if arena.monMovesFirst( 'tackle','tackle' ) else "No")))

testingGetDamage = 0
if testingGetDamage:
    print("==============TESTING GET DAMAGE=================") 
    for col in arena.learnDex.columns:
        if col != 'index' and pd.notna(arena.learnDex.at[mon1.name, col]) \
            and arena.moveDex.at[col,'category'] == 'attack' \
            and arena.moveDex.at[col,'subcat'] not in ['level_dep','fixed','reflect','ko','suicide', 'counter', 'rage', 'ko', 'random', 'status_dep'] \
            and pd.notna(arena.moveDex.at[col,'power']):
            print("%s uses %s vs %s for %s/%s HP" % (mon1.name, col, mon2.name, arena.getDamage(mon1, col, mon2), arena.pokeDex.at[mon2.name,'hp']))

    for col in arena.learnDex.columns:
        if col != 'index' and pd.notna(arena.learnDex.at[mon1.name, col]) \
            and arena.moveDex.at[col,'category'] == 'attack' \
            and arena.moveDex.at[col,'subcat'] not in ['level_dep','fixed','reflect','ko','suicide', 'counter', 'rage', 'ko', 'random', 'status_dep'] \
            and pd.notna(arena.moveDex.at[col,'power']):
            print("A burned %s uses %s vs %s for %s/%s HP" % (mon1.name, col, mon2.name, arena.getDamage(mon1, col, mon2, mod='burn'), arena.pokeDex.at[mon2.name,'hp']))

    for col in arena.learnDex.columns:
        if col != 'index' and pd.notna(arena.learnDex.at[mon2.name, col]) \
            and arena.moveDex.at[col,'category'] == 'attack' \
            and arena.moveDex.at[col,'subcat'] not in ['level_dep','fixed','reflect','ko','suicide', 'counter', 'rage', 'ko', 'random', 'status_dep'] \
            and pd.notna(arena.moveDex.at[col,'power']):
            print("%s uses %s vs %s for %s/%s HP" % (mon2.name, col, mon1.name, arena.getDamage(mon2, col, mon1), arena.pokeDex.at[mon1.name,'hp']))

    for col in arena.learnDex.columns:
        if col != 'index' and pd.notna(arena.learnDex.at[mon2.name, col]) \
            and arena.moveDex.at[col,'category'] == 'attack' \
            and arena.moveDex.at[col,'subcat'] not in ['level_dep','fixed','reflect','ko','suicide', 'counter', 'rage', 'ko', 'random', 'status_dep'] \
            and pd.notna(arena.moveDex.at[col,'power']):
            print("A burned %s uses %s vs %s for %s/%s HP" % (mon2.name, col, mon1.name, arena.getDamage(mon2, col, mon1, mod='burn'), arena.pokeDex.at[mon1.name,'hp']))

testingExpectedDamage = 0
if testingExpectedDamage:
    print("==============TESTING EXPECTED DAMAGE=================") 
    for col in arena.learnDex.columns:
        if col != 'index' and pd.notna(arena.learnDex.at[mon1.name, col]) \
            and arena.moveDex.at[col,'category'] == 'attack' \
            and arena.moveDex.at[col,'subcat'] not in ['level_dep','fixed','reflect','ko','suicide', 'counter', 'rage', 'ko', 'random', 'status_dep'] \
            and pd.notna(arena.moveDex.at[col,'power']):
            print("%s uses %s vs %s for an expected %s/%s HP" % (mon1.name, col, mon2.name, arena.getExpectedDamage(mon1, col, mon2), arena.pokeDex.at[mon2.name,'hp']))

    for col in arena.learnDex.columns:
        if col != 'index' and pd.notna(arena.learnDex.at[mon1.name, col]) \
            and arena.moveDex.at[col,'category'] == 'attack' \
            and arena.moveDex.at[col,'subcat'] not in ['level_dep','fixed','reflect','ko','suicide', 'counter', 'rage', 'ko', 'random', 'status_dep'] \
            and pd.notna(arena.moveDex.at[col,'power']):
            print("A burned %s uses %s vs %s for an expected %s/%s HP" % (mon1.name, col, mon2.name, arena.getExpectedDamage(mon1, col, mon2, mod='burn'), arena.pokeDex.at[mon2.name,'hp']))

    for col in arena.learnDex.columns:
        if col != 'index' and pd.notna(arena.learnDex.at[mon2.name, col]) \
            and arena.moveDex.at[col,'category'] == 'attack' \
            and arena.moveDex.at[col,'subcat'] not in ['level_dep','fixed','reflect','ko','suicide', 'counter', 'rage', 'ko', 'random', 'status_dep'] \
            and pd.notna(arena.moveDex.at[col,'power']):
            print("%s uses %s vs %s for an expected %s/%s HP" % (mon2.name, col, mon1.name, arena.getExpectedDamage(mon2, col, mon1), arena.pokeDex.at[mon1.name,'hp']))

    for col in arena.learnDex.columns:
        if col != 'index' and pd.notna(arena.learnDex.at[mon2.name, col]) \
            and arena.moveDex.at[col,'category'] == 'attack' \
            and arena.moveDex.at[col,'subcat'] not in ['level_dep','fixed','reflect','ko','suicide', 'counter', 'rage', 'ko', 'random', 'status_dep'] \
            and pd.notna(arena.moveDex.at[col,'power']):
            print("A burned %s uses %s vs %s for an expected %s/%s HP" % (mon2.name, col, mon1.name, arena.getExpectedDamage(mon2, col, mon1, mod='burn'), arena.pokeDex.at[mon1.name,'hp']))

testingConfusionDamage = 0
if testingConfusionDamage:
    print("==============TESTING CONFUSION DAMAGE=================") 
    print('%s took %s damage in its confusion.' % (mon1.name, arena.hurtItselfInConfusion(mon1)))
    print('%s took %s damage in its confusion.' % (mon2.name, arena.hurtItselfInConfusion(mon2)))
    print('%s would take %s damage on average if it hurt itself in confusion.' % (mon1.name, arena.hurtItselfInConfusion(mon1, expected=True)))
    print('%s would take %s damage on average if it hurt itself in confusion.' % (mon2.name, arena.hurtItselfInConfusion(mon2, expected=True)))

testingStatusValue = 0
if testingStatusValue:
    print("==============TESTING STATUS VALUE=================") 
    for move in arena.learnDex.columns:
        if move != 'index' and pd.notna(arena.learnDex.at[mon1.name, move]) and pd.notna(arena.moveDex.at[move,'opp_status']):
            print("The estimated status value of %s using %s vs. %s is %s" % (mon1.name, move, mon2.name, arena.calculateStatusValue(mon1, move, mon2)))
    for move in arena.learnDex.columns:
        if move != 'index' and pd.notna(arena.learnDex.at[mon2.name, move]) and pd.notna(arena.moveDex.at[move,'opp_status']):
            print("The estimated status value of %s using %s vs. %s is %s" % (mon2.name, move, mon1.name, arena.calculateStatusValue(mon2, move, mon1)))

testingProcessMove = 1
if testingProcessMove:
    print("==============TESTING PROCESS MOVE=================") 
    moveDict = {}
    for move in arena.learnDex.columns:
        if move != 'index' and pd.notna(arena.learnDex.at[mon1.name, move]) and (arena.moveDex.at[move,'category'] == 'attack' or arena.moveDex.at[move, 'subcat'] == 'status'):
            moveDict[move] = int(arena.processMove(mon1, move, mon2, expected=True))

    for tuple in sorted( ((v,k) for k,v in moveDict.items()), reverse=True):
        print("Move value of %s using %s vs. %s is %s" % (mon1.name, tuple[1], mon2.name, tuple[0]))

    print("==============TESTING PROCESS MOVE=================") 

    moveDict = {}
    for move in arena.learnDex.columns:
        if move != 'index' and pd.notna(arena.learnDex.at[mon2.name, move]) and (arena.moveDex.at[move,'category'] == 'attack' or arena.moveDex.at[move, 'subcat'] == 'status'):
            moveDict[move] = int(arena.processMove(mon2, move, mon1, expected=True))

    for tuple in sorted( ((v,k) for k,v in moveDict.items()), reverse=True):
        print("Move value of %s using %s vs. %s is %s" % (mon2.name, tuple[1], mon1.name, tuple[0]))





# print("==============TESTING MOVE PICKER=================") 
# # with open("log.txt","w") as f:
# #     for pokemon in list(gen1.pokeDex.index):
# #         opponent = classes.Mon(pokemon, gen1.pokeDex)

# #         print('~~~~VERSUS %s~~~~\n' % pokemon, file=f)
# #         print("Bulbasaur's optimal move is %s\n" % string.capwords(gen1.pickMove(bulbasaur, opponent)), file=f)
# #         print("Charmander's optimal move is %s\n" % string.capwords(gen1.pickMove(charmander, opponent)), file=f)
# #         print("Squirtle's optimal move is %s\n" % string.capwords(gen1.pickMove(squirtle, opponent)), file=f)


# print("==============BATTLE SIMULATOR=================")

# df = pd.DataFrame(columns=list(gen1.pokeDex.index.values))
# print(df.shape)

# for mon1 in list(gen1.pokeDex.index.values):
#     recordLog = []

#     totWins = 0
#     totFights = 0

#     for mon2 in list(gen1.pokeDex.index.values):
        
#         wins = 0
#         fights = 10
        
#         if mon1 == mon2:
#             totFights += fights
#             totFights += fights/2
#             recordLog.append(float(1/2))
#             print('%s wins %s/%s times vs. %s' % (mon1, fights/2, fights, mon2))
#             continue
        
#         for i in range(fights):
#             pokemon = classes.Mon(mon1, gen1.pokeDex)
#             opponent = classes.Mon(mon2, gen1.pokeDex)

#             fightResults = gen1.battle(pokemon, opponent, log=False)

#             if fightResults > 0:
#                 wins += 1
#                 totWins += 1

#             totFights += 1

#         recordLog.append(wins/float(fights))
#         print('%s wins %s/%s times vs. %s' % (mon1, wins, fights, mon2))

#     # print('%s total win/loss ratio: %s' % (mon1, (float(totWins)/totFights)))
#     df.loc[mon1] = recordLog

# df.index = list(gen1.pokeDex.index.values)

# df.to_csv('results.csv')
