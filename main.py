import cfscrape
import bs4
import requests
import re
import selenium
import os

from time import sleep
from sys import argv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chromeOptions = webdriver.ChromeOptions()  
chromeOptions.add_argument("--headless")  
chromeOptions.add_argument('--ignore-certificate-errors')

DDOS_SLEEP_TIME = 10

scraper = cfscrape.create_scraper()

targetSeriesURL = argv[1] # get the target url page
targetDir = argv[2] # get the input target directory to store the videos

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

# create an instance of chrome
mainDriver = webdriver.Chrome(chrome_options=chromeOptions, service_log_path = os.path.devnull)

for i in range(0, listLen):
	currentLink = linksList[i]
	print("Downloading video from: " + currentLink)	
	print("Sleeping for " + str(DDOS_SLEEP_TIME) + " seconds to bypass DDOS protection")
	
	mainDriver.get(currentLink)
	sleep(DDOS_SLEEP_TIME)
	mainDriver.find_element_by_tag_name("body").send_keys("Keys.ESCAPE");

	thisSiteData = mainDriver.page_source	

	newSoup = bs4.BeautifulSoup(thisSiteData, 'html.parser')
	divD = newSoup.find_all('div', {'id':'divDownload'})

	try:
		dLink = divD[0].a.get('href')
		print(dLink)

	except:
		print("failed to find video download link")

	i += 1