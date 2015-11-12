
class Player(object):
    def __init__(self):
        self.name = ""
        self.champion = ""
        self.isAlive = False
        self.team = 100
        self.participantId = 0
        self.health = 0
        self.mana = 0
        self.armor = 0
        self.mr = 0
        self.ad = 0
        self.ap = 0
        self.items = []
        self.spells = []
        self.spellLevels = []
        self.spellCDs = []
        self.kills = 0
        self.deaths = 0
        self.assists = 0
        self.attackSpeed = 0
        self.respawnTimer = 0
        self.attackSpeed = 0
        self.movementSpeed = 0
        self.cs = 0
        self.level = 1
        self.exp = 0
        self.gold = 0


class Teams(object):
    def __init__(self):
        self.towersKilled = 0
        self.dragonCount = 0
        self.totalGold = 0
        self.totalKills = 0


class Teams(object):
    def __init__(self):
        self.time = 0 # seconds since game start
