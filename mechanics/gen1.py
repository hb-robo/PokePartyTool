from cmath import log
import numpy as np
import pandas as pd
import random
import math

# constant lists for gens 1-3 calculation
SPECTYPES = ['fire', 'water', 'grass', 'electric', 'ice', 'psychic', 'dragon']
PHYSTYPES = ['normal', 'fighting', 'flying', 'poison', 'rock', 'ground', 'bug', 'ghost']

# import data relevant to the generation
pokeDex = pd.read_csv('data/rby/rby_pokedex.csv', index_col='mon_name')
moveDex = pd.read_csv('data/rby/rby_movedex.csv', index_col='move')
learnDex = pd.read_csv('data/rby/rby_move_access.csv', index_col='mon_name')
types = pd.read_csv('data/gen1types_expanded.csv', index_col='off_type')

# There is a chance for all moves to do a bonus amount of damage, called a
#   critical hit. The chance is based on the user's base speed.
def calculateCritChance(monName, moveName):
    # Critical hits only apply to attacking moves.
    if moveDex.at[moveName, 'category'] != 'attack':
        # print("Status moves do not have critical chances.")
        return -1
    baseSpeed = pokeDex.at[monName, 'base_speed']
    # Some moves have a massively improved critical chance. In combination with some
    #   very fast Pokemon, this can create a maxed out critical chance where it is
    #   almost guaranteed to do critical damage.
    #  However, crit chances can't exceed 255/256 due to programming error.
    if pd.notna(moveDex.at[moveName,'crit']):
        critChance = (baseSpeed * 100 / 64) / 100
        return min(0.996, critChance)
    else:
        critChance = (baseSpeed * 100 / 512) / 100
        return min(0.996, critChance)

# If a Pokemon uses a move that has the same type as it does, the move's
#   damage is boosted by Same Type Attack Bonus (STAB). Pokemon with more
#   than one type get STAB bonuses for both of its types.
def calculateSTAB(monName, moveName,pokeDex=pokeDex,moveDex=moveDex):
    if moveDex.at[moveName,'type'] in (pokeDex.at[monName, 'first_type'], pokeDex.at[monName, 'second_type']):
        return 1.5
    else:
        return 1

# Certain types of Pokemon are weak or resistant to certain types of attacks.
#    In some cases, typed Pokemon can even be immune to an attack type.
def calculateTypeBonus(moveName, oppName, pokeDex=pokeDex,moveDex=moveDex):
    moveType = moveDex.at[moveName, 'type']
    oppTypes = [pokeDex.at[oppName, 'first_type']]
    if pd.notna(pokeDex.at[oppName, 'second_type']):
        oppTypes.append(pokeDex.at[oppName, 'second_type'])
        return types.at[moveType,'vs_%s_%s' % (oppTypes[0], oppTypes[1])]
    else:
        return types.at[moveType,'vs_%s' % oppTypes[0]]


def getAttackStat(moveName, monName):
    moveType = moveDex.at[moveName,'type']
    if moveType in PHYSTYPES:
        return int(pokeDex.at[monName,'attack'])
    elif moveType in SPECTYPES:
        return int(pokeDex.at[monName,'special'])

def getDefenseStat(moveName, monName):
    moveType = moveDex.at[moveName,'type']
    if moveType in PHYSTYPES:
        return int(pokeDex.at[monName,'defense'])
    elif moveType in SPECTYPES:
        return int(pokeDex.at[monName,'special'])

def getMovePower(moveName, moveDex=moveDex):
    return int(moveDex.at[moveName,'power'])

def getMoveAccuracy(moveName,moveDex=moveDex):
    return 1 if moveName == 'swift' else min(0.996, moveDex.at[moveName,'accuracy']/100)

