from threading import Thread
import Messages
import Game
import json
import time
from Actor import Actor
import random

class Commentator(Thread):
    def __init__(self, eventQueue, commentatorQueue):
        Thread.__init__(self)

        self.eventQueue = eventQueue
        self.commentatorQueue = commentatorQueue

        self.commentators = []
        self.commentators.append(Actor("Rivington the 4th", "Brian", 0))
        self.commentators.append(Actor("Salli", "Salli", 1))

        riv_bot = self.commentators[0]
        salli_bot = self.commentators[1]

        self.teamProperties = ["DragonBuffs", "TowerKills"]
        self.teams = []

        for i in range(2):
            self.teams.append(Game.Team(i))

        self.playerProperties = ["Kills", "KillCount", "Heath", "Level"]
        self.players = []

        for i in range(10):
            self.players.append(Game.Player(i))

        with open("Config.json") as configFile:
            config = json.load(configFile)

        self.numberTh = ["first", "second", "third", "forth", "fifth", "sixth", "seventh", "eigth", "ninth", "tenth", "eleventh" ];

        pass


    def run(self):
        print "Commentator started"

        while True:
            event = self.eventQueue.get(True)

            bot = self.commentators[random.randint(0,1)]

            if (isinstance(event, Messages.InitMessage)):
                for i in range(10):
                    player = self.players[i]
                    player.name = event.summonerNames[i]
                    player.champion = event.championNames[i]
                    player.dataId = event.dataIds[i]

                    # print "Champion " + player.champion + ": " + player.dataId

            elif (isinstance(event, Messages.PropertyChangeMessage)):
                if (event.propertyName in self.playerProperties):
                    player = self.players[event.sourceId]

                    self.players[event.sourceId].update(event)

                    if (player.update(event)):
                        message = None

                        if (message):
                            self.processMessage(bot, message)
                elif (event.propertyName in self.teamProperties):
                    team = self.teams[event.sourceId]

                    if (team.update(event)):
                        message = None

                        if (event.propertyName == "DragonBuffs"):
                            if (event.value == 1):
                                message = "{t} team has just slain their first dragon of the game.".format(t = team.name)
                            else:
                                message = "The {t} team has slain their {n} dragon.".format(t = team.name, n = self.numberTh[event.value - 1])
                        elif (event.propertyName == "TowerKills"):
                            print ">>> " + str(event.value)
                            if (event.value == 1):
                                message = "{t} team has just taken their first tower.".format(t = team.name)
                            elif (event.value == 11):
                                message = "{t} team has just the last tower of the game and only the nexus remains.".format(t = team.name)
                            else:
                                message = "{t} team has taken their {n} tower of the game.".format(t = team.name, n = self.numberTh[event.value - 1])

                        if (message):
                            self.processMessage(bot, message)

                    message = "{c} has scored a kill.".format(c = player.champion)

                    self.processMessage(bot, message)

            elif (isinstance(event, Messages.KillMessage)):
                killer = self.findPlayerByDataId(event.killerId)
                victim = self.findPlayerByDataId(event.victimId)

                assists = []

                if event.assistIds:
                    for assistId in event.assistIds:
                        assist = self.findPlayerByDataId(assistId);

                        if assist:
                            assists.append(assist.champion);

                if killer and victim:
                    message = "{k} has killed {v}".format(k = killer.champion, v = victim.champion)
                    self.processMessage(bot, message)


            elif (isinstance(event, Messages.BuildingKillMessage)):
                killer = self.findPlayerByDataId(event.killerId)
                building = ""

                if killer and building:
                    message = "{k} has destroyed {v}".format(k = killer.champion, v = building)

                    self.processMessage(bot, message)

            elif (isinstance(event, Messages.MonsterKillMessage)):
                killer = self.findPlayerByDataId(event.killerId)
                monster = ""

                if killer and monster:
                    message = "{k} has slain {v}".format(k = killer.champion, v = monster)

                    self.processMessage(bot, message)

    def findPlayerByDataId(self, dataId):
        for player in self.players:
            if (player.dataId == dataId):
                return player

    def processMessage(self, actor, message, rate="medium", volume=0.8, pitch=1.0):
        if random.randint(0, 10) < 3:
            self.commentatorQueue.put(actor.generateMessage(message, rate, volume, pitch))
