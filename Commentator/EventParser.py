from threading import Thread;
import Messages;
import time;

class EventParser(Thread):
	def __init__(self, eventQueue):
		Thread.__init__(self);
		self.eventQueue = eventQueue;

	def run(self):
		print "Generating event";
		self.eventQueue.put(Messages.PropertyChangeMessage("HP", 0, 100));
