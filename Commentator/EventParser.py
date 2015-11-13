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

	def run(self):
		print "Generating event";

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
								propertySource = propertyGroups[1];

							self.eventQueue.put(Messages.PropertyChangeMessage(eventSource, propertyName, propertySource, propertyValue));
					else:
						pass

		
def read_line(s):
	ret = ''

	while True:
		c = s.recv(1)

		if c == '\n' or c == '':
		    break
		else:
		    ret += c
	return ret