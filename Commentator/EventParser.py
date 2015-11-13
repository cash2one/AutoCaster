from threading import Thread;
import Messages;
import time;
import re;

class EventParser(Thread):
	def __init__(self, eventQueue):
		Thread.__init__(self);
		self.eventQueue = eventQueue;

		self.eventPattern = re.compile("^\((\w+)\)(.*)$");
		self.propertySourcePattern = re.compile("(\w+)_(\d+)");
		self.initPattern = re.compile("([^,:]+),([^,:]+),img...__(........),img");
		self.killPattern = re.compile("1,img...__(........),([-\d]+),([-\d]+),img...__(........),([-\d]+),([-\d]+),img...__(........),([-\d]+)(?:,img...__(........))*")

#1,img://__09f5e000,1,0,img://__09ce8400,0,6,img://__09a67900,-1,img://__09d4af00,img://__09e53f00
	def run(self):
		print "Generating event";

		f = open('game.txt', 'r');
		ln = 0
		for line in f:
			match = self.eventPattern.match(line);

			ln = ln + 1
			if (match):
				groups = match.groups();

				if (groups):
					eventSource = groups[0];
					data = groups[1];

					if (eventSource == "Update"):
						propertyAndValues = data.split(",");

						i = 0;
						while i < len(propertyAndValues):
							propertyName = propertyAndValues[i];
							propertyValue = propertyAndValues[i + 1];
							propertySource = -1;
							i = i + 2

							propertyMatch = self.propertySourcePattern.match(propertyName);

							if (propertyMatch):
								propertyGroups = propertyMatch.groups();
								propertyName = propertyGroups[0];
								propertySource = int(propertyGroups[1]);

							self.eventQueue.put(Messages.PropertyChangeMessage(propertyName, propertySource, propertyValue));
					elif (eventSource == "Init"):
						self.eventQueue.put(self.parseInit(data));
					elif (eventSource == "AddMessage"):
						self.eventQueue.put(self.parseKillMessage(data));

	def parseInit(self, rawData):
		groups = self.initPattern.findall(rawData);

		if (groups):
			summonerNames = [];
			championNames = [];
			dataIds = [];

			i = 0;
			while i < len(groups):
				summonerName = groups[i][0];
				championName = groups[i][1];
				dataId = groups[i][2];
				i = i + 1

				summonerNames.append(summonerName);
				championNames.append(championName);
				dataIds.append(dataId);

			return Messages.InitMessage(summonerNames, championNames, dataIds);

	def parseKillMessage(self, rawData):
		match = self.killPattern.match(rawData);

		if (match):
			groups = match.groups();
			print groups;

		victimId = 0;
		killerId = 0;
		assistIds = 0;

		return Messages.KillMessage(victimId, killerId, assistIds);