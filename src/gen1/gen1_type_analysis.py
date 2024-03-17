"""
One-stop shop for data analysis centered around Pokemon types.
Applies to:
* Pocket Monsters R/G/B/Y
* Pokemon R/B/Y
* Pocket Monsters Stadium 1/2
* Pokemon Stadium

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
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, ColumnDataSource, Range1d, FixedTicker, Div
from bokeh.layouts import gridplot
from src.gen1 import gen1_constants as constants

g1typeinteractions = pd.read_csv(
    '/data/gen1/csv/gen1_type_interactions.csv'
)
g1typeinteractions_expanded = pd.read_csv(
    'data/gen1/csv/gen1_expanded_type_interactions.csv'
)

def save_plot_as_html_js_snippets(path_and_filename, plot_figure):
    """
    Save a Bokeh plot as in HTML/JS snippet format for easy webpage import.

    Parameters:
    - path_and_filename (str): The path and name of the HTML file to save.
    - plot_figure (bokeh.plotting.Figure): The Bokeh plot to save.
    """
    script, div = components(plot_figure)
    with open(f'{path_and_filename}_script.js', 'w', encoding='utf8') as f:
        f.write(script)

    with open(f'{path_and_filename}_div.html', 'w', encoding='utf8') as f:
        f.write(div)


# =============================================================================
# PART 1: Naive Analysis
# * Assumes equal distribution of type frequencies in available Pokemon.
# * Assumes equal stats and equivalent move access for each type.
# * Assumes attacking moves are limited to the typing of the Pokemon.
# =============================================================================

def generate_offensive_interaction_plot():
    """
    Generate a plot showing each type's distribution of offensive interactions.
    """
    offensive_type_advantages = duckdb.query(
        '''
        SELECT off_type,
            SUM(CASE g.multiplier WHEN 0.0 THEN 1 ELSE 0 END)::int as "0.0x",
            SUM(CASE g.multiplier WHEN 0.5 THEN 1 ELSE 0 END)::int as "0.5x",
            SUM(CASE g.multiplier WHEN 1.0 THEN 1 ELSE 0 END)::int as "1.0x",
            SUM(CASE g.multiplier WHEN 2.0 THEN 1 ELSE 0 END)::int as "2.0x",
            AVG(g.multiplier) as avg_multiplier
        from g1typeinteractions g
        group by off_type
        order by AVG(g.multiplier) desc;
        '''
    ).df()
    offensive_type_advantages.index = offensive_type_advantages['off_type']
    # print(offensive_type_advantages)

    title = Div(text="<h2>Offensive Interaction Distribution By Type</h2>")

    off_types = offensive_type_advantages['off_type'].tolist()
    categories = offensive_type_advantages.columns[1:-1].tolist() # exclude off_type and avg_multiplier

    num_cols = 4
    grid = []
    row = []
    for off_type in off_types:
        data = offensive_type_advantages[(offensive_type_advantages['off_type'] == off_type)]

        source = ColumnDataSource(data=dict(
            x=categories,
            top = data.values[0].tolist()[1:-1],
        ))
        ptitle = f"{off_type}:   {data['avg_multiplier'].values[0]:.3f}x Avg. Off. Mult."
        p = figure(
            x_range=categories,
            y_range=Range1d(0, len(constants.TYPES)),
            height=200, width=400,
            title=ptitle)
        p.yaxis.ticker = FixedTicker(ticks=[x for x in range(0, len(constants.TYPES)+1, 5)])
        p.vbar(x='x', top='top', width=0.9, color=constants.TYPE_COLORS[off_type], source=source)

        hover = HoverTool(tooltips=[
            ("Count", "@top")
        ])
        p.add_tools(hover)

        row.append(p)
        if len(row) == num_cols:
            grid.append(row)
            row = []

    if row:
        row.append(Div(
            text="<h3>0.0x: Immune, 0.5x: Resistant, 1.0x: Neutral, 2.0x: Weak</h3> \
                <p>Assumes no double-types, equal type distribution, equal Pokemon stats and equivalent movepools per type</p>"
        ))
        grid.append(row)

    grid.insert(0, [title])
    # show(gridplot(grid))
    save_plot_as_html_js_snippets('docs/gen1/charts/gen1_offensive_interaction_plot', gridplot(grid))


def generate_defensive_interaction_plot():
    """
    Generate a plot showing each type's distribution of defensive interactions.
    """
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
def generate_expanded_offensive_interaction_plot():
    """
    Generate a plot showing each type's distribution of offensive interactions
    against both single- and double-typed defenders.
    """
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


def generate_expanded_defensive_interaction_plot():
    """
    Generate a plot showing each unique single- and double-type combination's
    distribution of defensive interactions against single-type attacks.
    """
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

# =============================================================================
# PART 2: Partially-Naive Analysis
# * Recognizes actual distribution of types in Kanto Pokedex
# * Recognizes actual base stats of available Pokemon
# * Assumes equivalent movepools between types
# * Assumes attacking moves are limited to the typing of the Pokemon.
# =============================================================================


# =============================================================================
# PART 3: Fully-Informed Analysis
# * Recognizes actual types, stats, and movepools of in-game Pokemon
# =============================================================================



if __name__ == '__main__':
    generate_offensive_interaction_plot()
    generate_defensive_interaction_plot()
    generate_expanded_offensive_interaction_plot()
    generate_expanded_defensive_interaction_plot()
