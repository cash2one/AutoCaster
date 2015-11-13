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

            #if self.player.playing:
                #print "sound currently playing"
                # return

            media = pyglet.media.load(audio_file)
            self.player.volume = volume

            # this isn't well tested
            self.player.next()

            self.player.queue(media)
            self.player.play()

            # maybe this should be 'next'
            self.player.eos_action = 'stop'

            # print "{} {} {}".format(self.player.pitch, self.player.playing, self.player.volume)
