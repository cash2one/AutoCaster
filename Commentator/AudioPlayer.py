from threading import Thread
import time
import pyglet

class AudioPlayer(Thread):
    def __init__(self, rendererQueue):
        Thread.__init__(self)
        self.rendererQueue = rendererQueue

    def run(self):
        while True:
            event = self.rendererQueue.get(True)
            audio_file = event["audio_file"]

            # print "Audio player an audio file ({}) to play from source {}.".format(audio_file, event["source"])

            media = pyglet.media.load(audio_file)
            media.play()
