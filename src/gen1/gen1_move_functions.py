"""
A set of functions to handle move effects that are more complicated.
"""

def handle_charge(attacker, log=False):
    """
    Handles first-turn charge effect of certain moves.
    This effect applies to:
    - Solar Beam
    - Sky Attack
    - Skull Bash
    - Razor Wind
    """
    attacker.charging = not attacker.charging
    if log and attacker.charging:
        print(f"{attacker.name} is building up energy!")

def handle_recharge(attacker):
    """
    Handles recharge effect of certain moves.
    In this game, only Hyper Beam has this effect.
    """
    attacker.recharging = not attacker.recharging

def handle_confusion(attacker):
    """
    Handles confusion counter and self-damage chance.
    Caused by:
    - Confuse Ray
    - Supersonic
    - Confusion
    - Psybeam
    - Thrash
    - Petal Dance
    """
    if not attacker.vol_status['confusion']:
        pass

    if attacker.vol_status.confusion.counter == 0:
        del attacker.vol_status['confusion']
        if log:
            print(f"{attacker.name} is confused no longer!")


def is_confused(self):
    """
    Checks if a Pokemon is confused.
    """
    if self.vol_status['confusion']:
        if self.log:
            print(f"{self.name} is confused!")

        if np.random.choice([0,1], 1):
            self.hurt_itself_in_confusion()
            return True

    return False

def hurt_itself_in_confusion(self):
    """
    Handles self-damage if Pokemon hurts itself in confusion.
    """
    L = self.level
    AS = self.stats.attack
    P = 40
    DS = self.stats.defense
    STAB = 1
    TB = 1

    base_dmg = min(((((2*L/5)+2)*(AS/DS)*P)/50),997)+2
    mod_dmg = math.floor(math.floor(base_dmg*STAB)*(TB*10/10))
    if mod_dmg > 1:
        if expected:
            mod_dmg = math.floor(mod_dmg*(236/255))
        else:
            R = 217 + np.random.choice(range(39),size=1,replace=False)[0]
            mod_dmg = math.floor(mod_dmg*(R/255))

    return mod_dmg

            mon.stats['hp'] -= confuse_dmg
            if log:
                print("%s took %s damage in its confusion!" % (mon.trueName, confuse_dmg))
