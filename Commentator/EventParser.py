from threading import Thread;
import Messages;
import time;
import re;
import socket;

ip = "192.168.203.180";
port = 8444;


class EventParser(Thread):
	def __init__(self, eventQueue):
		Thread.__init__(self);
		self.eventQueue = eventQueue;

		self.eventPattern = re.compile("^\((\w+)\)(.*)$");
		self.propertySourcePattern = re.compile("(\w+)_(\d+)");
		self.initPattern = re.compile("([^,:]+),([^,:]+),img...__(........),img");
		self.killPattern = re.compile("1,img...__(........),([-\d]+),([-\d]+),img...__(........),([-\d]+),([-\d]+),img...__(........),([-\d]+)(?:,img...__(........))*")

	def run(self):
		print "Generating event";

		#f = open('game.txt', 'r');
		#ln = 0
		#for line in f:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as err:
			print "Socket creation failed."

		s.bind((ip, port));
		s.listen(2)
		ln=0
		(client, address) = s.accept()
		while True:
			line = read_line(client)
			print(line)
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

def read_line(s):
	ret = ''

	while True:
		c = s.recv(1)

		if c == '\n' or c == '':
		    break
		else:
		    ret += c
	return ret