class Mon:
    def __init__(self, name, dex):
        self.name = name
        self.hp = dex.at[name,'hp']
        self.attack = dex.at[name,'attack']
        self.defense = dex.at[name,'defense']
        self.special = dex.at[name,'special']
        self.speed = dex.at[name,'speed']

        self.lastUsedMove = ""

        # stat buffs and nerfs
        self.attackMod = 0
        self.defenseMod = 0
        self.specialMod = 0
        self.specialAttMod = 0
        self.specialDefMod = 0
        self.speedMod = 0
        self.accuracyMod = 0
        self.evasionMod = 0

        # status conditions
        self.status = False
        self.statusCounter = 0
        self.isConfused = False
        self.isPoisoned = False
        self.isToxic = False
        self.isAsleep = False
        self.isBurned = False
        self.isParalyzed = False
        self.isFrozen = False

        # miscellaneous conditions
        self.rageCounter = 0
        self.rampageCounter = 0
        self.physProtection = 0.0
        self.specProtection = 0.0
        self.hasSubstitute = False
        self.isSeeded = False
        self.isTrapped = False
        self.isAirborne = False
        self.isUnderground = False


class Battle:
    def __init__(self, mon1, mon2):
        self.pokemon = mon1
        self.opponent = mon2

        # various battle conditions
        self.weather = None
        self.firstMover = None

