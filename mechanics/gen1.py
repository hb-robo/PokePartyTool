import numpy as np
import pandas as pd
import random
import math

# constant lists for gens 1-3 calculation
SPECTYPES = ['fire', 'water', 'grass', 'electric', 'ice', 'psychic', 'dragon']
PHYSTYPES = ['normal', 'fighting', 'flying', 'poison', 'rock', 'ground', 'bug', 'ghost']

# import data relevant to the generation
pokeDex = pd.read_csv('../data/rby/rby_mons.csv')
moveDex = pd.read_csv('../data/rby/rby_movedex.csv')
learnDex = pd.read_csv('../data/rby/rby_move_access.csv')
types = pd.read_csv('../data/gen1types_expanded.csv')

def calculateCritChance(monName, moveName):
    baseSpeed = pokeDex[monName][baseSpeed]
    if moveDex[moveName]['extra_crit']:
        critChance = (baseSpeed * 100 / 512) / 100
        return min(0.996, critChance) # can't exceed 255/256 due to programming error
    else:
        critChance = (baseSpeed * 100 / 64) / 100
        return min(0.996, critChance)

def calculateSTAB(monName, moveName,pokeDex=pokeDex,moveDex=moveDex):
    if pokeDex[monName]['type'] == moveDex[moveName]['type']:
        return 1.5
    else:
        return 1

def calculateTypeBonus(moveName, oppName,pokeDex=pokeDex,moveDex=moveDex):
    moveType = moveDex[moveName]['type']
    oppType = pokeDex[oppName]['type']
    if len(oppType) == 1:
        return types[moveType]['vs_%s' % oppType]
    else: # opponent has two types
        return types[moveType]['vs_%s_%s' % (oppType[0], oppType[1])]

def getAttackStat(moveName, monName):
    moveType = moveDex[moveName]['type']
    if moveType in PHYSTYPES:
        return pokeDex[monName]['lvl50_attack']
    elif moveType in SPECTYPES:
        return pokeDex[monName]['lvl50_special']

def getDefenseStat(moveName, monName):
    moveType = moveDex[moveName]['type']
    if moveType in PHYSTYPES:
        return pokeDex[monName]['lvl50_defense']
    elif moveType in SPECTYPES:
        return pokeDex[monName]['lvl50_special']

def getMovePower(moveName, moveDex=moveDex):
    return moveDex[moveName]['power']

def calculateDamage(monName, moveName, oppName, level):
    if np.random.binomial(1,calculateCritChance(monName,moveName)):
        L = level * 2
    else:
        L = level
    AS = getAttackStat(moveName, monName)
    P = getMovePower(moveName)
    DS = getDefenseStat(moveName, monName)
    STAB = calculateSTAB(monName, moveName)
    TB = calculateTypeBonus(moveName, oppName)

    base_dmg = min(((((2*L/5)+2)*(AS/DS)*P)/50),997)+2
    mod_dmg = math.floor(math.floor(base_dmg*STAB)*(TB*10/10))

    if mod_dmg == 0 or mod_dmg == 1:
        return mod_dmg
    else:
        R = random.randRange(217,256)
        return math.floor(mod_dmg*(R/255))

def pickMove(monName, oppName):
    optimalMove = ""
    maxMoveScore = 0
    for move in learnDex[monName]:
        if not np.nan(move):
            damage = calculateDamage(monName, str(move), oppName, level=50)
            move_score = damage * move['accuracy']  / move['num_turns']
            
