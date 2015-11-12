from threading import Thread;
import json;
import time;

class Commentator(Thread):
	def __init__(self, eventQueue, commentatorQueue):
		Thread.__init__(self);

		self.eventQueue = eventQueue;
		self.commentatorQueue = commentatorQueue;

		with open("Config.json") as configFile:
			config = json.load(configFile)
	
		pass;

	def run(self):
		print "Commentator started";
		while True:
			event = self.eventQueue.get(True);
			print "Commentator recieved event."
			self.commentatorQueue.put(1);
