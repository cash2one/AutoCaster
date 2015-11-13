
class Team(object):
    def __init__(self, id):
        self.id = id;
        self.name = "blue" if (id == 0) else "red";
        self.towersKilled = 0
        self.dragonCount = 0
        self.totalGold = 0
        self.totalKills = 0


    def update(self, propertyChangedEvent):
        if (propertyChangedEvent.propertyName == "DragonBuffs"):
            if (self.dragonCount == propertyChangedEvent.value):
                return False;

            self.dragonCount = propertyChangedEvent.value;
        elif (propertyChangedEvent.propertyName == "TowerKills"):
            if (self.towersKilled == propertyChangedEvent.value):
                return False;

            self.towersKilled = propertyChangedEvent.value;

        return True;