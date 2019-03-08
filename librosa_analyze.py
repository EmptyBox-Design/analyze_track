import librosa

class getSpectrum:

    def __init__(self):
        self.spectrumArray = []

    def createSongArray(self,inputSongPath):
        print('inputSongPath: ', inputSongPath)
        y , sr = librosa.load("/Users/bamforion/Documents/Processing/analyze_track/data/"+inputSongPath)
        self.spectrumArray  = librosa.feature.spectral_centroid(y=y, sr=sr)
        return self.spectrumArray[0]