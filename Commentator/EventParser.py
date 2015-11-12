from threading import Thread;
import Messages;
import time;
import re;

class EventParser(Thread):
        def __init__(self, eventQueue):
                Thread.__init__(self);
                self.eventQueue = eventQueue;

        def run(self):
                print "Generating event";
                count = 0
                f = open('game.txt', 'r');
                for line in f:
                        if (re.match(".*[^A-z]+Kills_[0-9],[0-9]+", line)):
                                print line
                                count += 1
                print count
                self.eventQueue.put(Messages.PropertyChangeMessage("HP", 0, 100));
