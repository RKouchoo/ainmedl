import os
from sys import argv

from anime_downloader import get_anime_class

# Class refrence: https://github.com/vn-ki/anime-downloader/wiki/Package-documentation

targetSeriesURL = argv[1] # the target series to index and download
#targetDirectory = argv[2] # the target path to download  

print("Getting video meta-data for the url: {}".format(targetSeriesURL))
kissAnimeInterface = get_anime_class('kissanime')
currentAnime = kissAnimeInterface(targetSeriesURL)
currentAnimeName = currentAnime.title

episodes = len(currentAnime)
print("Found {} videos in this series to download. \n".format(episodes))
print("Downloading {} episdoes. This may take some time!".format(episodes))

# for every episode we want to download it
for i in range(0, episodes):
	print("Downloading episode ({} of {}). Name: {}".format(currentAnime[i].pretty_title, episodes, currentAnime.title))
	currentAnime[i].download() # download the episode to the current drectory.

def moveVideosToSelectedDir():
	
