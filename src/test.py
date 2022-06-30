import pandas as pd
import utils.classes as g

mon1 = g.Gen1Mon('victreebel', 50)
mon2 = g.Gen1Mon('cloyster', 50)
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

testingProcessMove = 0
if testingProcessMove:
    print("==============TESTING PROCESS MOVE=================") 
    moveDict = {}
    for move in arena.learnDex.columns:
        if move != 'index' and pd.notna(arena.learnDex.at[mon1.name, move]):
            value = (arena.processMove(mon1, move, mon2, expected=True))
            moveDict[move] = int(value) if pd.notna(value) else -1

    for tuple in sorted( ((v,k) for k,v in moveDict.items()), reverse=True):
        print("Move value of %s using %s vs. %s is %s" % (mon1.name, tuple[1], mon2.name, tuple[0]))

    print("==============TESTING PROCESS MOVE=================") 

    moveDict = {}
    for move in arena.learnDex.columns:
        if move != 'index' and pd.notna(arena.learnDex.at[mon2.name, move]):
            value = (arena.processMove(mon2, move, mon1, expected=True))
            moveDict[move] = int(value) if pd.notna(value) else -1

    for tuple in sorted( ((v,k) for k,v in moveDict.items()), reverse=True):
        print("Move value of %s using %s vs. %s is %s" % (mon2.name, tuple[1], mon1.name, tuple[0]))

testingMovePicker = 0
if testingMovePicker:
    print("==============TESTING MOVE PICKER=================")
    moveDict = {}
    for pokemon in list(arena.pokeDex.index):
        opponent = g.Gen1Mon(pokemon, level=50)
        move = arena.pickMove(mon1, opponent)
        # print("%s's optimal opener vs. %s is %s" % (mon1.name, pokemon, move))
        moveDict[move] = 1 if move not in moveDict else (moveDict[move]+1)

    print("~~~optimal move list for %s~~~" % mon1.name)
    moveList = sorted( ((v,k) for k,v in moveDict.items()), reverse=True)
    i = 0
    while i < 4 and i < len(moveList):
        print("%16s \t(%s uses)" % (moveList[i][1], moveList[i][0]))
        i += 1

testingBattleSim = 1
if testingBattleSim:
    print("==============BATTLE SIMULATOR=================")

    monRecord = {}
    totWins = 0
    losses = {}

    matches = 1

    for pokemon in list(arena.pokeDex.index):
        if pokemon == mon1.name:
            continue

        wins = 0

        for i in range(matches):
            opponent = g.Gen1Mon(pokemon, level=50)
            battle = g.Gen1Battle(mon1, opponent)
            result = battle.battle(log=True)
            if result > 0:
                wins += 1
            else:
                if pokemon not in losses:
                    losses[pokemon] = 1
                else:
                    losses[pokemon] += 1
            mon1.reset()

        print("%s won %s/%s matchups vs. %s." % (mon1.name, wins, matches, pokemon))
        monRecord[pokemon] = wins
        totWins += wins

    print("=======================================")
    print("%s won %s/%s total matchups." % (mon1.name, totWins, matches*150))

    moveList = sorted( ((v,k) for k,v in mon1.moveLog.items()), reverse=True)
    i = 0
    while i < len(moveList):
        print("%16s \t(%s uses)" % (moveList[i][1], moveList[i][0]))
        i += 1

    print("=======================================")
    print("Losses:")

    lossList = sorted( ((v,k) for k,v in losses.items()), reverse=True)
    i = 0
    while i < len(lossList):
        print("%16s \t(%s Ls)" % (lossList[i][1], lossList[i][0]))
        i += 1
    print("=======================================")


testingAllMatchups = 0
if testingAllMatchups:
    print("==============1V1 SIMULATOR=================")
    matchups = {}
    # moves = {}
    num_rounds = 10

    for name in list(arena.pokeDex.index):
        challenger = g.Gen1Mon(name, level=50)
        monRecord = {}
        totWins = 0
        totMatches = 0

        for pokemon in list(arena.pokeDex.index):
            if pokemon == name:
                continue

            wins = 0
            matches = 0

            for i in range(num_rounds):
                opponent = g.Gen1Mon(pokemon, level=50)
                battle = g.Gen1Battle(challenger, opponent)
                result = battle.battle(log=False)
                if result > 0:
                    wins += 1
                matches += 1
                challenger.reset(challenger.name, level=50)
                
            monRecord[opponent.name] = float(wins) / matches
            # print("%s record against %s: %s/%s" % (challenger.name, opponent.name, wins, matches))
            totWins += wins
            totMatches += matches

        monRecord['total'] = float(totWins) / totMatches
        print("%s overall record: %s/%s" % (challenger.name, totWins, totMatches))

        matchups[challenger.name] = monRecord

        # for move in moveList:
        #     if move[1] not in moves:
        #         moves[move[1]] = move[0]
        #     else:
        #         moves[move[1]] += move[0]

    df = pd.DataFrame.from_dict(matchups, orient='index')
    df.to_csv('results.csv')


getELO = 0
# if getELO:

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
