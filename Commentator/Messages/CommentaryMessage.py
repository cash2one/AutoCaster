
class CommentaryMessage(object):
    def __init__(self, voice, speech, sourceId, rate, volume, pitch):
        self.voice = voice
        self.speech = speech
        self.sourceId = sourceId
        self.rate = rate
        self.volume = volume
        self.pitch = pitch