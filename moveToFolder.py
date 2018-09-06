# A script when run reads the yaml file and makes a folder to move the current videos into it

import os
import yaml
from sys import argv

import animeDataStore # need this here so yaml knows what to refrence

destYAML = argv[1]


def getVideoFileList(dir):
    path, dirs, files = next(os.walk(dir))
    videoFiles = []

    for file in files:
        if ".mp4" in file:
            videoFiles.append(file)

    return videoFiles


# reads in the
def readYAMLFile(filePath):
    fileData = open(filePath, 'r')
    return fileData.read()


# returns an object after it is parsed though yaml
def fromYAMLString(data):
    return yaml.load(data)


# moves the videos from the current directory into a new folder
def moveVideosToSelectedDir(dir):
    files = getVideoFileList(os.getcwd())

    try:
        os.stat(dir)
    except:
        os.mkdir(dir)

    for file in files:
        print("Moving {} to {}".format(file, dir + "/" + file))
        os.rename(file, dir + "/" + file)  # try and move the file to the directory


# main method calls here
animData = readYAMLFile(os.getcwd() + destYAML)
animObject = fromYAMLString(animData)
folderName = animObject.memName.replace(" ", "-") 
moveVideosToSelectedDir(folderName)