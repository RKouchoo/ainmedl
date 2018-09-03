import os
import yaml
from sys import argv
from anime_downloader.sites import get_anime_class

import animeDataStore

# Class refrence: https://github.com/vn-ki/anime-downloader/wiki/Package-documentation

targetSeriesURL = argv[1]  # the target series to index and download


def getVideoFileList(dir):
    path, dirs, files = next(os.walk(dir))
    videoFiles = []

    for file in files:
        if ".mp4" in file:
            videoFiles.append(file)

    return videoFiles


def writeYAMLStringToFile(name, string):
    with open(name + '.yaml', "w+") as textFile:
        sys.stdout.flush()
        sys.stdout.write("\n Writing out cache file: {} ".format(name))
        sys.stdout.flush()
        textFile.write(string)


def generateYAMLString(animName, animLength, current):
    data = animeDataStore.animeInfo(animName, animLength, current)

    return yaml.dump(data)


def checkForAnimeYamlFile(dir):
    path, dirs, files = next(os.walk(dir))
    yamlFiles = []
    
    for yaml in files:
        if "yaml" = yaml:
            yamlFiles.append(yaml)

    return yamlFiles


 def readYAMLFile(filePath):
    fileData = open(filePath, 'r')
    return fileData.read()


def fromYAMLString(data):
    return yaml.load(data)


def getCurrentEpisodeFromYaml(yamls, animName):
    pos = 0    
    for yaml in yamls:
        data = readYAMLFile(yaml)
        animObject = fromYAMLString(data)

        # check if the file has the correct name
        if animObject.memName = animName:
            # we have the correct anime json file found
            pos = animObject.memCurrent
        else:
            pos = -1 # shows that there were no pos entries found.

    return pos


def moveVideosToSelectedDir(dir):
    files = getVideoFileList(os.getcwd())

    try:
        os.stat(dir)
    except:
        os.mkdir(dir)

    for file in files:
        print("Moving {} to {}".format(file, dir + "/" + file))
        os.rename(file, dir + "/" + file)  # try and move the file to the directory


def getDownloadFromUrl(url):
    print("Getting video meta-data for the url: {}".format(url))
    kissAnimeInterface = get_anime_class('kissanime')
    currentAnime = kissAnimeInterface(url, quality="480p")
    currentAnimeName = currentAnime.title

    episodes = len(currentAnime)
    print("Found {} videos in this series to download. \n".format(episodes))
    print("Downloading {} episdoes. This may take some time!".format(episodes))
    redownload = []

    # for every episode we want to download it
    for i in range(0, episodes):
        title = currentAnime[i].pretty_title
        print("Downloading episode ({} of {}). Name: {}".format(currentAnime[i].ep_no, episodes, title))
        try:
            currentAnime[i].download()  # download the episode to the current drectory.
        except:
            print("Encountered an error downloading the video: {}. Adding {} to be re-downloaded".format(title, title))
            redownload.append(i)

        # redownload failed videos. If they fail again then they aren't going to be dowloaded
        # might implement a persistent loop  
        for x in redownload:
            print("[RETRY]: Downloading episode ({} of {}). Name: {}".format(currentAnime[x].ep_no, episodes, currentAnime[x].pretty_title))
            try:
                currentAnime[x].download()
            except:
                print("Failed to download {}. Please download it manually!".format(currentAnime[x].pretty_title))

        redownload = []

    # once the files have been downloaded move them to the correct directory
    moveVideosToSelectedDir(currentAnimeName)



getDownloadFromUrl(targetSeriesURL)
