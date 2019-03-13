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
        self.sortedByLowestRank = []
        self.finalCompareList = []
        self.standardDeviation = 0
        self.mean = 0
        self.coefficientVariance = 0

    def splitSongPath(self,inputSongPath):
        return inputSongPath[0].split(".")[0].replace(".mp3", ".ogg")

    # returns absolute value of the songs
    # coefficients of deviation
    def compareCVs(self,a,b):
        return abs(a - b)

    # start the thing
    def startMatching(self):
        song = self.getSong()
        matchedSong = self.createSongArray(song)
        py.playSong(matchedSong) 

    # inputs text, x coordinate, y coordinate
    # clears screen at the top 
    # appends new text to pygame
    def appendText(self, text, locX, locY):
        basicfont = pygame.font.SysFont(None, 48)
        text = basicfont.render(text, True, (255, 0, 0), (255, 255, 255))
        textrect = text.get_rect()
        textrect.centerx = locX
        textrect.centery = locY
        self.screen.blit(text, textrect)
        pygame.display.update()
        self.clock.tick(self.fps)

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

    def startPygame(self):
        # init screen 
        self.screen = pygame.display.set_mode(self.size)
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
                        self.startMatching()

            # fill in screen
            self.screen.fill(self.bg)
            # draw button
            pygame.draw.rect(self.screen, [255, 0, 0], button)  # draw button
            self.appendText("Press Button to Match Song", self.screen.get_rect().centerx, 50)

        pygame.quit()
        sys.exit

    def parseSongInfo(self,matchedSong):
        parseSong = matchedSong[0].split("__",2)
        artist = parseSong[0].replace("_", " ")
        song = parseSong[1].replace(".csv", " ")
        self.screen.fill(self.bg, (0,0,self.screenWidth,200))
        self.appendText(artist, self.screen.get_rect().centerx, 50)
        self.appendText(song, self.screen.get_rect().centerx, 100)

    # input song path from data.csv and plays song
    # using pygame mixer
    def playSong (self,inputSongPath):
        # splits song path from .csv extension and returns song name
        songPath = "/Users/bamforion/Documents/Processing/analyze_track/song_tracks_ogg/"+ self.splitSongPath(inputSongPath) + ".ogg"
        self.parseSongInfo(inputSongPath)

        pygame.mixer.music.load(songPath)
        pygame.mixer.music.play(0)

        while pygame.mixer.music.get_busy():
            pygame.event.poll()
            self.clock.tick(self.fps)

py = pygameObject()
py.startPygame.__init__()
py.startPygame()