import pandas as pd
import numpy as np
import random
import gen1
import math

# constant lists for gens 1-3 calculation
SPECTYPES = ['fire', 'water', 'grass', 'electric', 'ice', 'psychic', 'dragon']
PHYSTYPES = ['normal', 'fighting', 'flying', 'poison', 'rock', 'ground', 'bug', 'ghost']

# import data relevant to the generation
pokeDex = pd.read_csv('../data/gsc/gsc_mons.csv')
moveDex = pd.read_csv('../data/gsc/gsc_movedex.csv')
learnDex = pd.read_csv('../data/gsc/gsc_move_access.csv')
types = pd.read_csv('../data/gen2types_expanded.csv')

# Critical chances have been severely nerfed in Generation 2. They are no
#   longer calculated using the base speed stat of the Pokemon like in
#   Generation 1. Now there is a flat crit chance of 1/16, or 1/4 if the 
#   move has a higher critical hit chance.
def calculateCritChance(moveName):
    if moveDex[moveName]['extra_crit']:
        return 0.25
    else:
        return 0.0625

# Physical and special types still exist in Generation 2.
# However, Special has been split into "Special Attack" and "Special Defense."

# When attacking with a special move, the calculation uses "Special Attack."
def getAttackStat(moveName, monName):
    moveType = moveDex[moveName]['type']
    if moveType in PHYSTYPES:
        return pokeDex[monName]['lvl50_attack']
    elif moveType in SPECTYPES:
        return pokeDex[monName]['lvl50_sp_attack']

# When defending from a special move, the calculation uses "Special Defense."
def getDefenseStat(moveName, monName):
    moveType = moveDex[moveName]['type']
    if moveType in PHYSTYPES:
        return pokeDex[monName]['lvl50_defense']
    elif moveType in SPECTYPES:
        return pokeDex[monName]['lvl50_sp_defense']

# Damage calculation is still largely the same as in Generation 1.
def calculateDamage(monName, moveName, oppName, level):
    # Although critical chances are lowered, crit damage is still applied by
    #   doubling the level of the attacking Pokemon.
    if np.random.binomial(1,calculateCritChance(monName,moveName)):
        L = level * 2
    else:
        L = level
    AS = getAttackStat(moveName, monName)
    DS = getDefenseStat(moveName, monName)
    P = gen1.getMovePower(moveName, moveDex=moveDex)

    base_dmg = min(((((2*L/5)+2)*(AS/DS)*P)/50),997)+2

    STAB = gen1.calculateSTAB(monName, moveName, pokeDex=pokeDex, moveDex=moveDex)
    TB = gen1.calculateTypeBonus(moveName, oppName, pokeDex=pokeDex, moveDex=moveDex)

    mod_dmg = math.floor(math.floor(base_dmg*STAB)*(TB*10/10))

    if mod_dmg == 0 or mod_dmg == 1:
        return mod_dmg
    else:
        R = random.randRange(217,256)
        return math.floor(mod_dmg*(R/255))