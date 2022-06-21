import numpy as np

def battle(mon, opp, level=50, log=False) -> int:
    turnCounter = 0

    if(log):
        print("====  %s vs. %s at L%s  ====" % (mon.name, opp.name, level))

    while(mon.hp > 0 and opp.hp > 0):
        turnCounter += 1

        if(log):
            print("---TURN %s: %s: %s/%s, opponent %s: %s/%s" % (turnCounter, mon.name, mon.hp, pokeDex.at[mon.name, 'hp'], opp.name, opp.hp, pokeDex.at[opp.name,'hp']))

        monMove = pickMove(mon, opp)
        oppMove = pickMove(opp, mon)

        if monMovesFirst(mon, monMove, opp, oppMove):
            
            if(np.random.binomial(1, float(moveDex.at[monMove,'accuracy'])/100)):
                dmg = calculateDamage(mon, monMove, opp, level)
                opp.hp -= dmg
                if(log):
                    print("%s uses %s. opponent %s takes %s damage!" % (mon.name, monMove, opp.name, dmg))
                if opp.hp <= 0:
                    if(log):
                        print("opponent %s faints!" % opp.name)
                    break
            else:
                if(log):
                    print("%s uses %s, but it missed!" % (mon.name, monMove))


            if(np.random.binomial(1, float(moveDex.at[oppMove,'accuracy'])/100)):
                dmg = calculateDamage(opp, oppMove, mon, level)
                mon.hp -= dmg
                if(log):
                    print("opponent %s uses %s. %s takes %s damage!" % (opp.name, oppMove, mon.name, dmg))
                if mon.hp <= 0:
                    if(log):
                        print("%s faints!" % mon.name)
                    turnCounter = (0 - turnCounter)
                    break
            else:
                if(log):
                    print("opponent %s uses %s, but it missed!" % (opp.name, oppMove))
        
        else:

            if(np.random.binomial(1, float(moveDex.at[oppMove,'accuracy'])/100)):
                dmg = calculateDamage(opp, oppMove, mon, level)
                mon.hp -= dmg
                if(log):
                    print("opponent %s uses %s. %s takes %s damage!" % (opp.name, oppMove, mon.name, dmg))
                if mon.hp <= 0:
                    if(log):
                        print("%s faints!" % mon.name)
                    turnCounter = (0 - turnCounter)
                    break
            else:
                if(log):
                    print("opponent %s uses %s, but it missed!" % (opp.name, oppMove))


            if(np.random.binomial(1, float(moveDex.at[monMove,'accuracy'])/100)):
                dmg = calculateDamage(mon, monMove, opp, level)
                opp.hp -= dmg
                if(log):
                    print("%s uses %s. opponent %s takes %s damage!" % (mon.name, monMove, opp.name, dmg))
                if opp.hp <= 0:
                    if(log):
                        print("opponent %s faints!" % opp.name)
                    break
            else:
                if(log):
                    print("%s uses %s, but it missed!" % (mon.name, monMove))

    return turnCounter