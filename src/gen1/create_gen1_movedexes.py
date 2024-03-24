"""
This script creates the movedexes for Gen 1 games. The movedexes are stored as
JSON files in the data/json/gen1/ directory. The movedexes are created by
parsing data from data/archive/rby_movedex.csv, which was a manual attempt at making
move effects parseable for the purposes of the battle engine. Similar attempts have
been made for other projects but they all use the most moden variant of each move,
which drastically misrepresents the quirks of Generation 1 combat.

NOTE: This describes the moves in isolation, and does not account for which 
Pokemon learn them. That is handled in the "Learndex."

There are two variants of the movedexes in Gen 1, and it really comes down to
which version of the move Blizzard is present. In the original Red/Green games,
PM Blue, and PM Yellow (in the base game), Blizzard has a 30.1% chance to freeze
the target. This was changed to 10.2% in the international releases of the game,
as well as all of the Stadium spin-offs and the Colosseum2 Link Battle modes in
Pocket Monsters Yellow. In Pokemon Yellow (Intl.), Blizzard always has the lowered
freeze chance. This is the only difference between the two movedexes.

Movedex (30.1% Freeze) applies to:
* Pocket Monsters Red, Green, and Blue
* Pocket Monsters Yellow in all modes except Colosseum2 Link Battle.

Movedex (10.2% Freeze) applies to:
* Pocket Monsters Stadium and Stadium 2
* Pokemon Red & Blue
* Pokemon Yellow in all modes.
* Pokemon Stadium (Intl.)

There is also a difference in how Sleep and the effects of Wrap are handled in
certain Generation 1 games, but ultimately this comes down to the implementation
of the combat engines and is not a property of any move or their effect chances.
As such, they are not documented here.
"""


import json
import os
import pandas as pd
import src.gen1.gen1_constants as constants

intl_movedex = pd.read_csv("../data/archive/gen1/csv/rby_movedex.csv")

gen1_og_movedex = []
gen1_rev_movedex = []


def capitalize_words(string):
    """
    This function capitalizes the first letter of each word in a string.
    I need it because I thought lowercase was really cool in 2021.
    """
    return ' '.join([word.capitalize() for word in string.split(' ')])


for _, row in intl_movedex.iterrows():

    if row['move'] == 'Blizzard':
        # account for version differences
        continue

    # Static move data and elements
    move = {
        'move_name': capitalize_words(row['move']),
        'type': capitalize_words(row['type']),
        'category': capitalize_words(row['category']),
        'power': int(row['power']) if(row['power']) else '-',
        'accuracy': '-' if(row['move'] in ['bide', 'swift']) else int(row['accuracy']),
        'pp': int(row['pp']),
        'priority': int(row['priority']),
        'hit_fly': bool(row['hit_fly']),
        'hit_dig': bool(row['hit_dig'])
    }

    # Attack-specific properties
    if row['category'] == 'attack':
        move['crit_rate'] = 8 if(row['crit'] == 'high') else 1,
        move['crash'] = bool(row['crash']),

        if row['recoil']:
            move['recoil'] = float(row['recoil'])
        if row['counter']:
            move['counter'] = float(row['recoil'].strip('%')) / 100.0

        # Number of hits / hit distribution
        match row['hit_distr']:
            case 'normal':
                move['hit_distribution'] = constants.MULTI_HIT_DISTRIBUTION
            case 'double':
                move['hit_distribution'] = {2: 1.000}
            case _:
                move['hit_distribution'] = {1: 1.000}

    # Status condition effects
    if row['status']:
        move['effects'].extend([
            {
                'effect': "non-volatile status" if \
                    row['status'].capitalize() in constants.NON_VOLATILE_STATUS_CONDITIONS \
                    else "volatile status",
                'target': 'self',
                'status_name': capitalize_words(row['status']),
                'chance': 1.000
            }
        ])
    if row['opp_status']:
        move['effects'].extend([
            {
                'effect': "non-volatile status" if \
                    row['opp_status'].capitalize() in constants.NON_VOLATILE_STATUS_CONDITIONS \
                    else "volatile status",
                'target': 'opponent',
                'status_name': capitalize_words(row['status']),
                'chance': 1.000 if not row['opp_status_chance'] \
                    else float(row['opp_status_chance'].strip('%')) / 100.0
            }
        ])
    # Stat changes
    if row['stat']:
        move['effects'].extend([
            {
                'effect': 'stat',
                'target': 'self',
                'stat_name': capitalize_words(row['stat']),
                'stat_change': int(row['stat_change']),
                'chance': 1.000
            }
        ])
    if row['opp_stat']:
        move['effects'].extend([
            {
                'effect': 'stat',
                'target': 'opponent',
                'stat_name': capitalize_words(row['opp_stat']),
                'stat_change': int(row['opp_stat_change']),
                'chance': 1.000 if not row['opp_stat_chance'] \
                    else float(row['opp_stat_chance'].strip('%')) / 100.0

            }
        ])
    # Healing effects
    if row['heal']:
        move['effects'].extend([
            {
                'effect': 'heal',
                'target': 'self',
                'heal_pct': float(row['heal']),
                'chance': 1.000
            }
        ])