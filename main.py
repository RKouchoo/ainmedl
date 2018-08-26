import cfscrape
import bs4
import requests
import re

from sys import argv

scraper = cfscrape.create_scraper()

targetSeriesURL = argv[1] # get the target url page
#targetDir = argv[2] # get the input target directory to store the videos

# first string is used in http://ww8.kiss-anime.me
# test url "http://ww8.kiss-anime.me/Anime/30-sai-no-hoken-taiiku"

siteData = scraper.get(targetSeriesURL).content
soup = bs4.BeautifulSoup(siteData, 'html.parser')

linksList = []

# goes through the digest and checks if the returned urls are valid 
# yes crude but works very well. 
for link in soup.find_all('a'):
    tempLink = link.get('href')

    if 'ww8' in tempLink:
    	linksList.append(tempLink)

# need to flip the list so items are downloaded in order
linksList.reverse()

# now create a loop to download each video
# each iteration should create a new bs and scraper to view the download link of each page.
listLen = len(linksList)

for i in range(0, listLen):
	currentLink = linksList[i]
	print("Downloading video from: " + currentLink)

	thisSiteData = scraper.get(currentLink).content
	newSoup = bs4.BeautifulSoup(thisSiteData, 'html.parser')

	tags = newSoup.find('div', id="container")

	for tag in tags.find_all('div'):
		print(tag)

	i += 1
'''
	for dlLink in newSoup.findAll('a'):
		#theLink = dlLink.get('href')
		print(dlLink)
'''