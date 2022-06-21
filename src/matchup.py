import pandas as pd
import math

# constant lists for gens 1-3 calculation
SPECTYPES = ['fire', 'water', 'grass', 'electric', 'ice', 'psychic', 'dragon']
PHYSTYPES = ['normal', 'fighting', 'flying', 'poison', 'rock', 'ground', 'bug', 'ghost']

# global variables because passing all this shit between 10 functions is awful
gen = ""
mode = ""
pokedex = ""
movedex = ""
learndex = ""
types = ""


def choose_stat(move):
    # gens 1 has fixed physical/special designations for each type
    if gen == 1:
        attstat = 'special' if movedex.at[move, 'type'] in SPECTYPES else 'attack'
        defstat = 'special' if attstat == 'special' else 'defense'
    # gens 2/3 split special into sp. att and sp. def
    elif gen in range(2, 4):
        attstat = 'sp. att' if movedex.at[move, 'type'] in SPECTYPES else 'attack'
        defstat = 'sp. def' if attstat == 'sp. att' else 'defense'
    # gen 4 introduced phys/spec designations on the move level, not for entire types
    else:
        attstat = 'sp. att' if movedex.at[move, 'category'] == 'special' else 'attack'
        defstat = 'sp. def' if attstat == 'sp. att' else 'defense'

    return attstat, defstat


def get_type(mon):
    if pd.isnull(pokedex.at[mon, 'second_type']):
        montype = "vs_%s" % (pokedex.at[mon, 'first_type'])
    else:
        montype = "vs_%s_%s" % (pokedex.at[mon, 'first_type'], pokedex.at[mon, 'second_type'])
    return montype


# calculates critical hit multiplier for a given pokemon's attack
def crit(mon, move):
    # generation 1 has weird calculations for critical hits involving base speed
    if gen == 1:
        s = pokedex.at[mon, 'speed'] - 28
        if movedex.at[move, 'crit'] == 'high':
            crit_chance = min((4 * s), 255) / 256
        else:
            crit_chance = (s / 2) / 256
    # gen 2 universalized crit chance for all pokemon, keeping high-crit moves
    elif gen == 2:
        if movedex.at[move, 'crit'] == 'high':
            crit_chance = 1 / 4
        else:
            crit_chance = 1 / 16
    # gens 3-5 lower the crit chance of high crit moves by one stage
    elif gen in range(3, 7):
        if movedex.at[move, 'crit'] == 'high':
            crit_chance = 1 / 8
        else:
            crit_chance = 1 / 16
    # gens 7 and 8 introduced super-high crit moves and lowered minimum crit chance
    else:
        if movedex.at[move, 'crit'] == 'super':
            crit_chance = 1 / 2
        elif movedex.at[move, 'crit'] == 'high':
            crit_chance = 1 / 8
        else:
            crit_chance = 1 / 24

    return crit_chance


def dmg(mon, vs_mon, move):
    # to get an attack's damage, we instantiate a few things.
    # first is the type of both the attacking and defending pokemon.
    montype, opptype = get_type(mon), get_type(vs_mon)
    # next is the statistics that will be used for the damage calculations.
    # in most games, attack/defense govern physical attacks, and
    #   special attack/special defense govern special attacks, but
    #   this is not always the case, so we outsource this to the stat fxn.
    attstat, defstat = choose_stat(move)

    # full damage calculations are a little involved:
    #   L - level of attacking mon, in this dataset always 50
    #   m - base attack power of the move
    #   A - the attacking pokemon's relevant attacking stat
    #   D - the defending pokemon's relevant defending stat
    #   c - the percent chance that the attack will be a critical hit
    #   s - STAB, a 1.5x multiplier if attack is same type as attacking pokemon
    #   t - the effectiveness of the move against the defending pokemon's type
    #   hits - the number of times the move hits the opponent on average
    #   acc - the percent chance the move will land at all
    l = 50
    m = int(movedex.at[move, 'power'])
    a = int(pokedex.at[mon, attstat])
    d = int(pokedex.at[vs_mon, defstat])
    c = crit(mon, move)
    s = 1.5 if movedex.at[move, 'type'] in montype else 1
    t = float(types.at[movedex.at[move, 'type'], opptype])
    hits = float(movedex.at[move, 'avg_hits'])
    acc = float(int(movedex.at[move, 'accuracy'])/100)
    # for now, we will do a very rudimentary calculation to account for multiturn attacks
    turns = 1 if movedex.at[move, 'subcat'] == 'rampage' else float(movedex.at[move, 'avg_turns'])

    damage = 0
    # gen 1, unlike other generations, doubles the attacking pokemon's Level for critical hits
    if gen == 1:
        nocrit = (((((2 * l / 5) + 2) * m * (a / d)) / 50) + 2) * s * t * hits * acc / turns
        ifcrit = (((((2 * (2*l) / 5) + 2) * m * (a / d)) / 50) + 2) * s * t * hits * acc / turns
        damage = (nocrit*(1-c)) + (ifcrit*c)
    # in gens 2-5, critical hits simply double the resulting damage calulation
    elif gen in range(2, 6):
        crit_mult = ((1 - c) * 1) + (c * 2)
        damage = (((2 * l / 5 + 2) * m * (a / d)) / 50 + 2) * crit_mult * s * t * hits * acc / turns
    # in gens 6 and onward, critical hits were nerfed to a 1.5x damage multiplier
    else:
        crit_mult = ((1 - c) * 1) + (c * 1.5)
        damage = (((2 * l / 5 + 2) * m * (a / d)) / 50 + 2) * crit_mult * s * t * hits * acc / turns

    # there are no decimal damage counts, so we round the damage up to the nearest int.
    return int(math.ceil(damage))


