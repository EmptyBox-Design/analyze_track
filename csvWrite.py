import csv
import statistics
import numpy
from librosa_analyze import librosaGetFeatures
 
class writeData:
    def __init__(self):
        self.writeCSV = list()

    def removeSongExtension(self,songPath):
        return songPath.split(".",2)[0]

    def getSpectrumStats(self,a):
        sd = statistics.stdev(a)
        mean = statistics.mean(a)
        cv = (sd/mean)*100

        return [sd, mean, cv]

    def createSongData(self,songPath):
        print('songPath: ', songPath)
        lb = librosaGetFeatures(songPath)
        cent = lb.getSpectrumArray()
        return self.getSpectrumStats(cent)

    def write(self,inputSong, songName):
        
        header = ["spectrumStandardDeviation","spectrumMean", "spectrumCoefficientVariance"]
        self.writeCSV.append(header)

        with open("./SongData/"+self.removeSongExtension(songName)+".csv",'w', newline="", encoding="UTF-8") as f:
            writer = csv.writer(f)
            
            data = self.createSongData(inputSong)
            writer.writerow(header)
            writer.writerow(data)

        return True
