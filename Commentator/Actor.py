import json
from CommentaryType import CommentaryType
from Messages import CommentaryMessage

PRONUNCIATION_DIR = "./pronounce/"

class Actor(object):
    def __init__(self, name, voice, sourceId, pronounce_file="default_pronounce.json"):
        self.name = name;
        self.voice = voice;

        with open(PRONUNCIATION_DIR + pronounce_file, 'rb') as fp:
            self.pronounce = json.load(fp);

        self.sourceId = sourceId;
        self.lastTalkTime = 0;
        self.excitement = 0;

        # 0 = nuetral, -1 = blue, 1 = red.
        self.teamFavor = 0;

    def generateMessage(self, messageType, messageArgs, rate, volume, pitch):
        message = self.selectMessageTemplate(messageType, messageArgs).format(**messageArgs);
        result = ""

        for i in message.split(" "):
            lookup = i.lower().replace('.', '').replace(',', '')
            if lookup in self.pronounce:
                new_text = i.replace(lookup, self.pronounce[lookup])
                result += new_text
            else:
                result += i
            result += " "

        return CommentaryMessage(self.voice, result, self.sourceId, rate, volume, pitch)

    def selectMessageTemplate(self, messageType, messageArgs):
        if (messageType == CommentaryType.Introduction):
            if (messageArgs["joiner"]):
                return "and I'm {bot.name}";

            return "Hi, I'm {bot.name}";
        elif (messageType == CommentaryType.GameSummary):
            return "Today we'll see the blue team's {players[0].champion}, {players[1].champion}, {players[2].champion}, {players[3].champion} and {players[4].champion} facing off against the red team's {players[5].champion}, {players[6].champion}, {players[7].champion}, {players[8].champion} and {players[9].champion}";
        elif (messageType == CommentaryType.ChampionKill):
            return "{killer.champion} has just killed {victim.champion}";
        elif (messageType == CommentaryType.BuildingKill):
            if (messageArgs["team"].towersKilled == 1):
                return "{team.name} team has just taken their first tower.";
            elif (messageArgs["team"].towersKilled == 11):
                return "{team.name} team has just the last tower of the game and only the nexus remains.";
            else:
               return "{team.name} team has taken their {nth} tower of the game.";
        elif (messageType == CommentaryType.DragonKill):
            if (messageArgs["team"].dragonCount == 1):
                return "{team.name} team has just slain their {nth} dragon of the game.";
            else:
                return "The {team.name} team has slain their {nth} dragon.";



