
class Player(object):
    def __init__(self, id):
        self.id = id;
        self.dataId = 0;
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
        self.killCount = 0
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

    def update(self, propertyChangedEvent):
        if (propertyChangedEvent.propertyName == "Kills"):
            self.kills = propertyChangedEvent.value;
        elif (propertyChangedEvent.propertyName == "KillCount"):
            self.killCount = propertyChangedEvent.value;
        elif (propertyChangedEvent.propertyName == "Heatlh"):
            self.health = propertyChangedEvent.value;
        elif (propertyChangedEvent.propertyName == "Level"):
            self.level = propertyChangedEvent.value;