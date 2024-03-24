"""
Classes to represent Pokemon from Generation 1 games.
Contains physical attributes, default stats, type data, and movepool,
as well as "live" HP, stats, status, etc.
"""
import json
from src.gen1.gen1_constants import PM_RG_CONSTANTS
from src.parent_classes import Pokemon

class PMRG_Pokemon(Pokemon):
    POKEDEX_PATH = '../../data/json/gen1/pm_red_green_pokedex.json'
    GEN1_MON_CONSTANTS = PM_RG_CONSTANTS

    def __init__(self, name, level=50):
        super().__init__(
            self.name,
            self.level,
            dex=self.POKEDEX_PATH,
            constants=self.GEN1_MON_CONSTANTS
        )

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

