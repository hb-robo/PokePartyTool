"""
Classes to represent Pokemon from Generation 1 games.
Contains physical attributes, default stats, type data, and movepool,
as well as "live" HP, stats, status, etc.
"""
import json
import src.gen1.gen1_constants as constants
from src.parent_classes import Pokemon

class Gen1HandheldBattle(Battle):
    """
    Class to represent a battle between two teams of Gen1 Pokemon.
    """
    def __init__(self, team1, team2):
        assert len(team1) < 6 and len(team2) < 6, "Teams must have at most 6 Pokemon."
        assert len(team1) > 0 and len(team2) > 0, "Teams must have at least 1 Pokemon."


        self.team1 = team1
        self.team2 = team2
        self.turn = 0

    # NOTE: The following methods are AI-generated for general direction.
    # They will be implemented later, but for now, they are placeholders.
    def switch_pokemon(self, team, new_pokemon):
        """
        Switches out the active Pokemon for a new one.
        """
        if team == 1:
            self.team1.active = new_pokemon
        elif team == 2:
            self.team2.active = new_pokemon
        else:
            raise ValueError("Invalid team number.")

    def run_turn(self):
        """
        Runs a turn in the battle.
        """
        self.turn += 1
        if self.team1.active.stats.speed > self.team2.active.stats.speed:
            self.run_move(self.team1.active, self.team2.active)
            self.run_move(self.team2.active, self.team1.active)
        else:
            self.run_move(self.team2.active, self.team1.active)
            self.run_move(self.team1.active, self.team2.active)

    def run_move(self, attacker, defender):
        """
        Runs a move from the attacker on the defender.
        """
        move = attacker.choose_move()
        move.use(attacker, defender)

    def run_battle(self):
        """
        Runs the battle until one team is defeated.
        """
        while not self.team1.is_defeated() and not self.team2.is_defeated():
            self.run_turn()

        if self.team1.is_defeated():
            print("Team 2 wins!")
        else:
            print("Team 1 wins!")

    def run_battle_with_log(self):
        """
        Runs the battle with log until one team is defeated.
        """
        while not self.team1.is_defeated() and not self.team2.is_defeated():
            print(f"Turn {self.turn}")
            self.run_turn()
            print("")

        if self.team1.is_defeated():
            print("Team 2 wins!")
        else:
            print("Team 1 wins!")


class Gen1Pokemon(Pokemon):
    """
    Superclass for all Generation 1 Pokemon classes.
    """
    POKEDEX_PATH = None
    GEN1_MON_CONSTANTS = None

    def __init__(self, name, level=50):
        super().__init__(self, name, level)


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

