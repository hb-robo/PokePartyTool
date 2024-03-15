"""
One-stop shop for data analysis centered around Pokemon types.

Rough analysis outline:
* Type advantages on paper
* All possible type matchups (on paper)
* Type advantages in game
* All possible type matchups (in game)
* BST by Type
    * Individual base stats by Type
* Move access per Type - stacked bar chart(S)?
    * Natural learnsets
    * TM/HM access
    * Specific move types, ie. status, damaging, buff, debuff
    * Factor in single type / double type
* Move access per "TypeType" ie phys/spec
* Move attributes per Type/TypeType
    * Damage distribution
    * Accuracy distribution
    * Presence of buff effect
    * Presence of debuff effect
    * Presence of status effect
    * Presence of recoil
    * Presence of flinch chance
    * Presence of self-obliteration
* 3D bar chart: move frequency by type and status effect applied
"""
import pandas as pd
import duckdb

g1typeinteractions = pd.read_csv(
    'data/gen1/csv/gen1_type_interactions.csv'
)
g1typeinteractions_expanded = pd.read_csv(
    'data/gen1/csv/gen1_expanded_type_interactions.csv'
)

"""
PART 1: Naive Analysis
* Assumes equal distribution of type frequencies in available Pokemon.
* Assumes equal stats and equivalent move access for each type.
* Assumes attacking moves are limited to the typing of the Pokemon.
"""

# Single-Type Advantages
offensive_type_advantages = duckdb.query(
    '''
    SELECT off_type,
        SUM(CASE g.multiplier WHEN 0.0 THEN 1 ELSE 0 END)::int as "0.0x",
        SUM(CASE g.multiplier WHEN 0.5 THEN 1 ELSE 0 END)::int as "0.5x",
        SUM(CASE g.multiplier WHEN 1.0 THEN 1 ELSE 0 END)::int as "1.0x",
        SUM(CASE g.multiplier WHEN 2.0 THEN 1 ELSE 0 END)::int as "2.0x"
    from g1typeinteractions g
    group by off_type;
    '''
).df()
print(offensive_type_advantages)
# TODO: dataviz stuff

defensive_type_advantages = duckdb.query(
    '''
    SELECT def_type,
        SUM(CASE g.multiplier WHEN 0.0 THEN 1 ELSE 0 END)::int as "0.0x",
        SUM(CASE g.multiplier WHEN 0.5 THEN 1 ELSE 0 END)::int as "0.5x",
        SUM(CASE g.multiplier WHEN 1.0 THEN 1 ELSE 0 END)::int as "1.0x",
        SUM(CASE g.multiplier WHEN 2.0 THEN 1 ELSE 0 END)::int as "2.0x"
    from g1typeinteractions g
    group by def_type;
    '''
).df()
print(defensive_type_advantages)
# TODO: dataviz stuff

# Something about value OF strengths (how rare they are) - the higher the better
# mean( 1/str_freq ) for each str - average value of strengths
# sum( 1/str_freq ) for each str - total value of strengths

# Value of weaknesses (how rare they are)
# mean( 1/weak_freq ) for each str - average value of weaknesses
# sum( 1/weak_freq ) for each str - total value of weaknesses


# Single-Type and Double-Type Advantages
expanded_off_type_advantages = duckdb.query(
    '''
    SELECT off_type,
        SUM(CASE ge.multiplier WHEN 0.0 THEN 1 ELSE 0 END)::int as "0.0x",
        SUM(CASE ge.multiplier WHEN 0.25 THEN 1 ELSE 0 END)::int as "0.25x",
        SUM(CASE ge.multiplier WHEN 0.5 THEN 1 ELSE 0 END)::int as "0.5x",
        SUM(CASE ge.multiplier WHEN 1.0 THEN 1 ELSE 0 END)::int as "1.0x",
        SUM(CASE ge.multiplier WHEN 2.0 THEN 1 ELSE 0 END)::int as "2.0x",
        SUM(CASE ge.multiplier WHEN 4.0 THEN 1 ELSE 0 END)::int as "4.0x"
    from g1typeinteractions_expanded ge
    group by off_type;
    '''
).df()
print(expanded_off_type_advantages)
# TODO: dataviz stuff

expanded_def_type_advantages = duckdb.query(
    '''
    SELECT def_type1, def_type2,
        SUM(CASE ge.multiplier WHEN 0.0 THEN 1 ELSE 0 END)::int as "0.0x",
        SUM(CASE ge.multiplier WHEN 0.25 THEN 1 ELSE 0 END)::int as "0.25x",
        SUM(CASE ge.multiplier WHEN 0.5 THEN 1 ELSE 0 END)::int as "0.5x",
        SUM(CASE ge.multiplier WHEN 1.0 THEN 1 ELSE 0 END)::int as "1.0x",
        SUM(CASE ge.multiplier WHEN 2.0 THEN 1 ELSE 0 END)::int as "2.0x",
        SUM(CASE ge.multiplier WHEN 4.0 THEN 1 ELSE 0 END)::int as "4.0x"
    from g1typeinteractions_expanded ge
    group by def_type1, def_type2;
    '''
).df()
print(expanded_def_type_advantages)
# TODO: dataviz stuff

"""
PART 2: Partially-Naive Analysis
* Recognizes actual distribution of types in Kanto Pokedex
* Recognizes actual base stats of available Pokemon
* Assumes equivalent movepools between types
* Assumes attacking moves are limited to the typing of the Pokemon.
"""


"""
PART 3: Fully-Informed Analysis
* Recognizes actual types, stats, and movepools of in-game Pokemon
"""
