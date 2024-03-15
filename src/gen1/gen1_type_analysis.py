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
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.models import HoverTool, ColumnDataSource, Label, Range1d, FixedTicker
from bokeh.layouts import column, gridplot
import gen1_constants as constants

g1typeinteractions = pd.read_csv(
    '../../data/gen1/csv/gen1_type_interactions.csv'
)
g1typeinteractions_expanded = pd.read_csv(
    '../../data/gen1/csv/gen1_expanded_type_interactions.csv'
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
offensive_type_advantages.index = offensive_type_advantages['off_type']
# print(offensive_type_advantages)

"""
Below might be unnecessary, can just use #Types.
"""
# off_type_adv_y_max = duckdb.query(
#     '''
#     SELECT 
#         CASE
#             WHEN max_0 >= max_0_5 AND max_0 >= max_1 AND max_0 >= max_2 THEN max_0
#             WHEN max_0_5 >= max_1 AND max_0_5 >= max_2 THEN max_0_5
#             WHEN max_1 >= max_2 THEN max_1
#             ELSE max_2
#         END AS max
#     FROM (
#         SELECT
#             MAX(ota."0.0x") as max_0,
#             MAX(ota."0.5x") as max_0_5,
#             MAX(ota."1.0x") as max_1,
#             MAX(ota."2.0x") as max_2
#         from offensive_type_advantages ota
#     ) t1;
#     '''
# ).df()
# ota_ymax = off_type_adv_y_max.loc[0, 'max']


off_types = sorted(offensive_type_advantages['off_type'])
categories = offensive_type_advantages.columns[1:].tolist()
bar_colors = [constants.TYPE_COLORS[off_type] for off_type in off_types]

num_cols = 4
grid = []
row = []

plots = []
for off_type in off_types:
    data = offensive_type_advantages[(offensive_type_advantages['off_type'] == off_type)]

    source = ColumnDataSource(data=dict(
        x=categories,
        top = data.values[0].tolist()[1:],
    ))

    p = figure(x_range=categories, height=200, width=400, y_range=Range1d(0, len(constants.TYPES)), title=off_type)
    p.yaxis.ticker = FixedTicker(ticks=[x for x in list(range(0, len(constants.TYPES)+1)) if x % 5 == 0])
    p.vbar(x='x', top = 'top', width=0.9,color=constants.TYPE_COLORS[off_type], source=source)

    label = Label(x=-10, y=0, text=off_type, text_font_size='10pt')
    p.add_layout(label)
        
    hover = HoverTool(tooltips=[
        ("Count", "@top")
    ])
    p.add_tools(hover)

    row.append(p)
    if len(row) == num_cols:
        grid.append(row)
        row = []

if row:
    grid.append(row)

show(gridplot(grid))

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
