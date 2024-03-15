# This file contains all of the classes that govern pokemon and battle functions, variables, and logic.
import math
import pandas as pd
import numpy as np
import random
import copy
import os

# constant lists for gens 1-3 calculation
SPECTYPES = ['fire', 'water', 'grass', 'electric', 'ice', 'psychic', 'dragon']
PHYSTYPES = ['normal', 'fighting', 'flying', 'poison', 'rock', 'ground', 'bug', 'ghost']

# import data relevant to the generation
pokeDex = pd.read_csv(
    os.path.join(
        os.path.dirname(__file__), 
        '../../data/rby/rby_pokedex.csv'
    ),
    index_col='mon_name'
)
moveDex = pd.read_csv(
    os.path.join(
        os.path.dirname(__file__),
        '../../data/rby/rby_movedex.csv'
    ),
    index_col='move'
)
learnDex = pd.read_csv(
    os.path.join(
        os.path.dirname(__file__), 
        '../data/rby/rby_move_access.csv'
    ), 
    index_col='mon_name'
)
types = pd.read_csv(
    os.path.join(
        os.path.dirname(__file__), 
        '../data/types/gen1types_expanded.csv'
        ), 
    index_col='off_type'
)

class Gen1Mon:
   
    def __init__( self, name, level ):
        if name not in list(pokeDex.index.values):
            print("ERROR: Invalid Pokemon inputted to Gen1Mon object.")
        else:
            self.moveLog = {}
            self.trueName = name
            self.level = level
            self.reset()

    def reset( self ):

        self.name = self.trueName
        self.types = [
            pokeDex.at[self.trueName, 'first_type'],
            pokeDex.at[self.trueName, 'second_type']
        ]

        # self.stats = {
        #     'hp': int(self.dex.at[name,'lvl%s_hp' % level]),
        #     'attack': int(self.dex.at[name,'lvl%s_attack' % level]),
        #     'defense': int(self.dex.at[name,'lvl%s_defense' % level]),
        #     'special': int(self.dex.at[name,'lvl%s_special' % level]),
        #     'speed': int(self.dex.at[name,'lvl%s_speed' % level])
        # }
        self.stats = {
            'hp': int(pokeDex.at[self.trueName,'hp']),
            'attack': int(pokeDex.at[self.trueName,'attack']),
            'defense': int(pokeDex.at[self.trueName,'defense']),
            'special': int(pokeDex.at[self.trueName,'special']),
            'speed': int(pokeDex.at[self.trueName,'speed'])          
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
            'poison': False,
            'toxic': False,
            'sleep': False,
            'burn': False,
            'paralyze': False,
            'freeze': False
        }
        self.wokeUp = False

        self.volStatus = {
            'confuse': False,
            'seed': False,
            'curse': False
        }
        self.confusedNoLonger = False

        self.confusionCounter = 0

        self.willFlinch = False

        self.hasToRest = False
        self.hasToCharge = False
        self.isCharged = False

        self.bufferedMove = ""

        # miscellaneous conditions
        self.rageCounter = 0
        self.rampageCounter = 0
        self.physProtection = 0.0
        self.specProtection = 0.0
        self.hasSubstitute = False
        self.isTrapped = False
        self.isAirborne = False
        self.isUnderground = False

        self.isTransformed = False
        self.reflecting = False

        self.physDefense = False
        self.specDefense = False

        self.incomingMove = ''
        self.incomingDamage = 0

        self.knowsSwift = True if pd.notna(learnDex.at[self.name, 'swift']) else False
        print(self.knowsSwift)
            

    def uses( self, move, log=False ):
        if log:
            print("%s uses %s!" % (self.trueName, move))
        self.lastUsedMove = move
        if not self.isTransformed and not self.reflecting:
            self.logMove(move)

    def updateStats( self ):
        for stat in self.stats:
            if stat == 'hp':
                continue
            elif stat == 'evasion':
                self.stats[stat] = math.floor(pokeDex.at[self.name, stat] * self.evasionStages[self.statMods[stat]])
            else:
                self.stats[stat] = math.floor(pokeDex.at[self.name, stat] * self.statStages[self.statMods[stat]])

    def logMove( self, move ):

        if move in self.moveLog:
            self.moveLog[move] += 1
        else:
            self.moveLog[move] = 1

    def increment( self ):
        if self.rampageCounter > 0:
            self.rampageCounter -= 1
        if self.rageCounter > 0:
            self.rageCounter -= 1

    def alterStats( self, stat, num_stages ):
        if stat == 'all' and num_stages == 0:
            for stat in self.statMods:
                self.statMods[stat] = 0
            self.updateStats()

        elif stat not in ['attack','defense','special','speed','accuracy','evasion']:
            print("ERROR: Invalid input for alterStats(). No stat change applied.")

        else:
            if -6 <= self.statMods[stat] + num_stages <= 6:
                self.statMods[stat] += num_stages
                self.updateStats()

    def processStatus( self, status, move ):

        if status in ['freeze', 'paralyze', 'poison', 'toxic', 'burn','sleep'] and not self.hasStatus:
            self.status[status] = True
            self.hasStatus = True

            if status == 'toxic':
                self.statusCounter = 1

            if status == 'sleep':
                if move == 'rest':
                    self.statusCounter = 2
                else:
                    self.statusCounter = np.random.choice([1,2,3,4,5,6,7], 1)

            if status == 'burn':
                self.stats['attack'] = math.floor(self.stats['attack'] / 2)

            if status == 'paralyze':
                self.stats['speed'] = math.floor(self.stats['speed'] / 4)

    def processVolStatus( self, status ):

        if status == 'confuse':
            self.volStatus[status] = True
            self.confusionCounter = np.random.choice([2,3,4,5], 1)

        elif status in ['seed','curse']:
            self.volStatus[status] = True

        elif status == 'flinch' and not self.willFlinch:
            self.willFlinch = True

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

    # Average Durations of effects and attacks
    avg_sleep_turns = 4
    avg_confusion_turns = 3.5
    avg_battle_length = 3


    def __init__( self, mon1, mon2 ):
        if type(mon1) is not Gen1Mon or type(mon2) is not Gen1Mon:
            print("Error: Both Gen1Battle inputs must be of type Gen1Mon.")
        else:
            self.reset( mon1, mon2 )

    def reset( self, mon1, mon2 ):
        self.pokemon = mon1
        self.opponent = mon2
        self.turn = 0

    # There is a chance for an attack to do bonus critical damage.
    # In Generation 1, this is calculated using a Mon's base speed.
    def calculateCritChance( self, mon, move ):
        if moveDex.at[move, 'category'] != 'attack':
            print("ERROR: Status moves do not have critical chances.")
            return 0
        baseSpeed = pokeDex.at[mon.trueName, 'base_speed']

        # Some moves have additional improved critical chance.
        if pd.notna(moveDex.at[move,'crit']):
            critChance = (baseSpeed * 100 / 64) / 100
            #   However, crit chances can't exceed 255/256 due to programming error.
            return min(0.996, critChance)
        else:
            critChance = (baseSpeed * 100 / 512) / 100
            return min(0.996, critChance)


    # A damage multiplier called Same Type Attack Bonus (STAB) is
    #   triggered when a Mon uses a move with the same type as its own.
    def calculateSTAB( self, mon, move ):
        if moveDex.at[move,'type'] in mon.types:
            return 1.5
        else:
            return 1
    
    # Certain types of Pokemon are weak or resistant to certain types of attacks.
    def calculateTypeBonus( self, move, mon ):
        moveType = moveDex.at[move, 'type']
        if pd.notna(mon.types[1]):
            return types.at[moveType,'vs_%s_%s' % (mon.types[0], mon.types[1])]
        else:
            return types.at[moveType,'vs_%s' % mon.types[0]]

    # Depending on a move's typing, we need to pick the corresponding statistics
    #   for the attacking and defending Mons to calculate the move damage.
    def getAttackStat( self, move, mon ):
        moveType = moveDex.at[move,'type']
        if moveType in PHYSTYPES:
            return mon.stats['attack']
        elif moveType in SPECTYPES:
            return mon.stats['special']

    def getDefenseStat( self, move, mon ):
        moveType = moveDex.at[move,'type']
        if moveType in PHYSTYPES:
            if mon.physDefense:
                return mon.stats['defense'] * 2
            else: 
                return mon.stats['defense']
        elif moveType in SPECTYPES:
            if mon.specDefense:
                return mon.stats['special'] * 2
            else:
                return mon.stats['special']

    def getMovePower( self, move ):
        return moveDex.at[move,'power']

    def getMoveAccuracy( self, move ):
        return 1 if move == 'swift' else min(0.996, moveDex.at[move,'accuracy']/100)

    def calculateAccuracy( self, mon, move, opp ):
        acc = self.getMoveAccuracy(move)
        accMod = mon.statStages[mon.statMods['accuracy']]
        evasionMod = opp.evasionStages[opp.statMods['evasion']]
        return acc * accMod * evasionMod


    # Because Pokemon is turn-based, we have to pick who attacks first.
    #   First, we check if one mon uses a priority move. Then, we compare
    #   speeds. Finally, if either of those methods tie, we flip a coin. 
    def monMovesFirst( self, monMove, oppMove ):
        if int(moveDex.at[monMove,'priority']) > int(moveDex.at[oppMove,'priority']):
            return True 
        elif int(moveDex.at[oppMove,'priority']) > int(moveDex.at[monMove,'priority']):
            return False 
        elif self.pokemon.stats['speed'] > self.opponent.stats['speed']:
            return True
        elif self.opponent.stats['speed'] > self.pokemon.stats['speed']:
            return False
        else:
            return np.random.choice(range(2),size=1,replace=False)[0]

    # Used to calculate damage for Psywave, Night Shade, and Seismic Toss.
    def levelDepAttack( self, mon, move, opp, expected=False ):
        if self.calculateTypeBonus(move,opp) == 0:
            return 0
        else:
            # Psywave does between 1 and 1.5x the user's level in damage.
            if move == 'psywave':
                return math.floor(mon.level*0.75) if expected else (random.randrange(1, math.floor(mon.level*1.5)))
            # Night Shade and Seismic Toss do damage equal to the user's level.
            else:
                return mon.level


    # Some moves do a damage amount relative to the user's level. These moves
    #    ignore STAB and type bonuses, BUT they do 0 damage to Pokemon who are
    #    immune to the move's type.
    def fixedAttack( self, move, opp ):
        # Super Fang does half the opponent's current health, rounded down.
        if move == 'super fang':
            return max(1, math.floor(opp.stats['hp'] / 2))
        # Supersonic and Dragon Rage do a fixed damage amount (20, 40 respectively).
        else:
            return float(moveDex.at[move,'power'])  

    def rollHitCount( self, move ):
        if moveDex.at[move, 'hit_distr'] == 'normal':
            return np.random.choice([2,3,4,5], 1, p=[0.375,0.375,0.125,0.125])
        elif moveDex.at[move, 'hit_distr'] == 'double':
            return 2
        else:
            return 1

    def attack( self, mon, move, opp, expected=False ):
        L = float(mon.level)
        AS = float(self.getAttackStat(move, mon))
        if mon.status['burn']:
            AS = math.floor(AS/2)
        P = float(self.getMovePower(move))
        DS = float(self.getDefenseStat(move, opp))
        STAB = float(self.calculateSTAB(mon, move))
        TB = float(self.calculateTypeBonus(move, opp))

        base_dmg = min(((((2*L/5)+2)*(AS/DS)*P)/50),997)+2      
        mod_dmg = math.floor(math.floor(base_dmg*STAB)*(TB*10/10))

        crit_base_dmg = min(((((2*(2*L)/5)+2)*(AS/DS)*P)/50),997)+2
        crit_mod_dmg = math.floor(math.floor(crit_base_dmg*STAB)*(TB*10/10))

        crit_chance = self.calculateCritChance(mon,move)

        if expected==False:
            dmg = crit_mod_dmg if np.random.binomial(1,crit_chance) else mod_dmg
            num_hits = self.rollHitCount(move)

            if dmg == 0 or dmg == 1:
                return math.floor(dmg) * num_hits
            else:
                R = 217 + np.random.choice(range(39),size=1,replace=False)[0]
                return math.floor(dmg * (R/255)) * num_hits
        
        else:
            total = math.floor((1 - crit_chance) * mod_dmg)
            total_crit = math.floor(crit_chance * crit_mod_dmg)
            return (total + total_crit) * moveDex.at[move,'avg_hits']

    def getDamage( self, mon, move, opp, expected=False):
        # Some moves do a variable amount of damage based on the user's level.
        if moveDex.at[move,'subcat'] == 'level_dep':
            return self.levelDepAttack(mon, move, opp, expected=expected)
                
        # Some moves do a fixed amount of damage, ignoring types and STAB.
        elif moveDex.at[move,'subcat'] == 'fixed':
            return self.fixedAttack(move, opp)

        # Some moves instantly KO if they land, but have a low accuracy. To evaluate the
        #   value of these moves, we will return the opponent's max HP, which will then
        #   be multiplied by the accuracy in the pickMove function.
        elif moveDex.at[move,'subcat'] == 'ko':
            return pokeDex.at[opp.trueName, 'hp']

        # Finally, the rest of the moves are calculated in a normal way.
        else:
            # If the opponent is charging Fly or Dig, only certain moves will hit it.
            if (opp.isUnderground) and not (moveDex.at[move, 'hit_dig']):
                return 0
            elif (opp.isAirborne) and not (moveDex.at[move,'hit_fly']):
                return 0
            # And here we have the calculation for every other move.
            else:
                return self.attack(mon, move, opp, expected=expected)


    # This is the default damage calculation for most moves in the game.
    def processAttack( self, mon, move, opp, expected=False, damageOnly=False ):

        if moveDex.at[move, 'subcat'] == 'status_dep' and not opp.status[moveDex.at[move, 'opp_status']]:
            return 0

        attackScore = 0

        dmg = self.getDamage(mon, move, opp, expected=expected)
        acc = self.calculateAccuracy(mon, move, opp)

        attackScore += dmg * acc

        # We also want to account for how many turns the move takes to charge up.
        #    Moves like Fly and Dig aren't checked here because the charge is done 
        #    in a way that protects the user.
        if moveDex.at[move,'subcat'] == 'charge':
            attackScore /= float(moveDex.at[move,'avg_turns'])

        # There is a single move (Hyper Beam) that does not charge up but instead
        #   shoots first with a turn of rest afterwards required. If the move is
        #   expected to kill the next turn, this rest turn is ignored. If the move
        #   will not kill, this rest turn must be accounted for.
        elif (moveDex.at[move,'subcat'] == 'burst') and (attackScore < opp.stats['hp']):
            attackScore /= float(moveDex.at[move,'avg_turns'])

        #   Moves with recoil inflict damage on the user as a percentage of the damage
        #   inflicted, so we have to account for those.
        if pd.notna(moveDex.at[move,'recoil']) and not damageOnly:
            recoil = math.floor(dmg * moveDex.at[move,'recoil'])
            
            # If the recoil would kill the user, its score is made to be zero to ensure 
            # it doesn't pick it.
            if ((mon.stats['hp'] - recoil) <= 0):
                # BUT, if using the move is expected to kill, it will process the move
                # normally, because the user will "win" before they die.
                if attackScore < opp.stats['hp']:
                    attackScore = 0
            else:
                attackScore -= recoil

        # Patchwork solution to encourage Earthquake over Dig, for example.
        #   Want mon to realize that using even a semi-invulnerable two-turn move is more
        #   dangerous than just using a one-turn normal attack.
        if moveDex.at[move, 'subcat'] in ['fly', 'dig']:
            if mon.stats['speed'] < opp.stats['speed'] and opp.knowsSwift != "":
                attackScore -= self.processMove(opp, 'swift', mon, expected=True, damageOnly=True)

        #   This is kind of petty, but we also have to be wary of crash damage, which
        #   in Gen 1 is always 1 HP, lol.
        if pd.notna(moveDex.at[move,'crash']) and not damageOnly:
            attackScore -= 1

        # Next, we account for ways in which the move can affect the user's HP.
        #   "Absorb" type moves heal the user for a percentage of the damage dealt,
        #   so we add the HP the user would heal to the score.
        if (moveDex.at[move,'subcat'] == 'absorb') and not damageOnly:
            exp_heal_amt = math.floor(dmg * acc * moveDex.at[move,'heal'])
            health_diff = pokeDex.at[mon.name,'hp'] - mon.stats['hp']
            if health_diff > exp_heal_amt:
                attackScore += exp_heal_amt
            else:
                attackScore += health_diff

        # Next, we account for status conditions.
        if moveDex.at[move, 'subcat'] != 'status_dep' and pd.notna(moveDex.at[move,'opp_status']) and not damageOnly:
            attackScore += self.processStatusMove(mon, move, opp)

        # Next, we account for status conditions.
        if (pd.notna(moveDex.at[move,'stat']) or pd.notna(moveDex.at[move,'opp_stat'])) and not damageOnly:
            attackScore += self.processStatMove(mon, move, opp)

        return attackScore        



    def hurtItselfInConfusion( self, mon, expected=False ):
        L = mon.level
        AS = self.getAttackStat('tackle', mon)
        P = 40
        DS = self.getDefenseStat('tackle', mon)
        STAB = 1
        TB = 1

        base_dmg = min(((((2*L/5)+2)*(AS/DS)*P)/50),997)+2
        mod_dmg = math.floor(math.floor(base_dmg*STAB)*(TB*10/10))
        if mod_dmg > 1:
            if expected:
                mod_dmg = math.floor(mod_dmg*(236/255))
            else:
                R = 217 + np.random.choice(range(39),size=1,replace=False)[0]
                mod_dmg = math.floor(mod_dmg*(R/255))

        return mod_dmg

    def processStatusMove( self, mon, move, opp ):
        status = moveDex.at[move,'opp_status']
        status_chance = float( str(moveDex.at[move,'opp_status_chance']).strip('%') )/100
        status_score = 0

        # In Gen 1, status effects cannot be inflicted on a Pokemon of the same type as the
        #   move. This applies even to, e.g., Normal Pokemon paralyzes from Body Slam.
        if moveDex.at[move,'type'] in opp.types:
            return 0

        # Poison does 1/16th of the opponent's maximum health per turn, so that's the
        #   factor we multiply by the status chance and the average number of turns per battle.
        if status == 'seed' and not opp.volStatus['seed']:
            status_score += (math.floor(pokeDex.at[opp.name, 'hp'] / 16) * 2 * status_chance * float(self.avg_battle_length/self.turn))

        elif status == 'confuse' and not opp.volStatus['confuse']:
            status_score += self.hurtItselfInConfusion(opp) * (self.avg_confusion_turns/self.turn)

        elif status == 'poison' and 'poison' not in opp.types and not opp.hasStatus:
            status_score += (math.floor(pokeDex.at[opp.name, 'hp'] / 16) * status_chance * float(self.avg_battle_length/self.turn))

        elif status == 'toxic' and 'poison' not in opp.types and not opp.hasStatus:
            if type(self.avg_battle_length/self.turn) is int:
                rangeUpper = (self.avg_battle_length/self.turn) + 1
            else:
                rangeUpper = math.ceil(float(self.avg_battle_length/self.turn))
            status_score += (math.floor(pokeDex.at[opp.name, 'hp'] / 16) * status_chance * sum(range(1,rangeUpper)))

        else:

            if status == 'burn' and not opp.hasStatus:
                status_score += (math.floor(pokeDex.at[opp.name, 'hp'] / 16) * status_chance * float(self.avg_battle_length/self.turn))
                burned_opp = copy.deepcopy(opp)
                burned_opp.status['burn'] == True
                incomingDamage_burned = self.processMove(burned_opp, mon.incomingMove, mon, expected=True, damageOnly=True)
                burnDiff = mon.incomingDamage - incomingDamage_burned
                status_score += burnDiff * float(self.avg_battle_length/self.turn)

            elif status == 'paralyze' and not opp.hasStatus:
                par_turns = self.avg_battle_length
                if mon.stats['speed'] <= opp.stats['speed']:
                    if mon.stats['speed'] == opp.stats['speed']:
                        par_turns += 0.5
                    else:
                        par_turns += 1
                status_score += (mon.incomingDamage * 0.25) * float(par_turns/self.turn)

            elif status == 'sleep' and not opp.hasStatus:
                status_score += self.avg_sleep_turns * mon.incomingDamage

            elif status == 'freeze' and not opp.hasStatus:
                status_score += self.avg_battle_length * mon.incomingDamage
            
            # Similarly, we account for flinch, but only if the user outspeeds its opponent.
            #    If it doesn't, the opponent will never flinch anyway. If the speed is
            #    equal, moving first is a coin flip, so the flinch chance is halved.
            elif status == 'flinch' and (mon.stats['speed'] >= opp.stats['speed']):
                if mon.stats['speed'] == opp.stats['speed']:
                    status_chance /= 2
                status_score += mon.incomingDamage

        acc =  self.calculateAccuracy(mon, move, opp)

        status_mod = status_score * status_chance * acc        
        return math.floor(status_mod)


    def processStatMove( self, mon, move, opp ):
        buff_value = 0

        if pd.notna(moveDex.at[move,'stat']):
            stat = moveDex.at[move,'stat']
            stages = int(moveDex.at[move,'stat_change'])
            acc = self.calculateAccuracy(mon, move, opp)
            
            buffedMon = copy.deepcopy(mon)
            buffedMon.alterStats(stat, stages)

            if stat in ['speed','all'] and mon.stats['speed'] < opp.stats['speed']:
                if buffedMon.stats['speed'] >= opp.stats['speed']:
                    outspeedValue = mon.incomingDamage
                    if buffedMon == opp.stats['speed']:  
                        outspeedValue /= 2
                    buff_value += outspeedValue * (acc)


            if stat in ['attack', 'special', 'all']:

                bestMove = self.pickMove( mon, opp, damageOnly=True)
                bestDamage = min(self.processMove(mon, bestMove, opp, expected=True, damageOnly=True), opp.stats['hp'])

                buffedMove = self.pickMove( buffedMon, opp, damageOnly=True)
                buffedDamage = min(self.processMove(buffedMon, buffedMove, opp, expected=True, damageOnly=True), opp.stats['hp'])

                buff_value += ((buffedDamage - bestDamage) * (acc))


            if stat in ['defense', 'special', 'evasion', 'all']:
                
                incomingDamage = min(mon.incomingDamage, mon.stats['hp'])

                buffedIncomingMove = self.pickMove( opp, buffedMon, damageOnly=True )
                buffedIncomingDamage = min(self.processMove(opp, buffedIncomingMove, buffedMon, expected=True, damageOnly=True), mon.stats['hp'])

                buff_value += ((incomingDamage - buffedIncomingDamage) * (acc))


        debuff_value = 0
        if pd.notna(moveDex.at[move,'opp_stat']):
            stat = moveDex.at[move,'opp_stat']
            stages = int(moveDex.at[move,'opp_stat_change'])
            acc = self.calculateAccuracy( mon, move, opp )
            status_chance = float(str(moveDex.at[move,'opp_stat_chance']).strip('%'))/100

            nerfedOpp = copy.deepcopy(opp)
            nerfedOpp.alterStats(stat, stages)

            if stat in ['speed', 'all'] and mon.stats['speed'] < opp.stats['speed']:

                if nerfedOpp.stats['speed'] >= opp.stats['speed']:
                    outspeedValue = mon.incomingDamage
                    if nerfedOpp == opp.stats['speed']:  
                        outspeedValue /= 2
                    debuff_value += outspeedValue * acc * status_chance


            if stat in ['attack', 'special', 'accuracy', 'all']:

                incomingDamage = min(mon.incomingDamage, mon.stats['hp'])
                
                nerfedIncomingMove = self.pickMove( nerfedOpp, mon, damageOnly=True )
                nerfedIncomingDamage = min(self.processMove( nerfedOpp, nerfedIncomingMove, mon, expected=True, damageOnly=True), mon.stats['hp'])

                debuff_value += (incomingDamage - nerfedIncomingDamage) * acc * status_chance


            if stat in ['defense', 'special', 'all']:

                bestMove = self.pickMove( mon, opp, damageOnly=True)
                bestDamage = min(self.processMove(mon, bestMove, opp, expected=True, damageOnly=True), opp.stats['hp'])

                nerfedOppMove = self.pickMove( mon, nerfedOpp, damageOnly=True)
                nerfedOppDamage = min(self.processMove(mon, nerfedOppMove, nerfedOpp, expected=True, damageOnly=True), opp.stats['hp'])

                debuff_value += (nerfedOppDamage - bestDamage) * (acc) * status_chance

        # print('%s: %s' % (move, buff_value + debuff_value))


        return (buff_value + debuff_value) * float(self.avg_battle_length/self.turn)


    def processConversion( self, mon, opp ):

        convertedMon = copy.deepcopy(mon)
        convertedMon.types = opp.types

        convertedMove = self.pickMove(opp, convertedMon, damageOnly=True)
        convertedDamage = self.processMove(opp, convertedMove, convertedMon, expected=True, damageOnly=True)

        conv_value = (mon.incomingDamage - convertedDamage) * float(self.avg_battle_length/self.turn)
        return conv_value
    
    def transform(self, mon, opp):
        mon.types = opp.types
        for stat in opp.stats:
            if stat != 'hp':
                mon.stats[stat] = opp.stats[stat]
        mon.name = opp.name
        return mon

    def processDefense(self, mon, opp, deftype):

        if (deftype == 'spec_protect' and mon.specDefense) or (deftype == 'phys_protect' and mon.physDefense):
            return 0

        protectedMon = copy.deepcopy(mon)

        if deftype == 'spec_protect':
            protectedMon.specDefense = True
        elif deftype == 'phys_protect':
            protectedMon.physDefense = True

        protectedMove = self.pickMove(opp, protectedMon, damageOnly=True)
        protectedDamage = self.processMove(opp, protectedMove, protectedMon, expected=True, damageOnly=True)

        return (mon.incomingDamage - protectedDamage) * float(self.avg_battle_length/self.turn)

    def processHeal( self, mon, move ):
        # We use unprocessed accuracy because it's a self-applying status move.
        exp_heal_amt = math.floor( self.getMoveAccuracy(move) * pokeDex.at[mon.trueName, 'hp'] * moveDex.at[move,'heal'] )
        health_diff = pokeDex.at[mon.trueName,'hp'] - mon.stats['hp']

        if move == 'rest':
            if health_diff > exp_heal_amt:
                return exp_heal_amt - mon.incomingDamage
            else:
                return health_diff - mon.incomingDamage

        else:
            if health_diff > exp_heal_amt:
                return exp_heal_amt
            else:
                return health_diff


    # Here we will process the incoming move and account for all of the
    #   ways an attack can deal damage.
    def processMove( self, mon, move, opp, expected=False, damageOnly=False ):

        # The flying move Mirror Move copies the opponent's last-used attack.
        if moveDex.at[move,'subcat'] == 'reflect':
            if opp.lastUsedMove in ["", "mirror move"]:
                return 0
            else:
                return self.processMove(mon, opp.lastUsedMove, opp, expected=expected)

        elif moveDex.at[move, 'category'] == 'attack' and moveDex.at[move,'subcat'] not in ['suicide', 'counter', 'reflect','ko', 'rage', 'random']:
            return self.processAttack( mon, move, opp, expected=expected, damageOnly=damageOnly )

        elif not damageOnly:
            if moveDex.at[move, 'subcat'] == 'status':
                return self.processStatusMove( mon, move, opp )

            elif moveDex.at[move, 'subcat'] == 'stat':
                return self.processStatMove( mon, move, opp )

            elif moveDex.at[move, 'subcat'] == 'type_copy':
                return self.processConversion( mon, opp )

            elif moveDex.at[move, 'subcat'] == 'transform':
                return 0
            
            elif moveDex.at[move, 'subcat'] in ['spec_protect', 'phys_protect']:
                return self.processDefense(mon, opp, moveDex.at[move, 'subcat'])

            elif moveDex.at[move, 'subcat'] == 'heal':
                return self.processHeal(mon, move)

        return -1

    # For each move the Pokemon can use, we calculate a heuristic score for the overall value 
    #   of using the move versus a given opponent. We select the move with the highest score.
    def pickMove( self, mon, opp, damageOnly=False, validTypes='' ):

        if validTypes == '':
            validTypes = SPECTYPES + PHYSTYPES

        if not damageOnly:
            mon.incomingMove = self.pickMove(opp, mon, damageOnly=True)
            mon.incomingDamage = self.processMove(opp, mon.incomingMove, mon, expected=True, damageOnly=True)

        killMoves = {}
        killMoveBests = {
            'priority': -2,
            'accuracy': -1
        }

        optimalMove = ""
        maxMoveScore = -1
        for move in learnDex.columns:

            if pd.notna(learnDex.at[mon.name, move]) and move not in ['index','struggle'] and moveDex.at[move,'type'] in validTypes:

                moveScore = 0
                # If we're only considering attacking moves, status moves are skipped.
                if moveDex.at[move,'category'] == 'status' and damageOnly:
                        continue

                if moveDex.at[move,'subcat'] == 'reflect' and damageOnly:
                        continue

                elif moveDex.at[move, 'category'] == 'attack' and moveDex.at[move,'subcat'] in ['suicide', 'counter', 'rampage',
                                                                                                            'rage', 'random']:
                        continue

                score = self.processMove(mon, move, opp, expected=True, damageOnly=damageOnly)

                # At this stage we have an emergency exit clause. If the currently selected
                #   move is Quick Attack, and using it would kill the opponent, the Pokemon
                #   will always use it, because it has increased priority even if the opponent's
                #   speed is higher.
                if (self.processMove(mon, move, opp, expected=True, damageOnly=True) >= opp.stats['hp']):
                    killMoves[move] = score
                    if moveDex.at[move,'priority'] > killMoveBests['priority']:
                        killMoveBests['priority'] = moveDex.at[move,'priority']

                # If this move amounts to be optimal, we update the optimal move.
                if score > maxMoveScore:
                    optimalMove = move
                    maxMoveScore = score

        # While we do calculate the overall best value move, we have an additional clause if
        #   the Mon is able to faint the opponent in this turn that supercedes other decision-making.
        #   This is to prevent a situation where a Mon in a position to win uses a lower-accuracy
        #   or lower-priority move when it's not necessary.
        if len(killMoves) > 0:
            # First we filter for the highest-priority moves:
            killMoves = dict(filter(lambda elem: moveDex.at[elem[0],'priority'] == killMoveBests['priority'], killMoves.items()))

            # Then we sort by accuracy in our new list:
            for move in killMoves:
                acc = self.calculateAccuracy(mon, move, opp)
                if acc > killMoveBests['accuracy']:
                    killMoveBests['accuracy'] = acc

            killMoves = dict(filter(lambda elem: self.calculateAccuracy(mon, elem[0], opp) == killMoveBests['accuracy'], killMoves.items()))

            # Then we return the highest-value move.
            optimalMove = max(killMoves, key=killMoves.get)

        # Finally, we return the optimal move, or return struggle if nothing is picked.
        if optimalMove == "":
            return 'struggle'
        else:
            return optimalMove

    def incrementCounters( self ):
        self.pokemon.increment()
        self.opponent.increment()

    def checkPulse( self, mon, log=False ):
        if mon.stats['hp'] <= 0:
            if(log):
                print("%s fainted!" % mon.trueName)
            return False
        else:
            return True

    def isConfused( self, mon, log=False ):
        if mon.volStatus['confuse'] == True:
            if log:
                print("%s is confused!" % mon.trueName)

            if np.random.choice([0,1], 1):
                confuse_dmg = self.hurtItselfInConfusion( mon )
                mon.stats['hp'] -= confuse_dmg
                if log:
                    print("%s took %s damage in its confusion!" % (mon.trueName, confuse_dmg))
                return True

        return False

    def wakeUp( self, mon, log=False ):
        if log:
            print("%s woke up!" % mon.trueName)
        mon.status['sleep'] = False
        mon.hasStatus = False
        mon.wokeUp = False

    def handlePoison( self, mon, log=False ):
        if mon.status['toxic'] == True:
            poison_dmg = math.floor(pokeDex.at[mon.trueName, 'hp'] / 16)
            mon.stats['hp'] -= poison_dmg
            if log:
                print("%s took %s damage from poison!" % (mon.trueName, poison_dmg))

        elif mon.status['toxic'] == True:
            tox_dmg = math.floor(pokeDex.at[mon.trueName, 'hp'] * mon.statusCounter / 16)
            mon.stats['hp'] -= tox_dmg
            if log:
                print("%s took %s damage from toxin!" % (mon.trueName, tox_dmg))
            if mon.statusCounter < 16:
                mon.statusCounter += 1

    def handleSeed( self, mon, opp, log=False ):
        seedDmg = math.floor(pokeDex.at[mon.trueName, 'hp'] / 16)
        mon.stats['hp'] -= seedDmg
        opp.stats['hp'] += seedDmg
        if log:
            print("%s's leech seed absorbed %s HP from %s!" % (opp.trueName, seedDmg, mon.trueName))

    def handleConfusion( self, mon ):
        mon.confusionCounter -= 1
        if mon.confusionCounter == 0:
            mon.volStatus['confuse'] = False
            mon.confusedNoLonger = True

    def canMove( self, mon, log=False ):
        if mon.status['sleep'] == True:
            if log:
                print("%s is fast asleep!" % mon.trueName)
            if mon.status['sleep'] == True and mon.statusCounter > 0:
                mon.statusCounter -= 1
                if mon.statusCounter == 0:
                    mon.wokeUp = True
            return False

        if mon.status['freeze'] == True:
            if log:
                print("%s is frozen solid!" % mon.trueName)
            return False

        if mon.status['paralyze'] == True and np.random.choice([0,1], 1, p=[0.75, 0.25]):
            if log:
                print("%s is fully paralyzed!" % mon.trueName)
            return False

        if mon.willFlinch == True:
            if log:
                print("%s flinched!" % mon.trueName)
            mon.willFlinch = False
            return False

        if mon.hasToRest == True:
            if log:
                print("%s is still recovering..." % mon.trueName)
            mon.hasToRest = False
            return False

        return True

    def buildingUp( self, mon, monMove, log=False ):

        if moveDex.at[monMove, 'subcat'] == 'charge' and mon.isCharged == False:
            mon.bufferedMove = monMove
            if log:
                print("%s is building up energy!" % mon.trueName)
            mon.isCharged = True
            return True

        elif moveDex.at[monMove, 'subcat'] == 'fly' and mon.isAirborne == False:
            mon.bufferedMove = monMove
            if log:
                print("%s flies up high!" % mon.trueName)
            mon.isAirborne = True
            return True

        elif moveDex.at[monMove, 'subcat'] == 'dig' and mon.isUnderground == False:
            mon.bufferedMove = monMove
            if log:
                print("%s digs underground!" % mon.trueName)
            mon.isUnderground = True
            return True

        return False

    # Here, we account for the simple accuracy check. If the move misses, or is
    #   forced to miss by an opponent state, we of course do not process the move.
    def aMiss( self, mon, monMove, opp, log=False ):
        if not (np.random.binomial(1, self.calculateAccuracy(mon, monMove, opp))) or \
        (opp.isAirborne and pd.isna(moveDex.at[monMove,'hit_fly'])) or \
        (opp.isUnderground and pd.isna(moveDex.at[monMove,'hit_dig'])):
            if log and moveDex.at[monMove,'category'] == 'attack':
                print("...but it missed!")

            elif log and moveDex.at[monMove,'category'] == 'status':
                print("...but it failed!")

            if moveDex.at[monMove, 'subcat'] == 'burst':
                mon.hasToRest = True

            return True
        else:
            return False

    def runTurn( self, mon, monMove, opp, log=False ):

        # First, we trigger flavor text if a previously afflicted
        #   Pokemon is about to shed their status ailment.

        if mon.wokeUp:
            self.wakeUp(mon, log=log)
        
        if mon.confusedNoLonger:
            if log:
                print("%s snapped out of confusion!" % mon.trueName)
            mon.confusedNoLonger = False          

        # Then, we process the main "body" of the turn.

        if self.canMove(mon, log=log):
            # If the Pokemon can move, we have to first check if it hurts itself in confusion.
            if not self.isConfused(mon, log=log) and not self.checkPulse(mon, log=log):
                return
            
            # Then we check if it's executing the first turn of a multi-turn move.
            elif self.buildingUp(mon, monMove, log=log):
                return

            # Otherwise, we run the move live.
            else:
                mon.uses(monMove, log=log)

                if moveDex.at[monMove, 'subcat'] == 'reflect':
                    if opp.lastUsedMove in ["", "mirror move"] and log:
                        print("...but it failed!")
                    else:
                        mon.reflecting = True
                        return self.runTurn(mon, opp.lastUsedMove, opp, log=log)

                elif moveDex.at[monMove, 'subcat'] == 'status_dep' and not opp.status[moveDex.at[monMove, 'opp_status']]:
                    if(log):
                        print("...but it failed!")

                # If, of course, we don't miss the attack...
                elif not self.aMiss( mon, monMove, opp, log=log ):

                    if moveDex.at[monMove,'category'] == 'attack':
                        dmg = self.getDamage(mon, monMove, opp)
                        opp.stats['hp'] -= dmg
                        if(log):
                            print("%s takes %s damage!" % (opp.trueName, dmg))
                        
                        if not self.checkPulse(opp, log=log):
                            return

                        # applying absorb healing
                        if pd.notna(moveDex.at[monMove, 'heal']):
                            recoil = math.floor(dmg * moveDex.at[monMove, 'heal'])
                            mon.stats['hp'] += recoil
                            if log:
                                print("%s absorbs %s HP from %s!" % (mon.trueName, recoil, opp.trueName))

                        # applying recoil   
                        if pd.notna(moveDex.at[monMove, 'recoil']):
                            recoil = math.floor(dmg * moveDex.at[monMove, 'recoil'])
                            mon.stats['hp'] -= recoil
                            if log:
                                print("%s is hit with %s damage of recoil!" % (mon.trueName, recoil))

                        if moveDex.at[monMove, 'subcat'] == 'burst':
                            mon.hasToRest = True


                    # applying self status effects
                    if pd.notna(moveDex.at[monMove, 'status']) and not mon.hasStatus:
                        status = moveDex.at[monMove, 'status']
                        mon.processStatus(status, monMove)
                        if log:
                            print("%s was afflicted with %s!" % (mon.trueName, status))

                    # applying opponent status effects
                    if moveDex.at[monMove, 'subcat'] != 'status_dep' and \
                    pd.notna(moveDex.at[monMove, 'opp_status']) and np.random.binomial(1, float(str(moveDex.at[monMove,'opp_status_chance']).strip('%'))/100):
                        opp_status = moveDex.at[monMove, 'opp_status']
                        if opp_status in ['freeze', 'paralyze', 'poison', 'toxic', 'burn','sleep'] and not opp.hasStatus:
                            opp.processStatus(opp_status, '')
                            if log:
                                print("%s was afflicted with %s!" % (opp.trueName, opp_status))
                        elif opp_status in ['seed','curse','confuse'] and opp.volStatus[opp_status] == False:
                            opp.processVolStatus(opp_status)
                            if log:
                                print("%s was afflicted with %s!" % (opp.trueName, opp_status))
                            
                        else:
                            if moveDex.at[monMove, 'category'] == 'status' and log:
                                print("...but it failed!")

                    # applying buffs
                    if pd.notna(moveDex.at[monMove, 'stat']):
                        stat = moveDex.at[monMove,'stat']
                        stages = moveDex.at[monMove,'stat_change']
                        mon.alterStats(stat, stages)
                        if log:
                            print("%s's %s rose by %s stage(s)!" % (mon.trueName, stat, int(stages)))

                    # applying debuffs
                    if pd.notna(moveDex.at[monMove, 'opp_stat']) and np.random.binomial(1, float(str(moveDex.at[monMove,'opp_stat_chance']).strip('%'))/100):
                        stat = moveDex.at[monMove,'opp_stat']
                        stages = moveDex.at[monMove,'opp_stat_change']
                        opp.alterStats(stat, stages)
                        if log:
                            print("%s's %s fell by %s stages!" % (opp.trueName, stat, -1*int(stages)))

                    if moveDex.at[monMove,'subcat'] == 'heal' and moveDex.at[monMove,'category'] == 'status':
                        heal_amt = math.floor( int(pokeDex.at[mon.trueName, 'hp']) * float(moveDex.at[monMove, 'heal']) )
                        lost_health = int(pokeDex.at[mon.trueName, 'hp']) - mon.stats['hp']
                        mon.stats['hp'] += min(heal_amt, lost_health)
                        if log:
                            print("%s healed for %s points!" % (mon.trueName, min(heal_amt, lost_health)) )

                    if moveDex.at[monMove,'subcat'] == 'phys_protect':
                        mon.physDefense = True
                        if log:
                            print("%s is protected against physical attacks!" % (mon.trueName))

                    if moveDex.at[monMove,'subcat'] == 'spec_protect':
                        mon.specDefense = True
                        if log:
                            print("%s is protected against special attacks!" % (mon.trueName))

                    if moveDex.at[monMove,'subcat'] == 'type_copy':
                        mon.types = opp.types
                        types_str = "%s-%s" % (mon.types[0],mon.types[1]) if pd.notna(mon.types[1]) else mon.types[0]
                        if log:
                            print("%s copied %s's %s type!" % (mon.trueName, opp.trueName, types_str))

                    if moveDex.at[monMove,'subcat'] == 'transform':
                        mon = self.transform(mon, opp)
                        mon.isTransformed = True
                        if log:
                            print("%s transformed into %s!" % (mon.trueName, opp.trueName))

                if moveDex.at[monMove, 'subcat'] == 'charge':
                    mon.isCharged = False
                if moveDex.at[monMove, 'subcat'] == 'fly':
                    mon.isAirborne = False
                if moveDex.at[monMove, 'subcat'] == 'dig':
                    mon.isUnderground = False

        # Finally, we handle the end-of-turn status operations.

        if mon.volStatus['confuse'] == True:
            self.handleConfusion(mon)

        if (mon.status['poison'] or mon.status['toxic']):
            self.handlePoison(mon, log=log)
            if not self.checkPulse(mon, log=log):
                return

        if mon.volStatus['seed']:
            self.handleSeed(mon, opp, log=log)
            if not self.checkPulse(mon, log=log):
                return

        # If a Pokemon was processing a Mirrored move, we disable the flag for that.
        if mon.reflecting == True:
            mon.reflecting = False



    def battle( self, log=False ):
        
        if(log):
            print("====  %s vs. %s  ====" % (self.pokemon.trueName, self.opponent.trueName))

        # Every fight, of course, continues until one Pokemon faints.
        while(self.pokemon.stats['hp'] > 0 and self.opponent.stats['hp'] > 0):
            self.turn += 1

            if(log):
                print("---TURN %s | %s: %s/%s, opponent %s: %s/%s" % \
                    (self.turn, self.pokemon.trueName, self.pokemon.stats['hp'], pokeDex.at[self.pokemon.trueName, 'hp'], \
                        self.opponent.trueName, self.opponent.stats['hp'], pokeDex.at[self.opponent.trueName,'hp']))

            # The challenger picks its highest-value move, unless one is buffered from a previous turn.
            if self.pokemon.bufferedMove != "":
                monMove = self.pokemon.bufferedMove
                self.pokemon.bufferedMove = ""
            else:
                monMove = self.pickMove(self.pokemon, self.opponent)

            # The opponent then does the same.
            if self.opponent.bufferedMove != "":
                oppMove = self.opponent.bufferedMove
                self.opponent.bufferedMove = ""
            else:
                oppMove = self.pickMove(self.opponent, self.pokemon)

            # Then we run the two turns in order of speed priority.
            if self.monMovesFirst(monMove, oppMove):
                self.runTurn( self.pokemon, monMove, self.opponent, log=log )
                if not (self.pokemon.stats['hp'] > 0 and self.opponent.stats['hp'] > 0):
                    break
                self.runTurn( self.opponent, oppMove, self.pokemon, log=log )

            else:
                self.runTurn( self.opponent, oppMove, self.pokemon, log=log )
                if not (self.pokemon.stats['hp'] > 0 and self.opponent.stats['hp'] > 0):
                    break
                self.runTurn( self.pokemon, monMove, self.opponent, log=log )

            if not (self.pokemon.stats['hp'] > 0 and self.opponent.stats['hp'] > 0):
                    break

            self.incrementCounters()

        win = 1 if self.pokemon.stats['hp'] > 0 else -1
        return self.turn * win