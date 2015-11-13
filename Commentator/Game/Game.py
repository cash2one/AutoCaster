
class Game(object):
    def __init__(self):
        self.time = 0;

    def update(self, propertyChangedEvent):
        if (propertyChangedEvent.propertyName == "GameTime"):
            if (self.time == propertyChangedEvent.value):
                return False;

            self.time = propertyChangedEvent.value;

        return True;
