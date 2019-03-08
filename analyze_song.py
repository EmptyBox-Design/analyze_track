import csv
import statistics
from librosa_analyze import librosaGetFeatures
import pygame
from pygame import mixer

def compareCVs(a,b):
    return abs(a - b)

def splitSongPath(inputSongPath):
    print('inputSongPath: ', inputSongPath[0].split(".")[0])
    return inputSongPath[0].split(".")[0]

# inputs new song to be compared against data.csv
# this returns an array of spectrum results as a list
# this will fire when a user interacts with the pygame button
# sending a song file to be compared and matched with
def createSongArray (song):
    # print('song: ', song)
    # dump array
    # currentSongArray = []
    # init librosa comparison 
    lb = librosaGetFeatures(song)
    inputSongArray = lb.getSpectrumArray()
    # print('inputSongArray: ', inputSongArray)
    standarDeviation = statistics.stdev(inputSongArray)
    print('standarDeviation: ', standarDeviation)
    mean = statistics.mean(inputSongArray)
    print('mean: ', mean)
    coefficientVariance = (standarDeviation/mean) *100
    print('coefficientVariance: ', coefficientVariance)
    # temp file created to house song data to be compared
    # not sure if I want to write this to disk
    # or hold it in temp memory
    # with open("./tempFile/"+song, newline='') as songFile:
    #     f = csv.reader(songFile, delimiter=",",quotechar='|')
        
    #     for row in f:
    #         if(row[1] != 'value'):
    #             currentSongArray.append(float(row[1]))
    match = matchAgainstSongs(coefficientVariance)
    print('match: ', match)
    playSong(match)

def matchAgainstSongs (coefficientVariance):
    with open("data.csv", newline='') as csvfile:
        f = csv.reader(csvfile, delimiter=',', quotechar='|')

        finalCompareList = []
        # skip header row
        for row in f:
            if(row[1] != "spectrumMean"):
                # input input songs CV, and comparision songs CV
                # output is the difference
                compare = compareCVs(coefficientVariance, float(row[3]))
                # append to list for sorting 
                finalCompareList.append((row[0], compare))
        # sort in decending order
        sortedByLowestRank = sorted(finalCompareList, key=lambda tup: tup[1])
        # print('sortedByLowestRank: ', sortedByLowestRank)
        # return lowest value
        return sortedByLowestRank[0]

def playSong (inputSongPath):
    pygame.init()
    pygame.display.set_mode((200,100))
    pygame.mixer.music.load("/Users/bamforion/Documents/Processing/analyze_track/data/"+splitSongPath(inputSongPath)+".mp3")
    pygame.mixer.music.play(0)

    clock = pygame.time.Clock()
    clock.tick(10)
    while pygame.mixer.music.get_busy():
        pygame.event.poll()
        clock.tick(10)

createSongArray("avenged_sevenfold__almost_easy.mp3")