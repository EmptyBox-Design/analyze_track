from csvWrite import writeData
from csvread import createDataCSV
import time
from pathlib import Path
wb = writeData()
cd = createDataCSV()

# remove diretory from song path
def partitionSongName(songPath):
    return songPath.split("/",2)[1]

def removeSongExtension(songPath):
    return songPath.split(".",2)[0]

# checks to see if song has already been processed
def checkIfSongIsAlreadyCreated(songPath):
    pathList = Path("./songData").glob("**/*.csv")
    check = False
    for d in pathList:
        pathToString = str(d)
        songPath = removeSongExtension(songPath)
        pathToString = removeSongExtension(partitionSongName(pathToString))
        if(pathToString == songPath):
            check = True

    return check
# creates a list of all the songs in the data directory
# these songs will be passed to be processed
def createGlobalListFromDirectory (directory):
    songList = []
    # ITERATE THROUGH FILES 
    pathlist = Path(directory).glob('**/*.mp3')
    for path in pathlist:
        pathToString = str(path)
        songPath = partitionSongName(pathToString)

        if(checkIfSongIsAlreadyCreated(songPath) == False):
            songList.append(songPath)

    return songList
        
# input list of song paths
# creates csv's for each song 
# CSV contains index, frame, beat of each entire song
# CSVs are placed in songData directory
def generateSongData(songList):
    start = time.time()
    counter = len(songList)
    for song in songList:
        wb.write(song, song)
        counter-=1
        print(counter,"/", len(songList))
    end = time.time()
    print('Finished',end - start)
    cd.createGlobalListFromDirectory("./songData")

# input is directory to look in
# output is a list of songs to generate fils for
listSongsPaths = createGlobalListFromDirectory("./data")
generateSongData(listSongsPaths)
