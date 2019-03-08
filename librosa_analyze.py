import librosa

class librosaGetFeatures:

    def __init__(self, song):
        self.spectrumArray = []
        self.beats = 0
        self.frames = 0
        self.tempo = 0
        self.path = "/Users/bamforion/Documents/Processing/analyze_track/data/"
        self.y , self.sr = librosa.load(self.path+song)

    def getSpectrumArray(self):
        self.spectrumArray  = librosa.feature.spectral_centroid(y=self.y, sr=self.sr)
        return self.spectrumArray[0]

    def getRhythm(self, type):
        self.tempo,self.beats = librosa.beat.beat_track(y=self.y, sr=self.sr)
        self.frames = librosa.frames_to_time(self.beats, sr=self.sr)

        if(type == "tempo"):
            return self.tempo
        elif(type == "beats"):
            return self.beats
        elif(type == "frames"):
            return self.frames
