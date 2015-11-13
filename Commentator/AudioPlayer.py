from threading import Thread
import time
import pyglet

class AudioPlayer(Thread):
    def __init__(self, rendererQueue):
        Thread.__init__(self)
        self.rendererQueue = rendererQueue
        self.player = pyglet.media.Player()

    def run(self):
        while True:
            event = self.rendererQueue.get(True)
            audio_file = event["audio_file"]
            volume = event["volume"]
            message_timestamp = event["timestamp"]
            now_timestamp = time.time()

            # print "Audio player an audio file ({}) to play from source {}.".format(audio_file, event["source"])

            time.sleep(5)
            media = pyglet.media.load(audio_file)
            self.player.volume = volume
            self.player.queue(media)
            self.player.play()
