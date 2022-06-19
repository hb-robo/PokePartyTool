# This file contains all of the classes that govern pokemon and battle functions, variables, and logic.
from concurrent.futures import process
import math
from unittest import expectedFailure
import pandas as pd
import numpy as np
import random

class Gen1Mon:

    dex = pd.read_csv('data/rby/rby_pokedex.csv', index_col='mon_name')

    statStages = {
        6: 4.00,
        5: 3.50,
        4: 3.00,
        3: 2.50,
        2: 2.00,
        1: 1.50,
        0: 1.00,
        -1: 0.66,
        -2: 0.50,
        -3: 0.40,
        -4: 0.33,
        -5: 0.28,
        -6: 0.25
    }

    evasionStages = {
        6: 0.25,
        5: 0.28,
        4: 0.33,
        3: 0.40,
        2: 0.50,
        1: 0.66,
        0: 1.00,
        -1: 1.50,
        -2: 2.00,
        -3: 2.50,
        -4: 3.00,
        -5: 3.50,
        -6: 4.00
    }
    
    def __init__( self, name, level ):
        if name not in list(self.dex.index.values):
            print("ERROR: Invalid Pokemon inputted to Gen1Mon object.")
        else:
            self.reset(name, level)

    def reset( self, name, level ):
        self.name = name
        self.types = [
            self.pokeDex.at[name, 'first_type'],
            self.pokeDex.at[name, 'second_type']
        ]

        self.stats = {
            'hp': int(self.dex.at[name,'lvl%s_hp' % level]),
            'attack': int(self.dex.at[name,'lvl%s_attack' % level]),
            'defense': int(self.dex.at[name,'lvl%s_defense' % level]),
            'special': int(self.dex.at[name,'lvl%s_special' % level]),
            'speed': int(self.dex.at[name,'lvl%s_speed' % level])
        }

        self.lastUsedMove = ""

        # stat buffs and nerfs
        self.statMods = {
            'attack': 0,
            'defense': 0,
            'special': 0,
            'speed': 0,
            'accuracy': 0,
            'evasion': 0
        }

        # status conditions
        self.hasStatus = False
        self.statusCounter = 0
        self.status = {
            'confused': False,
            'poisoned': False,
            'toxic': False,
            'asleep': False,
            'burned': False,
            'paralyzed': False,
            'frozen': False
        }
        
        # miscellaneous conditions
        self.rageCounter = 0
        self.rampageCounter = 0
        self.physProtection = 0.0
        self.specProtection = 0.0
        self.hasSubstitute = False
        self.isSeeded = False
        self.isTrapped = False
        self.isAirborne = False
        self.isUnderground = False

    def updateStats( self ):
        for stat in self.stats.keys():
            self.stats[stat] = math.floor(self.dex.at[self.name, stat] * self.statStages[self.statMods])

    def buff( self, stat, num_stages ):
        if stat not in ['attack','defense','special','speed','accuracy','evasion'] \
            or type(num_stages) != 'int' or num_stages <= 0:
            print("ERROR: Invalid input for buff(). No stat buff applied.")
        else:
            self.statMods[stat] += num_stages
            self.updateStats()
            


    def debuff( self, stat, num_stages ):
        if stat not in ['attack','defense','special','speed','accuracy','evasion'] or \
            type(num_stages) != 'int' or num_stages >= 0:
            print("ERROR: Invalid input for debuff(). No stat debuff applied.")
        else:
            self.statMods[stat] += num_stages
            self.updateStats()
        

class StadiumMon(Gen1Mon):
    accuracyStages = {
        6: 3.00,
        5: 2.66,
        4: 2.33,
        3: 2.00,
        2: 1.66,
        1: 1.33,
        0: 1.00,
        -1: 0.75,
        -2: 0.66,
        -3: 0.50,
        -4: 0.43,
        -5: 0.36,
        -6: 1/3
    }

    evasionStages = {
        6: 1/3,
        5: 0.36,
        4: 0.43,
        3: 0.50,
        2: 0.66,
        1: 0.75,
        0: 1.00,
        -1: 1.33,
        -2: 1.66,
        -3: 2.00,
        -4: 2.33,
        -5: 2.66,
        -6: 3.00
    }

    pass


