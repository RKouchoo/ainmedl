import os
from sys import argv

from anime_downloader import get_anime_class

# Class refrence: https://github.com/vn-ki/anime-downloader/wiki/Package-documentation

targetSeriesURL = argv[1]  # the target series to index and download

print("Getting video meta-data for the url: {}".format(targetSeriesURL))
kissAnimeInterface = get_anime_class('kissanime')
currentAnime = kissAnimeInterface(targetSeriesURL)
currentAnimeName = currentAnime.title

episodes = len(currentAnime)
print("Found {} videos in this series to download. \n".format(episodes))
print("Downloading {} episdoes. This may take some time!".format(episodes))

# for every episode we want to download it
for i in range(0, episodes):
    print("Downloading episode ({} of {}). Name: {}".format(currentAnime[i].ep_no, episodes, currentAnime.pretty_title))
    currentAnime[i].download()  # download the episode to the current drectory.


def getVideoFileList(dir):
    path, dirs, files = next(os.walk(dir))
    videoFiles = []

    for file in files:
        if ".mp4" in file:
            videoFiles.append(file)

    return videoFiles


def moveVideosToSelectedDir(dir):
    files = getVideoFileList("~")

    try:
        os.stat(dir)
    except:
        os.mkdir(dir)


for file in files:
    print("Moving {} to {}".format(file, dir + "/" + file))
    os.rename(file, dir + "/" + file)  # try and move the file to the directory

moveVideosToSelectedDir(currentAnimeName)
