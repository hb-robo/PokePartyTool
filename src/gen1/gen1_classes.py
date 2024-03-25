"""
Classes to represent Pokemon from Generation 1 games.
Contains physical attributes, default stats, type data, and movepool,
as well as "live" HP, stats, status, etc.
"""
import json
import src.gen1.gen1_constants as constants
from src.parent_classes import Pokemon


class Gen1Pokemon(Pokemon):
    POKEDEX_PATH = '../../data/json/gen1/pm_red_green_pokedex.json'
    GEN1_MON_CONSTANTS = constants.PM_RG_CONSTANTS

    def __init__(self, name, level=50):
        super().__init__(
            self.name,
            self.level,
            pokedex_path=self.POKEDEX_PATH,
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


class PMHandheldPokemon(Gen1Pokemon):
    """
    Class to represent Pokemon from Pocket Monsters Red/Green/Blue/Pikachu.
    """
    POKEDEX_PATH = '../../data/json/gen1/pm_rgbp_pokedex.json'
    GEN1_MON_CONSTANTS = constants.PM_RGBP_CONSTANTS


class PMStadiumPokemon(Gen1Pokemon):
    """
    Class to represent Pokemon from Pocket Monsters Stadium.
    """
    POKEDEX_PATH = '../../data/json/gen1/pm_stadium_pokedex.json'
    GEN1_MON_CONSTANTS = constants.PM_S_CONSTANTS


class PMStadium2Pokemon(Gen1Pokemon):
    """
    Class to represent Pokemon from Pocket Monsters Stadium 2.
    """
    POKEDEX_PATH = '../../data/json/gen1/pm_stadium2_pokedex.json'
    GEN1_MON_CONSTANTS = constants.PM_S2_CONSTANTS


class PkmnHandheldPokemon(Gen1Pokemon):
    """
    Class to represent Pokemon from Pokemon Red/Blue/Yellow.
    """
    POKEDEX_PATH = '../../data/json/gen1/pm_rgbp_pokedex.json'
    GEN1_MON_CONSTANTS = constants.PKMN_RBY_CONSTANTS


class PkmnStadiumPokemon(Gen1Pokemon):
    """
    Class to represent Pokemon from Pokemon Stadium.
    """
    POKEDEX_PATH = '../../data/json/gen1/pkmn_stadium_pokedex.json'
    GEN1_MON_CONSTANTS = constants.PKMN_S_CONSTANTS

