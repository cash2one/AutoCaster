from threading import Thread
import Messages
import time
import re
import socket
import requests
import subprocess

ip = "";
port = 8445;


class EventParser(Thread):
    def __init__(self, eventQueue):
        Thread.__init__(self);
        self.eventQueue = eventQueue;

        self.eventPattern = re.compile("^\((\w+)\)(.*)$");
        self.propertySourcePattern = re.compile("(\w+)_(\d+)");
        self.initPattern = re.compile("([^,:]+),([^,:]+),img...__(........),img");
        self.killPattern = re.compile("1,img...__(........),([-\d]+),([-\d]+),img...__(........),([-\d]+),([-\d]+),img...__(........),([-\d]+)(,.*)?$");
        self.killAssistsPattern = re.compile("img...__([A-Fa-f0-9]{8})");

    def run(self):
        print "Generating event";
        self.runFromFile();
        self.runFromGame();

    def runFromGame(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print "Socket creation failed."
            return;

        (gameID, encryptionKey) = self.requestFeaturedGameMode()
        s.bind((ip, port));
        s.listen(2)

        self.startLeague(gameID, encryptionKey)
        (client, address) = s.accept()
        while True:
            line = self.read_line(client)
            print(line)
            match = self.eventPattern.match(line);

    def runFromFile(self):
        f = open('game.txt', 'r');
        for line in f:
            self.processLine(line);

    def processLine(self, line):
        match = self.eventPattern.match(line);

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

                        #self.eventQueue.put(Messages.PropertyChangeMessage(propertyName, propertySource, propertyValue));
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

            victimId = groups[0];
            killerId = groups[3];

            assists = groups[8];
            assistIds = None;

            if (assists):
                assistIds = self.killAssistsPattern.findall(assists);

            return Messages.KillMessage(victimId, killerId, assistIds);

    def read_line(self, s):
        ret = ''

        while True:
            c = s.recv(1)

            if c == '\n' or c == '':
                break
            else:
                ret += c
        return ret

    def requestFeaturedGameMode(self):
        r = requests.get('https://na.api.pvp.net/observer-mode/rest/featured?api_key=3c8bb0c2-ac29-4441-8211-35f44a2cd943');
        # print r.status_code
        if (r.status_code == 200):
            json = r.json()
            gameID = str(json['gameList'][0]['gameId'])
            encryptionKey = json['gameList'][0]['observers']['encryptionKey']
            return (gameID, encryptionKey)
        return False

    def startLeague(self, gameID, encryptionKey):
        cwd = "C:\\Riot Games\\League of Legends\\RADS\\solutions\\lol_game_client_sln\\releases\\0.0.1.111\\deploy\\"
        print cwd
        p = subprocess.Popen([
                cwd + "League of Legends.exe",
                "8394",
                "LoLLauncher.exe",
                "",
                "spectate spectator.na.lol.riotgames.com:80 {} {} NA1".format(encryptionKey, gameID)],
                cwd=cwd)
