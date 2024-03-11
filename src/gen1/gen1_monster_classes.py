import pandas as pd
from src.parent_classes import Pokemon
import json

pokeDex = pd.read_csv('data/rby/rby_pokedex.csv', index_col='mon_name')

"""
Classes to represent Pokemon from Generation 1 games.
Contains physical attributes, default stats, type data, and movepool,
as well as "live" HP, stats, status, etc.
"""


class PMRG_Pokemon(Pokemon):

    def __init__(self, name, level=50):
        self.name = name
        self.level = level
        # Grab static values from corresponding Pokedex
        self.pokedex_path = '../../data/gen1/json/pm_red_green_pokedex.json'
        self.getDexEntry()
        
        self.lastUsedMove = ''
        self.stat_modifiers = {k: 0 for k in self.stats.keys()}

    def getDexEntry(self):
        if self.pokedex_path is None:
            raise FileNotFoundError("Pokedex file not defined.")
        with open(self.pokedex_path, 'r') as pokedex_json:
            pokedex = json.load(pokedex_json)
            if self.name not in list(pokedex.keys()):
                raise ValueError(
                    f"Pokemon '{self.name}' not found in Pokedex."
                )
            self.__dict__.update(pokedex[self.name])