def calculateDamage(mon, moveName, opp, level=50):
    # Some moves do a damage amount relative to the user's level. These moves
    #    ignore STAB and type bonuses, BUT they do 0 damage to Pokemon who are
    #    immune to the move's type.
    if moveDex.at[moveName,'subcat'] == 'level_dep':
        if calculateTypeBonus(moveName,opp.name) == 0:
            return 0
        else:
            # Psywave does between 1 and 1.5x the user's level in damage.
            if moveName == 'psywave':
                return random.randrange(1, math.floor(level*1.5))
            # Night Shade and Submission do damage equal to the user's level.
            else:
                return level

    # Some moves do a fixed amount of damage, ignoring types and STAB.
    elif moveDex.at[moveName,'subcat'] == 'fixed':
        # Super Fang does half the opponent's health, rounded down.
        if moveName == 'super fang':
            return max(1, math.floor(opp.hp / 2))
        # Supersonic and Dragon Rage do a fixed damage amount.
        else:
            return float(moveDex.at[moveName,'power'])  

    # The flying move Mirror Move copies the opponent's last-used attack.
    elif moveDex.at[moveName,'subcat'] == 'reflect':
        chosenMove = opp.lastUsedMove
        if chosenMove is None:
            return 0
        else:
            return calculateDamage(mon,chosenMove,opp,level)

    # Finally, the rest of the moves are calculated in a normal way.
    else:
        # If the opponent is in the air or underground, AKA charging Fly or Dig,
        #    only certain moves will hit it.
        if (opp.isUnderground) and not (moveDex.at[moveName, 'hit_dig']):
            return 0
        elif (opp.isAirborne) and not (moveDex.at[moveName,'hit_fly']):
            return 0
        # And here we have the calculation for every other move.
        else:
            if np.random.binomial(1,calculateCritChance(mon.name,moveName)):
                L = level * 2
            else:
                L = level
            AS = getAttackStat(moveName, mon.name)
            P = getMovePower(moveName)
            DS = getDefenseStat(moveName, opp.name)
            STAB = calculateSTAB(mon.name, moveName)
            TB = calculateTypeBonus(moveName, opp.name)

            base_dmg = min(((((2*L/5)+2)*(AS/DS)*P)/50),997)+2
            mod_dmg = math.floor(math.floor(base_dmg*STAB)*(TB*10/10))

            if mod_dmg == 0 or mod_dmg == 1:
                return float(mod_dmg)
            else:
                R = random.randrange(217,256)
                return math.floor(mod_dmg*(R/255))

