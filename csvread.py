import csv
import statistics
from pathlib import Path

class createDataCSV:

    def __init__(self):
        self.dataList = []
        self.writeCSV = list()

    # helper functions
    def partitionSongName(self,alist):
        return alist.split("/",2)[1]

    def compareList(self,a,b):

        sdA = statistics.stdev(a)
        meanA = statistics.mean(a)
        cvA = (sdA/meanA)*100

        sdB = statistics.stdev(b)
        meanB = statistics.mean(b)
        cvB = (sdB/meanB)*100

        return abs(cvA - cvB)

    # creates list from song data directory
    def createGlobalListFromDirectory (self,directory):
        # ITERATE THROUGH FILES with .csv extension
        pathlist = Path(directory).glob('**/*.csv')
        for path in pathlist:
            # filename pathing
            path_in_str = str(path)
            # read the file in directory as a csv
            with open(path_in_str, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                # array of values
                valueArray = []
                # empty dict for creating dump file
                d = dict()
                # iterate through each row and fill in dump file with array values
                for row in reader:
                    # dummy check to exclue header row
                    if(row[1] != 'frame'):
                        # append spectrum reading to list
                        valueArray.append(float(row[3]))

                # field names added to object
                d['songName'] = self.partitionSongName(path_in_str)
                d['values'] = valueArray
                d['songList'] = []
                # append object to global list
                self.dataList.append(d.copy())

        sortedList = self.createSortedList(self.dataList)
        self.writeDataToCSV(sortedList)

    def createSortedList(self,rawList):
        # loop through each song in list unless
        # song names match
        for d in rawList:
            for e in rawList:
                if(d['songName'] != e['songName']):
                    sm = self.compareList(d['values'], e['values'])
                    obj = [e['songName'], sm]
                    d['songList'].append(obj)

        for j in rawList:
            sort = sorted(j['songList'], key=lambda song:song[1])
            j['songList'] = sort

        print("done sorting data")
        return rawList

    def writeDataToCSV(self,sortedData):
        header = ["song_name","average","standard_deviation","variance","coefficent_variance","rank_1_name","rank_1_score","rank_2_name","rank_2_score","rank_3_name","rank_3_score"]
        self.writeCSV.append(header)

        for c in sortedData:
            average = statistics.mean(c['values'])
            standardDeviation = statistics.stdev(c['values'])
            variance = statistics.variance(c['values'])
            coefficentVariance = (standardDeviation/average)*100
            rank_1 = c['songList'][0]
            rank_2 = c['songList'][1]
            rank_3 = c['songList'][2]
            o = [c['songName'], average, standardDeviation, variance, coefficentVariance
            ,rank_1[0],rank_1[1] ,rank_2[0], rank_2[1], rank_3[0],rank_3[1]]
            self.writeCSV.append(o)

        with open('data.csv', 'w', newline="", encoding="UTF-8") as f:
            writer = csv.writer(f)
            for l in self.writeCSV:
                writer.writerow(l)

        print("finished writing to CSV")



