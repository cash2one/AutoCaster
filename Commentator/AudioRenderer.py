from threading import Thread;
import time;

class AudioRenderer(Thread):
	def __init__(self, commentatorQueue, rendererQueue):
		Thread.__init__(self);

		self.commentatorQueue = commentatorQueue;
		self.rendererQueue = rendererQueue;

	def run(self):
		while True:
			event = self.commentatorQueue.get(True);
			print "Audio renderer recieved commentation."
			self.rendererQueue.put(1);
