import json
from Messages import CommentaryMessage

PRONUNCIATION_DIR = "./pronounce/"

class Actor(object):
    def __init__(self, name, voice, sourceId, pronounce_file="default.json"):
        self.name = name
        self.voice = voice
        with open(PRONUNCIATION_DIR + pronounce_file, 'rb') as fp:
            self.pronounce = json.load(fp)
        self.sourceId = sourceId

    def generateMessage(self, message, rate, volume, pitch):
        result = ""
        for i in message.split(" "):
            lookup = i.lower().replace('.', '')
            if lookup in self.pronounce:
                result += self.pronounce[lookup]
            else:
                result += lookup
            result += " "
        return CommentaryMessage(self.voice, result, self.sourceId, rate, volume, pitch)