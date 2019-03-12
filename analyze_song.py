import csv
import statistics
from librosa_analyze import librosaGetFeatures
import pygame
import sys

class pygameObject:

    def __init__(self):
        pygame.init()
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.song = None
        self.screenWidth = 500
        self.screenHeight = 500
        self.buttonWidth = 100
        self.buttonHeight = 100
        self.buttonXPos = self.screenWidth/2 - self.buttonWidth/2
        self.buttonYPos = self.screenHeight/2 - self.buttonHeight/2
        self.size = [self.screenWidth, self.screenHeight]
        self.bg = [255, 255, 255]
        self.startPygame()

    def splitSongPath(inputSongPath):
        return inputSongPath[0].split(".")[0].replace(".mp3", ".ogg")

    def startPygame(self):
        # init screen 
        screen = pygame.display.set_mode(self.size)
        # creates button object
        button = pygame.Rect(self.buttonXPos, self.buttonYPos, self.buttonWidth, self.buttonHeight)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # gets mouse position

                    # checks if mouse position is over the button
                    # use collider function
                    if button.collidepoint(mouse_pos):
                        # prints current location of mouse
                        print('button was pressed at {0}'.format(mouse_pos))
                        matchSongs()
                        
            # fill in screen
            screen.fill(self.bg)
            # draw button
            pygame.draw.rect(screen, [255, 0, 0], button)  # draw button

            pygame.display.update()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit

    # input song path from data.csv and plays song
    # using pygame mixer
    def playSong (self,inputSongPath):
        # splits song path from .csv extension and returns song name
        songPath = "/Users/bamforion/Documents/Processing/analyze_track/song_tracks_ogg/"+ self.splitSongPath(inputSongPath) + ".ogg"

        pygame.mixer.music.load(songPath)
        pygame.mixer.music.play(0)

        # while pygame.mixer.music.get_busy():
        #     pygame.event.poll()
        #     self.clock.tick(self.fps)

class matchSongs:

    def __init__(self):
        self.sortedByLowestRank = []
        self.finalCompareList = []
        self.standardDeviation = 0
        self.mean = 0
        self.coefficientVariance = 0
        self.startMathcing()
    # returns absolute value of the songs
    # coefficients of deviation
    def compareCVs(self,a,b):
        return abs(a - b)

    # start the thing
    def startMathcing(self):
        song = self.getSong()
        matchedSong = self.createSongArray(song)
        pygameObject.playSong(pygameObject,matchedSong)      

    # returns song from sample folder
    def getSong(self):
        return "/Users/bamforion/Documents/Processing/analyze_track/inputSong/sample.mp3"

    # inputs new song to be compared against data.csv
    # this returns an array of spectrum results as a list
    # this will fire when a user interacts with the pygame button
    # sending a song file to be compared and matched with
    def createSongArray (self,song):
        # dump array
        # init librosa comparison 
        
        lb = librosaGetFeatures(song)
        inputSongArray = lb.getSpectrumArray()
        self.standarDeviation = statistics.stdev(inputSongArray)
        self.mean = statistics.mean(inputSongArray)
        self.coefficientVariance = (self.standarDeviation/self.mean) *100
        return self.matchAgainstSongs(self.coefficientVariance)

    def matchAgainstSongs (self,coefficientVariance):
        with open("data.csv", newline='') as csvfile:
            f = csv.reader(csvfile, delimiter=',', quotechar='|')
            # skip header row
            for row in f:
                if(row[1] != "spectrumMean"):
                    # input input songs CV, and comparision songs CV
                    # output is the difference
                    compare = self.compareCVs(coefficientVariance, float(row[3]))
                    # append to list for sorting 
                    self.finalCompareList.append((row[0], compare))
            # sort in decending order
            self.sortedByLowestRank = sorted(self.finalCompareList, key=lambda tup: tup[1])
            # return lowest value
            return self.sortedByLowestRank[0]

py = pygameObject()