class Gen1Battle:

    # constant lists for gens 1-3 calculation
    SPECTYPES = ['fire', 'water', 'grass', 'electric', 'ice', 'psychic', 'dragon']
    PHYSTYPES = ['normal', 'fighting', 'flying', 'poison', 'rock', 'ground', 'bug', 'ghost']

    # import data relevant to the generation
    pokeDex = pd.read_csv('data/rby/rby_pokedex.csv', index_col='mon_name')
    moveDex = pd.read_csv('data/rby/rby_movedex.csv', index_col='move')
    learnDex = pd.read_csv('data/rby/rby_move_access.csv', index_col='mon_name')
    types = pd.read_csv('data/gen1types_expanded.csv', index_col='off_type')

    # status condition heuristics:
    statusScores = {
        'freeze': 1,
        'sleep': 0.9,
        'paralyze': 0.7,
        'confuse': 0.6,
        'burn': 0.6,
        'toxic': 0.5,
        'poison': 0.25
    }


    def __init__( self, mon1, mon2 ):
        if type(mon1) is not Gen1Mon or type(mon2) is not Gen1Mon:
            print("Error: Both Gen1Battle inputs must be of type Gen1Mon.")
        else:
            self.reset( mon1, mon2 )

    def reset( self, mon1, mon2 ):
        self.pokemon = mon1
        self.opponent = mon2


    # There is a chance for an attack to do bonus critical damage.
    # In Generation 1, this is calculated using a Mon's base speed.
    def calculateCritChance( self, mon, move ):
        if self.moveDex.at[move, 'category'] != 'attack':
            print("ERROR: Status moves do not have critical chances.")
            return -1
        baseSpeed = self.pokeDex.at[mon.name, 'base_speed']

        # Some moves have additional improved critical chance.
        if pd.notna(move.dex.at[move,'crit']):
            critChance = (baseSpeed * 100 / 64) / 100
            #   However, crit chances can't exceed 255/256 due to programming error.
            return min(0.996, critChance)
        else:
            critChance = (baseSpeed * 100 / 512) / 100
            return min(0.996, critChance)


    # A damage multiplier called Same Type Attack Bonus (STAB) is
    #   triggered when a Mon uses a move with the same type as its own.
    def calculateSTAB( self, mon, move ):
        if self.moveDex.at[move,'type'] in mon.types:
            return 1.5
        else:
            return 1
    
    # Certain types of Pokemon are weak or resistant to certain types of attacks.
    def calculateTypeBonus( self, move, mon ):
        moveType = self.moveDex.at[move, 'type']
        if pd.notna(mon.types[1]):
            return self.types.at[moveType,'vs_%s_%s' % (mon.types[0], mon.types[1])]
        else:
            return self.types.at[moveType,'vs_%s' % mon.types[0]]

    # Depending on a move's typing, we need to pick the corresponding statistics
    #   for the attacking and defending Mons to calculate the move damage.
    def getAttackStat( self, move, mon ):
        moveType = self.moveDex.at[move,'type']
        if moveType in self.PHYSTYPES:
            return mon.stats['attack']
        elif moveType in self.SPECTYPES:
            return mon.stats['special']

    def getDefenseStat( self, move, mon ):
        moveType = self.moveDex.at[move,'type']
        if moveType in self.PHYSTYPES:
            return mon.stats['defense']
        elif moveType in self.SPECTYPES:
            return mon.stats['special']

    def getMovePower( self, move ):
        return int(self.moveDex.at[move,'power'])

    def getMoveAccuracy( self, move ):
        return 1 if move == 'swift' else min(0.996, self.moveDex.at[move,'accuracy']/100)

    # Because Pokemon is turn-based, we have to pick who attacks first.
    #   First, we check if one mon uses a priority move. Then, we compare
    #   speeds. Finally, if either of those methods tie, we flip a coin. 
    def monMovesFirst( self, monMove, oppMove ):
        if self.moveDex.at[monMove,'subcat'] == 'quick' and self.moveDex.at[oppMove,'subcat'] != 'quick':
            return True
        elif self.moveDex.at[oppMove,'subcat'] == 'quick' and self.moveDex.at[monMove,'subcat'] != 'quick':
            return False
        elif self.pokemon.stats['speed'] > self.opponent.stats['speed']:
            return True
        elif self.opponent.stats['speed'] > self.pokemon.stats['speed']:
            return False
        else:
            return np.random.choice(range(2),size=1,replace=False)[0]


    # This is the default damage calculation for most moves in the game.
    def getDamage( self, mon, move, opp ):
        if np.random.binomial(1,self.calculateCritChance(mon.name,move)):
            L = mon.level * 2
        else:
            L = mon.level
        AS = self.getAttackStat(move, mon.name)
        P = self.getMovePower(move)
        DS = self.getDefenseStat(move, opp.name)
        STAB = self.calculateSTAB(mon.name, move)
        TB = self.calculateTypeBonus(move, opp.name)

        base_dmg = min(((((2*L/5)+2)*(AS/DS)*P)/50),997)+2
        mod_dmg = math.floor(math.floor(base_dmg*STAB)*(TB*10/10))

        if mod_dmg == 0 or mod_dmg == 1:
            return float(mod_dmg)
        else:
            R = 217 + np.random.choice(range(39),size=1,replace=False)[0]
            return math.floor(mod_dmg*(R/255))

    # Because of the randomness involved in damage calculations, we need a
    #   method to get the expected damage amount on an average roll so that
    #   we can accurately derive the move with the highest expected value.
    def getExpectedDamage( self, mon, move, opp ):
        L = mon.level
        AS = self.getAttackStat(move, mon.name)
        P = self.getMovePower(move)
        DS = self.getDefenseStat(move, opp.name)
        STAB = self.calculateSTAB(mon.name, move)
        TB = self.calculateTypeBonus(move, opp.name)

        base_dmg = min(((((2*L/5)+2)*(AS/DS)*P)/50),997)+2
        crit_base_dmg = min(((((2*(2*L)/5)+2)*(AS/DS)*P)/50),997)+2

        mod_dmg = math.floor(math.floor(base_dmg*STAB)*(TB*10/10))
        if mod_dmg > 1:
            mod_dmg = math.floor(mod_dmg*(236/255))

        crit_mod_dmg = math.floor(math.floor(crit_base_dmg*STAB)*(TB*10/10))
        if crit_mod_dmg > 1:
            crit_mod_dmg = math.floor(crit_mod_dmg*(236/255))
        
        crit_chance = self.calculateCritChance(mon.name,move)

        total = (1 - crit_chance) * mod_dmg
        total_crit = crit_chance * crit_mod_dmg

        return total + total_crit


    # Here we will process the incoming move and account for all of the
    #   ways an attack can deal damage.
    def processMove( self, mon, move, opp, expected=False ):
        # Some moves do a damage amount relative to the user's level. These moves
        #    ignore STAB and type bonuses, BUT they do 0 damage to Pokemon who are
        #    immune to the move's type.
        if self.moveDex.at[move,'subcat'] == 'level_dep':
            if self.calculateTypeBonus(move,opp.name) == 0:
                return 0
            else:
                # Psywave does between 1 and 1.5x the user's level in damage.
                if move == 'psywave':
                    return math.floor(mon.level*0.75) if expected else (random.randrange(1, math.floor(mon.level*1.5)))
                # Night Shade and Submission do damage equal to the user's level.
                else:
                    return mon.level

        # Some moves do a fixed amount of damage, ignoring types and STAB.
        elif self.moveDex.at[move,'subcat'] == 'fixed':
            # Super Fang does half the opponent's current health, rounded down.
            if move == 'super fang':
                return max(1, math.floor(opp.hp / 2))
            # Supersonic and Dragon Rage do a fixed damage amount (20, 40 respectively).
            else:
                return float(self.moveDex.at[move,'power'])  

        # The flying move Mirror Move copies the opponent's last-used attack.
        elif self.moveDex.at[move,'subcat'] == 'reflect':
            if opp.lastUsedMove == "":
                return 0
            else:
                return self.processMove(mon, opp.lastUsedMove, opp, expected=expected)

        # Finally, the rest of the moves are calculated in a normal way.
        else:
            # If the opponent is charging Fly or Dig, only certain moves will hit it.
            if (opp.isUnderground) and not (self.moveDex.at[move, 'hit_dig']):
                return 0
            elif (opp.isAirborne) and not (self.moveDex.at[move,'hit_fly']):
                return 0
            # And here we have the calculation for every other move.
            else:
                if(expected):
                    return self.getExpectedDamage(mon, move, opp)
                else:
                    return self.getDamage(mon, move, opp)


    # For each move the Pokemon can use, we calculate a heuristic score for the overall value 
    #   of using the move versus a given opponent. We select the move with the highest score.
    def pickMove( self, mon, opp ):
        optimalMove = ""
        maxMoveScore = -1
        for move in self.learnDex.columns:        
            if pd.notna(self.learnDex.at[mon.name, move]) and move != 'index':
                # We're only considering attacking moves here, so status moves are skipped.
                if self.moveDex.at[move,'category'] == 'status':
                    continue

                # These are the attacking moves I haven't implemented yet.
                if self.moveDex.at[move,'subcat'] in ['suicide', 'reflect','counter', 'seed', 'rage', 'ko', 'random', 'status_dep']:
                    continue

                # First, the move's expected damage against the opponent is calculated.
                exp_dmg = self.processMove(mon, move, opp, expected=True)
                score=exp_dmg

                # Then, we account for the move's accuracy and the number of times
                #    the move hits. Even "max" accuracy is not 100% unless the move is 
                #    Swift. Otherwise, it's equal to 255/256, or 0.996.
                accuracy = self.getMoveAccuracy(move)
                score = power * accuracy * self.moveDex.at[move,'avg_hits']

                # At this stage we have an emergency exit clause. If the currently selected
                #   move is Quick Attack, and using it would kill the opponent, the Pokemon
                #   will always use it, because it has increased priority even if the opponent's
                #   speed is higher.
                if (score >= opp.stats['hp']) and self.moveDex.at[move,'subcat'] == 'quick':
                    optimalMove = 'quick attack'
                    maxMoveScore = score
                    break
                
                # We also want to account for how many turns the move takes to charge up.
                #    Moves like Fly and Dig aren't checked here because the charge is done 
                #    in a way that protects the user.
                if self.moveDex.at[move,'subcat'] == 'charge':
                    score /= float(self.moveDex.at[move,'avg_turns'])
                
                # There is a single move (Hyper Beam) that does not charge up but instead
                #   shoots first with a turn of rest afterwards required. If the move is
                #   expected to kill the next turn, this rest turn is ignored. If the move
                #   will not kill, this rest turn must be accounted for.
                if (self.moveDex.at[move,'subcat'] == 'burst') and (power < opp.stats['hp']):
                    score /= float(self.moveDex.at[move,'avg_turns'])
                
                # Next, we account for status conditions by multiplying the score by a
                #    factor of 1 + its affliction chance.
                #    e.g., a 100-score move with 20% chance to freeze now has a score of 120.
                if pd.notna(self.moveDex.at[move,'opp_status']):
                    status = self.moveDex.at[move,'opp_status']
                    status_chance = float(self.moveDex.at[move,'opp_status_chance'].strip('%'))/100
                    status_mod = 1 + (self.statusScores[status] * status_chance)
                    score += math.floor(score * status_mod)
                
                # Similarly, we account for flinch, but only if the user outspeeds its opponent.
                #    If it doesn't, the opponent will never flinch anyway. If the speed is
                #    equal, moving first is a coin flip, so the flinch chance is halved.
                if pd.notna(move.moveDex.at[move,'flinch']) and (mon.stats['speed'] >= opp.stats['speed']):
                    flinch_chance = float(self.moveDex.at[move,'flinch'].strip('%'))/100
                    if mon.stats['speed'] == opp.stats['speed']:
                        flinch_chance /= 2
                    score += math.floor(score * (1 + flinch_chance))
                
                # Finally, we account for ways in which the move can affect the user's HP.
                #   "Absorb" type moves heal the user for a percentage of the damage dealt,
                #   so we add the HP the user would heal to the score.
                if (self.moveDex.at[move,'subcat'] == 'absorb'):
                    heal_amt = math.floor(power * self.moveDex.at[move,'heal'])
                    health_diff = self.pokeDex.at[mon.name,'hp'] - mon.stats['hp']
                    if health_diff > heal_amt:
                        score += heal_amt
                    else:
                        score += health_diff
                
                #   Moves with recoil inflict damage on the user as a percentage of the damage
                #   inflicted, so we have to account for those.
                if pd.notna(self.moveDex.at[move,'recoil']):
                    recoil = math.floor(power * self.moveDex.at[move,'recoil'])
                    
                    # If the recoil would kill the user, its score is made to be zero to ensure 
                    # it doesn't pick it.
                    if ((mon.stats['hp'] - recoil) <= 0):
                        # BUT, if using the move is expected to kill, it will process the move
                        # normally, because the user will "win" before they die.
                        if exp_dmg < opp.stats['hp']:
                            score = 0
                    else:
                        score -= recoil
                
                #   This is kind of petty, but we also have to be wary of crash damage, which
                #   in Gen 1 is always 1 HP, lol.
                if pd.notna(self.moveDex.at[move,'crash']):
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
