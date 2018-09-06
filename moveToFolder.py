# A script when run reads the yaml file and makes a folder to move the current videos into it

import os
import yaml
from sys import argv

import animeDataStore

destYAML = argv[1]

def getVideoFileList(dir):
    path, dirs, files = next(os.walk(dir))
    videoFiles = []

    for file in files:
        if ".mp4" in file:
            videoFiles.append(file)

    return videoFiles

def readYAMLFile(filePath):
    fileData = open(filePath, 'r')
    return fileData.read()


animData = readYAMLFile(destYAML)

def moveVideosToSelectedDir(dir):
    files = getVideoFileList(os.getcwd())

    try:
        os.stat(dir)
    except:
        os.mkdir(dir)

    for file in files:
        print("Moving {} to {}".format(file, dir + "/" + file))
        os.rename(file, dir + "/" + file)  # try and move the file to the directory

folderName = animData.memName.replace(" ", "-") 

moveVideosToSelectedDir(folderName)