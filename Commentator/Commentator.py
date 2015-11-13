from threading import Thread
import Messages
import Game
from CommentaryType import CommentaryType
import json
import time
from Actor import Actor
import random

class Commentator(Thread):
	def __init__(self, eventQueue, commentatorQueue):
		Thread.__init__(self);

		self.eventQueue = eventQueue;
		self.commentatorQueue = commentatorQueue;

		self.commentators = []
		self.commentators.append(Actor("Rivington the 4th", "Brian", 0))
		self.commentators.append(Actor("Salli", "Salli", 1))

		riv_bot = self.commentators[0]
		salli_bot = self.commentators[1]

		self.reset();

		with open("Config.json") as configFile:
			config = json.load(configFile)
	
		self.numberTh = ["first", "second", "third", "forth", "fifth", "sixth", "seventh", "eigth", "ninth", "tenth", "eleventh" ];

	def reset(self):
		self.lastMessageTime = 0;

		self.gameProperties = ["GameTime"];
		self.game = Game.Game();

		self.teamProperties = ["DragonBuffs", "TowerKills", "TeamGoldTotal", "TeamGoldCurrent"];
		self.teams = [];

		for i in range(2):
			self.teams.append(Game.Team(i));

		self.playerProperties = ["Kills", "KillCount", "Health", "Level", "GoldTotal", "GoldCurrent"];
		self.players = [];

		for i in range(10):
			self.players.append(Game.Player(i));

	def introduceActors(self, initEvent):
		messageArgs = {}
		messageArgs["joiner"] = False;

		for i in range(len(self.commentators)):
			bot = self.commentators[i];
			messageArgs["bot"] = bot
			self.processMessage(bot, CommentaryType.Introduction, messageArgs);
			messageArgs["joiner"] = True;

		bot = self.commentators[0]
		messageArgs["bot"] = bot
		messageArgs["players"] = self.players;
		messageArgs["joiner"] = False;
		self.processMessage(bot, CommentaryType.GameSummary, messageArgs)

	def run(self):
		print "Commentator started";

		while True:
			event = self.eventQueue.get(True);

			messageType = None;
			messageArgs = {}

			bot = self.commentators[random.randint(0,1)]

			if (isinstance(event, Messages.InitMessage)):
				self.reset();

				for i in range(10):
					player = self.players[i];
					player.name = event.summonerNames[i];
					player.champion = event.championNames[i];
					player.dataId = event.dataIds[i];

					#print "Champion " + player.champion + ": " + player.dataId;

				self.introduceActors(event);
			elif (isinstance(event, Messages.PropertyChangeMessage)):
				if (event.propertyName in self.gameProperties):
					if (self.game.update(event)):
						if (event.propertyName == "GameTime"):
							if (self.lastMessageTime > 0) and (self.game.time > self.lastMessageTime):
								messageType = CommentaryType.GameState;
								messageArgs["teams"] = self.teams;
								messageArgs["players"] = self.players;

				if (event.propertyName in self.playerProperties):
					player = self.players[event.sourceId];

					if (player.update(event)):
						if (event.propertyName == "GoldTotal"):
							teamGoldTotal = 0

							for i in range(4):
								teamGoldTotal = teamGoldTotal + self.players[i].goldTotal;

							self.eventQueue.put(Messages.PropertyChangeMessage("TeamGoldTotal", 0 if event.sourceId < 5 else 1, teamGoldTotal))
						elif (event.propertyName == "GoldCurrent"):
							teamGoldCurrent = 0

							for i in range(4):
								teamGoldCurrent = teamGoldCurrent + self.players[i].goldCurrent;

							self.eventQueue.put(Messages.PropertyChangeMessage("TeamGoldCurrent", 0 if event.sourceId < 5 else 1, teamGoldCurrent))
						elif (event.propertyName == "Level"):
							messageType = CommentaryType.LevelUp;
							messageArgs["player"] = player;
							messageArgs["playerTeam"] = self.teams[0] if player.id < 5 else self.teams[1];
							messageArgs["enemyTeam"] = self.teams[1] if player.id < 5 else self.teams[0];
							pass
				elif (event.propertyName in self.teamProperties):
					team = self.teams[event.sourceId];

					if (team.update(event)):
						if (event.propertyName == "DragonBuffs"):
							messageType = CommentaryType.DragonKill;
						elif (event.propertyName == "TowerKills"):
							messageType = CommentaryType.BuildingKill;

						if (messageType):
							messageArgs["team"] = team;
							messageArgs["enemyTeam"] = self.teams[0] if team.id == 1 else self.teams[1]
							messageArgs["nth"] = self.numberTh[event.value - 1]
			elif (isinstance(event, Messages.KillMessage)):
				killer = self.findPlayerByDataId(event.killerId);
				victim = self.findPlayerByDataId(event.victimId);

				assists = []

				if event.assistIds:
					for assistId in event.assistIds:
						assist = self.findPlayerByDataId(assistId);

						if assist:
							assists.append(assist.champion);

				if killer and victim:
					messageType = CommentaryType.ChampionKill;
					messageArgs = {}
					messageArgs["killer"] = killer;
					messageArgs["killerTeam"] = self.teams[0] if killer.id < 5 else self.teams[1];
					messageArgs["victim"] = victim;
					messageArgs["victimTeam"] = self.teams[0] if victim.id < 5 else self.teams[1];

			if (messageType):
				self.processMessage(bot, messageType, messageArgs)

	def findPlayerByDataId(self, dataId):
		for player in self.players:
			if (player.dataId == dataId):
				return player;

	def processMessage(self, actor, messageType, messageArgs, rate="medium", volume=0.8, pitch=1.0):
		message = actor.generateMessage(messageType, messageArgs, rate, volume, pitch);

		if (message):
			self.commentatorQueue.put(message)
			self.lastMessageTime = self.game.time;

