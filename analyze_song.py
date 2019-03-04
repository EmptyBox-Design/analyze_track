import csv
import statistics

def compareList(a,deviationB):
    deviationA = statistics.stdev(a)
    deviationDifference = abs(deviationA - deviationB)
    return deviationDifference

def createSongArray (song):
    currentSongArray = []

    with open(song, newline='') as songFile:
        f = csv.reader(songFile, delimiter=",",quotechar='|')
        
        for row in f:
            if(row[1] != 'value'):
                currentSongArray.append(float(row[1]))

    return currentSongArray
                    
def matchAgainstSongs (currentSongArray):
    with open("data.csv", newline='') as csvfile:
        f = csv.reader(csvfile, delimiter=',', quotechar='|')

        finalCompareList = []

        for row in f:
            if(row[2] != "standard_deviation"):

                compare = compareList(currentSongArray, float(row[2]))
                finalCompareList.append((row[0], compare))

        sortedByLowestRank = sorted(finalCompareList, key=lambda tup: tup[1])

        return sortedByLowestRank[0]

createdSongArrays = createSongArray('songData/all_star.csv')
comparasionMatch = matchAgainstSongs(createdSongArrays)
