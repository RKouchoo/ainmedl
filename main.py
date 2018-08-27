import cfscrape
import bs4
import requests
import re
import selenium
import os
import wget


from time import sleep
from sys import argv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException 
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import UnexpectedAlertPresentException

chromeOptions = webdriver.ChromeOptions()  
chromeOptions.add_argument("--headless")  
chromeOptions.add_argument('--ignore-certificate-errors')
chromeOptions.add_argument("--log-level=3")
chromeOptions.add_argument("--silent")
chromeOptions.add_argument("--disable-notifications")
chromeOptions.add_argument("--mute-audio") # some really bitchy ads sometimes come by....

DDOS_SLEEP_TIME = 10

scraper = cfscrape.create_scraper()

targetSeriesURL = argv[1] # get the target url page
targetDir = argv[2] # get the input target directory to store the videos

# first string is used in http://ww8.kiss-anime.me
# test url "http://ww8.kiss-anime.me/Anime/30-sai-no-hoken-taiiku"

print("Grabbing video series urls..")
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
mainDriver = webdriver.Chrome(chrome_options=chromeOptions, service_log_path=os.path.devnull)

# create an empty list to retry downloading a failed video.
retryList = []
downloadURLList = []

for i in range(0, listLen):
	currentLink = linksList[i]
	print("Getting download data from video: " + currentLink)	
	print("Sleeping for " + str(DDOS_SLEEP_TIME) + " seconds to bypass DDOS/bot protection.")
	
	# set the max load time to avoid infinite loading
	mainDriver.set_page_load_timeout(DDOS_SLEEP_TIME)

	thisSiteData = ""

	# handle the infinite load on the site
	try:
		mainDriver.get(currentLink)
		sleep(DDOS_SLEEP_TIME)
	except TimeoutException:
		mainDriver.find_element_by_tag_name("body").send_keys("Keys.ESCAPE");
		thisSiteData = mainDriver.page_source		
	except UnexpectedAlertPresentException:
		#mainDriver.wait_for_and_accept_alert()
		mainDriver.find_element_by_tag_name("body").send_keys("Keys.ESCAPE");
		thisSiteData = mainDriver.page_source
		downloadURLList.append(currentDlLink)
		currentDlLink = ""

	newSoup = bs4.BeautifulSoup(thisSiteData, 'html.parser')
	divD = newSoup.find_all('div', {'id':'divDownload'})
	currentDlLink = ""

	try:
		currentDlLink = divD[0].a.get('href')
		print("Found download link.. " + currentDlLink[17:40]) # show a snippet of the download link
		print("\n")
		downloadURLList.append(currentDlLink)
		currentDlLink = ""
	except:
		if currentDlLink == "" or currentDlLink == "none":
			print("Failed to find video download data for: " + currentLink)
			# add to the retry list so that the video gets run through again.
			retryList.append(i)
			print("Added: " + linksList[i] + " to the retry list")
			print("\n")

	i += 1


if retryList:
	print("\nRetrying to download failed videos!")

	for x in range(0, len(retryList)):
		currentLink = linksList[retryList[x]]

		print("[RETRY] Getting video data from: " + currentLink)	
		print("[RETRY] Sleeping for " + str(DDOS_SLEEP_TIME) + " seconds to bypass DDOS/bot protection.")
		mainDriver.set_page_load_timeout(DDOS_SLEEP_TIME)

		thisSiteData = ""

		try:
			mainDriver.get(currentLink)
			sleep(DDOS_SLEEP_TIME)
		except TimeoutException:
			mainDriver.find_element_by_tag_name("body").send_keys("Keys.ESCAPE");
			thisSiteData = mainDriver.page_source
			downloadURLList.append(currentDlLink)
			currentDlLink = ""
		except UnexpectedAlertPresentException:
			#mainDriver.wait_for_and_accept_alert()
			mainDriver.find_element_by_tag_name("body").send_keys("Keys.ESCAPE");
			thisSiteData = mainDriver.page_source
			downloadURLList.append(currentDlLink)
			currentDlLink = ""
		
		newSoup = bs4.BeautifulSoup(thisSiteData, 'html.parser')
		divD = newSoup.find_all('div', {'id':'divDownload'})

		try:
			currentDlLink = divD[0].a.get('href')
			print("[RETRY] Found download link.. " + currentDlLink[17:40])
			downloadURLList.append(currentDlLink)
		except:
			print("[RETRY] Failed to find video download link...")
			print("[RETRY] Video may of been taken down!")
			sleep(2)
		x += 1

print("Sucsessfully found download links: ")
for a in downloadURLList:
	print(a)

def doDownload(links, path):
	for link in links:
		fName = wget.download(url=link, out=path, bar=bar_thermometer)
		print("Downloaded: " + fName)

doDownload(downloadURLList, targetDir)