import os
from os import walk
from datetime import datetime
import pandas as pd
from functools import lru_cache
import timeit

from os import listdir
from os.path import isfile, join

onlyfiles = list()

@lru_cache(maxsize=10000)
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles
start_time = timeit.default_timer()
a = '//midptmediap01/mftsharef/'
onlyfiles = getListOfFiles(a)

#TIMER
elapsed = timeit.default_timer() - start_time
print('Run time:'+str(elapsed))
print(len(onlyfiles))

rows = zip(onlyfiles)
import csv

with open('mft_files.csv', "w") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)