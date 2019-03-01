import csv
import statistics
import difflib
from pathlib import Path

# helper functions
def partitionSongName(alist):
    return alist.split("/",2)[1]

def compareList(a,b):
    # simularities = sum(a == b for a, b in zip(a, b))
    # print("simularities: ",simularities)
    # differences = sum(a != b for a, b in zip(a, b))
    deviationA = statistics.stdev(a)
    # print("deviationA",deviationA)
    # print("abs",deviationA)
    deviationB = statistics.stdev(b)
    # print("differences: ", differences)
    return abs(deviationA - deviationB)

def __createGlobalListFromDirectory__ (directory):
    dataList = []
    # ITERATE THROUGH FILES 
    pathlist = Path(directory).glob('**/*.csv')
    for path in pathlist:
        # filename pathing
        path_in_str = str(path)
        # print(path_in_str)
        # read the file in directory as a csv
        with open(path_in_str, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            # array of values
            valueArray = []
            # empty dict for creating dump file
            d = dict()
            # iterate through each row and fill in dump file with array values
            for row in spamreader:
                if(row[1] != 'value'):
                    valueArray.append(float(row[1]))
            # field names added to object
            d['songName'] = partitionSongName(path_in_str)
            d['values'] = valueArray
            d['songList'] = []
            # append object to global list
            dataList.append(d.copy())
    print('done processing data')
    return dataList

def __createSortedList__(rawList):
    for d in rawList:
        for e in rawList:
            if(d['songName'] != e['songName']):
                # sm = difflib.SequenceMatcher(None,d['values'],e['values'])
                sm = compareList(d['values'], e['values'])
                # obj = [e['songName'], sm.ratio()]
                # print("list compare return: ",sm)
                obj = [e['songName'], sm]
                d['songList'].append(obj)

    for j in rawList:
        sort = sorted(j['songList'], key=lambda song:song[1], reverse=True)
        j['songList'] = sort

    print("done sorting data")
    return rawList

def __writeDataToCSV__(sortedData):
    writeCSV = list()
    header = ["song_name","average","standard_deviation","variance","rank_1_name","rank_1_score","rank_2_name","rank_2_score","rank_3","rank_3_score"]
    writeCSV.append(header)

    for c in sortedData:
        rank_1 = c['songList'][0]
        rank_2 = c['songList'][1]
        rank_3 = c['songList'][2]
        o = [c['songName'], statistics.mean(c['values']),statistics.stdev(c['values'])
        ,statistics.variance(c['values']),rank_1[0],rank_1[1] ,rank_2[0], rank_2[1], rank_3[0],rank_3[1]]
        writeCSV.append(o)

    with open('data.csv', 'w', newline="", encoding="UTF-8") as f:
        writer = csv.writer(f)
        for l in writeCSV:
            writer.writerow(l)

    print("finished writing to CSV")

globalList = __createGlobalListFromDirectory__("./songData")
sortedList = __createSortedList__(globalList)
__writeDataToCSV__(sortedList)