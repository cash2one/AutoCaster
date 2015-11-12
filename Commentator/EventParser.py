from threading import Thread;
from EventMessage import EventMessage;
import time;

class EventParser(Thread):
	def __init__(self, eventQueue):
		Thread.__init__(self);
		self.eventQueue = eventQueue;

	def run(self):
		print "Generating event";
		self.eventQueue.put(EventMessage("HP", 0, 100));
