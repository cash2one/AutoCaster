from threading import Thread;
import Messages;
import time;
import re;
import socket;
import requests;
from subprocess import check_call

ip = "192.168.203.180";
port = 8444;


class EventParser(Thread):
<<<<<<< HEAD
        def __init__(self, eventQueue):
                Thread.__init__(self);
                self.eventQueue = eventQueue;

                self.eventPattern = re.compile("^\((\w+)\)(.*)$");
                self.propertySourcePattern = re.compile("(\w+)_(\d+)");
                self.initPattern = re.compile("([^,:]+),([^,:]+),img");

        def run(self):
                print "Generating event";
                try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                except socket.error as err:
                        print "Socket creation failed."
                (gameID, encryptionKey) = self.requestFeaturedGameMode()
                s.bind((ip, port));
                s.listen(2)
                ln=0
                (client, address) = s.accept()
                self.startLeague(gameID, encryptionKey)
                while True:
                        line = self.read_line(client)
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
                                                pass


                
        def read_line(self, s):
                ret = ''

                while True:
                        c = s.recv(1)

                        if c == '\n' or c == '':
                                break
                        else:
                                ret += c
                return ret

        def parseInit(self, rawData):
                groups = self.initPattern.findall(rawData);

                if (groups):
                        summonerNames = [];
                        championNames = [];

                        i = 0;
                        while i < len(groups):
                                summonerName = groups[i][0];
                                championName = groups[i][1];
                                i = i + 1

                                summonerNames.append(summonerName);
                                championNames.append(championName);

                        return Messages.InitMessage(summonerNames, championNames);

        def requestFeaturedGameMode(self):
                r = requests.get('https://na.api.pvp.net/observer-mode/rest/featured?api_key=3c8bb0c2-ac29-4441-8211-35f44a2cd943');
                if (r.status_code == 200):
                    json = r.json()
                    gameID = json['gameList'][0]['gameId']
                    encryptionKey = json['gameList'][0]['observers']['encryptionKey']
                    return (gameID, encryptionKey)
        def startLeague(self, gameID, encryptionKey):
                check_call([
                    r"C:\Riot Games\League of Legends\RADS\solutions\lol_game_client_sln\releases\0.0.1.110\deploy\League of Legends.exe",
                    "8394",
                    "LoLLauncher.exe",
                    "",
                    "spectate spectator.na.lol.riotgames.com:80" + gameID +" "+encryptionKey + " NA1"])
=======
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
>>>>>>> dee105aca3747f92bba7813c561390f915e7a2b3
