from threading import Thread
from datetime import datetime
import time
import pyglet
from mutagen.mp3 import MP3

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
            pitch = event["pitch"]
            message_timestamp = event["timestamp"]
            now_timestamp = datetime.now()
            diff = now_timestamp - message_timestamp

            if diff.total_seconds() > 5:
                continue

            mp3 = MP3(audio_file)
            media = pyglet.media.load(audio_file)

            self.player.volume = volume
            self.player.pitch = pitch

            self.player.next()

            self.player.queue(media)
            self.player.play()
            time.sleep(mp3.info.length)
