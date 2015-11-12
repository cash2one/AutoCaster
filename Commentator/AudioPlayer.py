from threading import Thread;
import time;

class AudioPlayer(Thread):
	def __init__(self, rendererQueue):
		Thread.__init__(self);
		self.rendererQueue = rendererQueue;

	def run(self):
		while True:
			event = self.rendererQueue.get(True);
			#print "Audio player an audio to play. " + str(event);
