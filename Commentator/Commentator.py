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

			if (isinstance(event, Messages.PropertyChangeMessage)):
				if (event.propertyName in self.playerProperties):
					player = self.players[event.sourceId];

					self.players[event.sourceId].update(event);

					message = "Player {p} has scored a kill.".format(p = event.sourceId);

					self.processEvent(Messages.CommentaryMessage(message));

	def processEvent(self, event):
		self.commentatorQueue.put(event);
		pass