# For each move the Pokemon can use, we calculate a heuristic score
#   that tries to encapsulate the overall value of using the move
#   versus a given opponent. The move with the highest score will
#   be selected for use.
def pickMove(mon, opp, level=50):
    optimalMove = ""
    maxMoveScore = -1
    for move in learnDex.columns:        
        if pd.notna(learnDex.at[mon.name, move]) and move != 'index':
            # We're only considering attacking moves here, so status moves are skipped.
            if moveDex.at[move,'category'] == 'status':
                continue
            # Many of the most powerful moves in the game cause the user to
            #   kill themselves. Because the user always faints first in the
            #   event of a double knockout, these moves will always be skipped.
            if moveDex.at[move,'subcat'] in ['suicide', 'reflect','counter', 'seed', 'rage', 'ko', 'random', 'status_dep']:
                continue

            # First, the move's damage against the opponent is calculated.
            if moveDex.at[move, 'subcat'] == 'level_dep':
                if move == 'psywave':
                    power = (1.5 * level / 2)
                else:
                    power = level
            elif moveDex.at[move, 'subcat'] == 'fixed':
                if move == 'super fang':
                    power = math.floor(opp.hp/2)
                else: 
                    power = getMovePower(move)
            else:
                power = getMovePower(move)
            # Then, we account for the move's accuracy and the number of times
            #    the move hits. Even "max" accuracy is not 100% unless the move is 
            #    Swift. Otherwise, it's equal to 255/256, or 0.996.
            accuracy = getMoveAccuracy(move)
            score = power * accuracy * moveDex.at[move,'avg_hits']

            # Accounting for high critical chances:
            critChance = 1 + calculateCritChance(mon.name, move)
            score *= critChance

            # Accounting for STAB:
            STAB = calculateSTAB(mon.name, move)
            score *= critChance

            # Accounting for Type Bonuses:
            TB = calculateTypeBonus(move, opp.name)
            score *= TB

            # At this stage we have an emergency exit clause. If the currently selected
            #   move is Quick Attack, and using it would kill the opponent, the Pokemon
            #   will always use it, because it has increased priority even if the opponent's
            #   speed is higher.
            if (score >= opp.hp) and moveDex.at[move,'subcat'] == 'quick':
                optimalMove = 'quick attack'
                maxMoveScore = score
                break
            
            # We also want to account for how many turns the move takes to charge up.
            #    Moves like Fly and Dig aren't checked here because the charge is done 
            #    in a way that protects the user.
            if moveDex.at[move,'subcat'] == 'charge':
                score /= float(moveDex.at[move,'avg_turns'])
            
            # There is a single move (Hyper Beam) that does not charge up but instead
            #   shoots first with a turn of rest afterwards required. If the move is
            #   expected to kill the next turn, this rest turn is ignored. If the move
            #   will not kill, this rest turn must be accounted for.
            if (moveDex.at[move,'subcat'] == 'burst') and (power < opp.hp):
                score /= float(moveDex.at[move,'avg_turns'])
            
            # Next, we account for status conditions by multiplying the score by a
            #    factor of 1 + its affliction chance.
            #    e.g., a 100-score move with 20% chance to poison now has a score of 120.
            if pd.notna(moveDex.at[move,'opp_status']):
                status_chance = float(moveDex.at[move,'opp_status_chance'].strip('%'))/100
                score += math.floor(score * status_chance)
            
            # Similarly, we account for flinch, but only if the user outspeeds its opponent.
            #    If it doesn't, the opponent will never flinch anyway. If the speed is
            #    equal, moving first is a coin flip, so the flinch chance is halved.
            if pd.notna(moveDex.at[move,'flinch']) and (mon.speed >= opp.speed):
                flinch_chance = float(moveDex.at[move,'flinch'].strip('%'))/100
                if mon.speed == opp.speed:
                    flinch_chance /= 2
                score += math.floor(score * flinch_chance)
            
            # Finally, we account for ways in which the move can affect the user's HP.
            #   "Absorb" type moves heal the user for a percentage of the damage dealt,
            #   so we add the HP the user would heal to the score.
            if (moveDex.at[move,'subcat'] == 'absorb'):
                heal_amt = math.floor(power * moveDex.at[move,'heal'])
                health_diff = pokeDex.at[mon.name,'hp'] - mon.hp
                if health_diff > heal_amt:
                    score += heal_amt
                else:
                    score += health_diff
            
            #   Moves with recoil inflict damage on the user as a percentage of the damage
            #   inflicted, so we have to account for those. If the recoil would kill the user,
            #   its score is made to be zero to ensure it doesn't pick it.
            if pd.notna(moveDex.at[move,'recoil']):
                recoil = math.floor(power * moveDex.at[move,'recoil'])
                if ((mon.hp - recoil) <= 0):
                    score = 0
                else:
                    score -= recoil
            
            #   This is kind of petty, but we also have to be wary of crash damage, which
            #   in Gen 1 is always 1 HP, lol.
            if pd.notna(moveDex.at[move,'crash']):
                score -= 1
            
            # If this move amounts to be optimal, we update the optimal move.
            if score > maxMoveScore:
                optimalMove = move
                maxMoveScore = score
    
    # Finally, we return the optimal move, or return struggle if nothing is picked.
    if optimalMove == "":
        return 'struggle'
    else:
        return optimalMove

def monMovesFirst(mon, monMove, opp, oppMove):
    if moveDex.at[monMove,'subcat'] == 'quick' and moveDex.at[oppMove,'subcat'] != 'quick':
        return True
    elif moveDex.at[oppMove,'subcat'] == 'quick' and moveDex.at[monMove,'subcat'] != 'quick':
        return False
    elif mon.speed > opp.speed:
        return True
    elif opp.speed > mon.speed:
        return False
    else:
        return np.random.choice(range(2),size=1,replace=False)[0]


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