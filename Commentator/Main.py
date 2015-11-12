from EventParser import EventParser;
from Commentator import Commentator;
from AudioRenderer import AudioRenderer;
from AudioPlayer import AudioPlayer;
from threading import Thread;
from Queue import Queue;
import time;

eventQueue = Queue();
commentatorQueue = Queue();
rendererQueue = Queue();

eventParser = EventParser(eventQueue);
commentator = Commentator(eventQueue, commentatorQueue)
audioRenderer = AudioRenderer(commentatorQueue, rendererQueue);
audioPlayer = AudioPlayer(rendererQueue);

eventParser.daemon = True;
eventParser.start();

commentator.daemon = True;
commentator.start();

audioRenderer.daemon = True;
audioRenderer.start();

audioPlayer.daemon = True;
audioPlayer.start();

while True:
	time.sleep(100);

print "Finished"