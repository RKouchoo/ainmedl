import cfscrape
import bs4
import requests

from sys import argv

scraper = cfscrape.create_scraper()

targetSeriesURL = argv[1] # get the target url page
#targetDir = argv[2] # get the input target directory

matchingStrsPerSite = {"<a href="} # first string is used in http://ww8.kiss-anime.me
# test url "http://ww8.kiss-anime.me/Anime/30-sai-no-hoken-taiiku"

site = scraper.get(targetSeriesURL).content

soup = bs4.BeautifulSoup(site)

for link in soup.find_all('table class=listing'):
    print(link.get('href'))