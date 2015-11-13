from threading import Thread;
import Messages;
import Game;
import json;
import time;

class Commentator(Thread):
	def __init__(self, eventQueue, commentatorQueue):
		Thread.__init__(self);

		self.eventQueue = eventQueue;
		self.commentatorQueue = commentatorQueue;

		self.teams = [];

		for i in range(2):
			self.teams.append(Game.Team(i));

		self.playerProperties = ["Kills", "KillCount"];
		self.players = [];

		for i in range(10):
			self.players.append(Game.Player(i));

		with open("Config.json") as configFile:
			config = json.load(configFile)
	
		pass;

	def run(self):
		print "Commentator started";

		while True:
			event = self.eventQueue.get(True);

			if (isinstance(event, Messages.InitMessage)):
				for i in range(10):
					player = self.players[i];
					player.name = event.summonerNames[i];
					player.champion = event.championNames[i];
					player.dataId = event.dataIds[i];

					print "Champion " + player.champion + ": " + player.dataId;
			elif (isinstance(event, Messages.PropertyChangeMessage)):
				if (event.propertyName in self.playerProperties):
					player = self.players[event.sourceId];

					self.players[event.sourceId].update(event);

					message = "{c} has scored a kill.".format(c = player.champion);

					#self.processEvent(Messages.CommentaryMessage(message));
			elif (isinstance(event, Messages.KillMessage)):
				killer = self.findPlayerByDataId(event.killerId);
				victim = self.findPlayerByDataId(event.victimId);

				if killer and victim:
					message = "{k} has killed {v}".format(k = killer.champion, v = victim.champion);

					self.processEvent(Messages.CommentaryMessage(message));

			elif (isinstance(event, Messages.BuildingKillMessage)):
				killer = self.findPlayerByDataId(event.killerId);
				building = "";

				if killer and building:
					message = "{k} has destroyed {v}".format(k = killer.champion, v = building);

					self.processEvent(Messages.CommentaryMessage(message));

			elif (isinstance(event, Messages.MonsterKillMessage)):
				killer = self.findPlayerByDataId(event.killerId);
				monster = "";

				if killer and monster:
					message = "{k} has slain {v}".format(k = killer.champion, v = monster);

					self.processEvent(Messages.CommentaryMessage(message));

	def findPlayerByDataId(self, dataId):
		for player in self.players:
			if (player.dataId == dataId):
				return player;

	def processEvent(self, event):
		self.commentatorQueue.put(event);