def pick_move(mon, vs_mon):
    # iterate over list of moves and find optimal damage
    max_dmg = -1
    picked_move = ""
    for move in learndex:
        # skip moves the attacking pokemon cannot learn
        mon_access = str(learndex.at[mon, move])
        if pd.isnull(mon_access):
            continue
        # for now, we will also skip non-attacking moves.
        if movedex.at[move, 'category'] != 'attack':
            continue
        # also temporarily we will skip complicated moves with difficult calculations
        if movedex.at[move, 'subcat'] in ['counter', 'fixed', 'ko', 'suicide', 'level_dep', 'seed', 'random', 'reflect']:
            continue
        # if learnable, checks if it's learnable under current movedex mode
        # NATURAL movesets are indicated by:
        #   1. numbers (learn levels), or
        #   2. GF (grandfathered in from previous evolution)
        # these moves are also included in all other movedexes.
        # RENEWABLE movedexes also include HMs and RTMs,
        #   which just means TMs that can be repeatedly acquired.
        # FULL movedexes include all of the above and regular TMs.
        if (mon_access.isnumeric() or mon_access == "GF" or
                (mode in ['renewable', 'full'] and mon_access in ['HM', 'RTM']) or
                (mode == 'full' and mon_access == "TM")):
            # calculate the damage the attack would inflict on the target
            damage = dmg(mon, vs_mon, move)
            # update the optimal move damage if this is the new maximum
            if damage > max_dmg:
                max_dmg = damage
                picked_move = move

    return picked_move, int(max_dmg)


def matchup(mon, vs_mon):
    # determine optimal moves for both pokemon
    move, dmg = pick_move(mon, vs_mon)
    print("%s chooses %s vs %s" % (mon, move, vs_mon))
    opp_move, opp_dmg = pick_move(vs_mon, mon)
    print("%s chooses %s vs %s" % (vs_mon, opp_move, mon))

    # instantiate turn counter and pokemon HP pools
    turns = 0
    hp, opp_hp = pokedex.at[mon, 'hp'], pokedex.at[vs_mon, 'hp']
    # turn order is normally based on the speed stats of each pokemon, but...
    turn = True if pokedex.at[mon, 'speed'] > pokedex.at[vs_mon, 'speed'] else False
    # ...some moves always go first...
    if move == 'quick attack' and opp_move != 'quick attack':
        turn = True
    elif opp_move == 'quick attack' and move != 'quick attack':
        turn = False
    # ...unless both pokemon use priority moves, in which case it defaults to speed again
    elif move == 'quick attack' and opp_move == 'quick attack':
        turn = True if pokedex.at[mon, 'speed'] > pokedex.at[vs_mon, 'speed'] else False
    # let them wail on each other until somebody dies
    while hp > 0 and opp_hp > 0:
        # first pokemon's turn
        if (turn):
            turn_dmg = min(dmg, opp_hp)
            opp_hp -= turn_dmg
            # some moves have recoil inflicted back onto the attacker.
            if pd.notna(movedex.at[move, 'recoil']):
                hp -= int(math.ceil(float(movedex.at[move, 'recoil']) * turn_dmg))
            # other moves absorb a portion of the damage they inflict.
            if pd.notna(movedex.at[move, 'heal']):
                heal = max(1, int(math.ceil(float(movedex.at[move, 'heal']) * turn_dmg)))
                hp += heal
        # second pokemon's turn
        else:
            turn_dmg = min(opp_dmg, hp)
            hp -= opp_dmg
            # recoil calculations
            if pd.notna(movedex.at[opp_move, 'recoil']):
                opp_hp -= int(math.ceil(float(movedex.at[opp_move, 'recoil']) * turn_dmg))
            # absorb calculations
            if pd.notna(movedex.at[opp_move, 'heal']):
                heal = max(1, int(math.ceil(float(movedex.at[opp_move, 'heal']) * turn_dmg)))
                opp_hp += heal
        # flips toggle flag so the other pokemon has next turn
        turn = not turn
        turns += 1

    # determine winner
    r = 1 if opp_hp <= 0 else -1
    return r * turns


