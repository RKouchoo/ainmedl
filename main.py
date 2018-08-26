import cfscrape
import bs4
import requests

from sys import argv

scraper = cfscrape.create_scraper()

targetSeriesURL = argv[1] # get the target url page
#targetDir = argv[2] # get the input target directory to store the videos

# first string is used in http://ww8.kiss-anime.me
# test url "http://ww8.kiss-anime.me/Anime/30-sai-no-hoken-taiiku"

siteData = scraper.get(targetSeriesURL).content
soup = bs4.BeautifulSoup(siteData)

linksList = {}

# goes through the digest and checks if the returned urls are valid 
# yes crude but works very well. 
for link in soup.find_all('a'):
    tempLink = link.get('href')

    if tempLink.contains('ww8'):
    	linksList.add(tempLink)


for url in linksList:
	print(url)
