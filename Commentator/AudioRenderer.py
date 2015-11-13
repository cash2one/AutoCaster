from threading import Thread
import Messages
import time
import pyvona
import os.path


AUDIO_DIRECTORY = "./audio/"

class AudioRenderer(Thread):
    def __init__(self, commentatorQueue, rendererQueue):
        Thread.__init__(self)
        self.commentatorQueue = commentatorQueue
        self.rendererQueue = rendererQueue
        self.v = pyvona.create_voice(
                "GDNAJCIHKDP2YAKG664A",
                "8yaFb9+jGeuI8DDrYKdK+9jUVNAqqYRuxyG254la"
            )
        self.v.codec = "mp3"
        self.v.region = "us-west"

    def getFilename(self, directory, speech, rate, voice_name):
        speech = speech.replace(" ", "").replace("\'","")
        return directory + speech + rate + voice_name + ".mp3"

    def run(self):
        while True:
            event = self.commentatorQueue.get(True)
            # print "Audio renderer recieved commentation."

            timestamp = time.time()
            speech = event.text
            print speech

            rate = "medium"
            voice_name = "Brian"

            output_file = self.getFilename(AUDIO_DIRECTORY, speech, rate, voice_name)
            if not os.path.isfile(output_file):
                self.v.speech_rate = rate
                self.v.voice_name = voice_name
                self.v.fetch_voice(speech, output_file)

            message = {}
            message["audio_file"] = output_file
            message["source"] = 0
            message["volume"] = 0.8
            message["timestamp"] = timestamp

            self.rendererQueue.put(message)