def generate():
    # instantiate dictionary of matchup results
    matchups = {}

    # iterate over each pokemon in the game
    for mon, row in pokedex.iterrows():
        # create the list of matchup results for the mon
        matchups[mon] = {}

        # iterate through pokemon DB for matchup opponents
        for vs_mon, row2 in pokedex.iterrows():
            # if pokemon is facing itself, instantly call matchup a draw
            if mon == vs_mon:
                matchups[mon][mon] = '-'
                continue

            # calculate results of matchup
            matchups[mon][vs_mon] = matchup(mon, vs_mon)

    return matchups


if __name__ == '__main__':
    # gen = int(input('Which generation? Please enter a number 1-8:\n'))
    # if gen == 1:
    #     g = 'rby'
    # elif gen == 2:
    #     g = 'gsc'
    # elif gen == 3:
    #     g = input('Which Gen3 games?\n'
    #               '\tRSE - Ruby, Sapphire, and Emerald\n'
    #               '\tFRLG - FireRed and LeafGreen\n'
    #               '\tCOL - Pokemon Colosseum\n'
    #               '\tXD - Pokemon XD: Gale of Darkness\n'
    #               ).lower()
    # elif gen == 4:
    #     g = input('Which Gen4 games?\n'
    #               '\tDPP - Diamond, Pearl, and Platinum\n'
    #               '\tHGSS - HeartGold and SoulSilver\n'
    #               ).lower()
    # elif gen == 5:
    #     g = input('Which Gen5 games?\n'
    #               '\tBW - Black and White\n'
    #               '\tBW2 - Black 2 and White 2\n'
    #               ).lower()
    # elif gen == 6:
    #     g = input('Which Gen6 games?\n'
    #               '\tXY - X and Y\n'
    #               '\tORAS - OmegaRuby and AlphaSapphire\n'
    #               ).lower()
    # elif gen == 7:
    #     g = input('Which Gen7 games?\n'
    #               '\tSM - Sun and Moon\n'
    #               '\tUSUM - Ultra Sun and Ultra Moon\n'
    #               '\tLGPE - Lets Go Pikachu! and Lets Go Eevee!\n'
    #               ).lower()
    # elif gen == 8:
    #     g = input('Which Gen8 games?\n'
    #               '\tSwSh - Sword and Shield\n'
    #               '\tSSIA - Sword and Shield + Isle of Armor DLC\n'
    #               '\tBDSP - BrilliantDiamond and ShiningPearl\n')
    # else:
    #     print('Please try again.')
    #
    # mode = int(input('Which movedex would you like to use?\n'
    #                  '1 - natural movesets only\n'
    #                  '2 - natural movesets + HMs + renewable TMs\n'
    #                  '3 - natural movesets + all TMs\n'))
    # if mode == 1:
    #     mode = 'natural'
    # elif mode == 2:
    #     mode = 'renewable'
    # else:
    #     mode = 'full'
    g = 'rby'
    gen = 1
    mode = 'renewable'

    pokedex = pd.read_csv('data/%s/%s_mons.csv' % (g.lower(), g.lower()))
    pokedex = pokedex.drop('index', axis=1).set_index('mon_name')
    movedex = pd.read_csv('data/%s/%s_movedex.csv' % (g.lower(), g.lower()))
    print(movedex)
    movedex = movedex.set_index('move')
    learndex = pd.read_csv('data/%s/%s_move_access.csv' % (g.lower(), g.lower()))
    learndex = learndex.drop('index', axis=1).set_index('mon_name')
    if gen == 1:
        types = pd.read_csv('data/gen1types_expanded.csv')
    if gen in range(2, 6):
        types = pd.read_csv('data/gens2-5types_expanded.csv')
    elif gen in range(6, 9):
        types = pd.read_csv('data/gens6-8types_expanded.csv')

    types = types.set_index('off_type')

    print(movedex)

    # calculate results for each pokemon matchup in the prompted game
    results = generate()

    # save results of matchup data to csv
    res_name = 'results/%s/%s_matchups_%s.csv' % (g.lower(), g.lower(), mode)
    results = pd.DataFrame.from_dict(results)
    results.transpose().to_csv(res_name)
    print('Results saved to %s' % (res_name))
