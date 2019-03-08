import csv
import librosa
import numpy

class writeData:
    def __init__(self):
        self.writeCSV = list()

    def removeSongExtension(self,songPath):
        return songPath.split(".",2)[0]

    def mergeArrays(self, a, b, c):
        mergeArray = list()
        
        j = 0
        while j < len(a):
            mergeArray.append([j,a[j], b[j], c[j]])
            j +=1

        return mergeArray

    def createSongData(self,songPath):
        print('songPath: ', songPath)
        y , sr = librosa.load(songPath)
        tempo,beats = librosa.beat.beat_track(y=y, sr=sr)
        frames = librosa.frames_to_time(beats, sr=sr)
        cent = librosa.feature.spectral_centroid(y=y, sr=sr)

        return self.mergeArrays(frames, beats, cent[0])

    def write(self,inputSong, songName):
        
        header = ["index","frame","value","spectrum"]
        self.writeCSV.append(header)

        with open("./SongData/"+self.removeSongExtension(songName)+".csv",'w', newline="", encoding="UTF-8") as f:
            writer = csv.writer(f)

            k = 0
            data = self.createSongData(inputSong)
            while k < len(data):
                if(k == 0):
                    writer.writerow(header)
                writer.writerow(data[k])
                k += 1

        return True
