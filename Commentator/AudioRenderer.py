from threading import Thread
import Messages
import time
import pyvona
import hashlib
import os.path

AUDIO_DIRECTORY = "./audio/"

class AudioRenderer(Thread):
    def __init__(self, commentatorQueue, rendererQueue):
        Thread.__init__(self)

        self.v = pyvona.create_voice(
                "GDNAJCIHKDP2YAKG664A",
                "8yaFb9+jGeuI8DDrYKdK+9jUVNAqqYRuxyG254la"
            )
        self.v.codec = "mp3"
        self.v.region = "us-west"
        self.commentatorQueue = commentatorQueue
        self.rendererQueue = rendererQueue

    def run(self):
        while True:
            event = self.commentatorQueue.get(True)
            #print "Audio renderer recieved commentation."
            '''
                replace speech and rate with event.speech and event.rate
            '''
            speech = event.text
            print speech;

            rate = "medium"
            sha256 = hashlib.sha256(speech + rate)
            hash_string = sha256.hexdigest()

            output_file = AUDIO_DIRECTORY + hash_string + ".mp3"
            if not os.path.isfile(output_file):
                self.v.speech_rate = rate
                self.v.voice_name = "Salli"
                self.v.fetch_voice(speech, output_file)
            #else:
                #print "already exists"

            '''
                put this into next queue
            '''

            #print output_file
            self.rendererQueue.put(event)
