# standard package general imports
import re
import csv

# standard package specific imports
from time import sleep

# installed Modules
from bs4 import BeautifulSoup
import pandas as pd

# Relative Imports (util functions)
from utils import getPageRes, getSoup, saveObjects

# Selinum Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# CONSTS
BASE_URL = 'https://www.reviews.co.uk/company-reviews/store/freeagent'
# example of page 2
# https://www.reviews.co.uk/company-reviews/store/freeagent/1
WEB_DRIVER_PATH = '/Users/Erik/downloads/chromedriver'

# # Init Selenium Object /w headless
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')  # Last I checked this was necessary.
# driver = webdriver.Chrome(WEB_DRIVER_PATH, options=options)

# # Navigates to results
# driver.get('https://www.reviews.co.uk/company-reviews/store/freeagent')

# # Waits until review text is rendered
# try:
#     myElem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'Review__quotationMark')))
#     print("Page is ready!")
# except TimeoutException:
#     print("Loading took too much time!")

# # Run scraping functions on now rendered page

# soup = getSoup(driver.page_source, usingDriver=True)




def getRatingDivs(soup):
    """ takes in a soup object and returns all the reviews' rating divs """
    return soup.find_all('div', class_='Review__overallStars__stars')


def numerifyStarStringList(starStringList):
    """ Helper method for converting star icons into a numerical measure """

    rating = 0
    for starString in starStringList:
        # handle full stars
        if starString == 'icon-full-star-01':
            rating += 1
        else:
            continue
    return rating


def getRatings(ratingDivs):
    """ extracts and return the numerical rating of every review div; returns a list of int:s """

    ratingElements = list(map(lambda ratingDiv: ratingDiv.find_all('i'), ratingDivs))
    
    # convert list of ratingElements to their respective class texts
    textifiedRatingsElements = list(map(lambda: [ itag['class'][1] for itag in x if itag ], ratingElements))
    
    # convert that into a simple numerical measure
    numericalRatings = list(map(lambda x: numerifyStarStringList(x), textifiedRatingsElements))

    return numericalRatings


res = getSoup(BASE_URL, usingDriver=True)
soup = BeautifulSoup(res)

def getReviewText(soup):

    # Text is actually wrapped inside a script tag as JSON data
    data = soup.find_all('script', 'application/ld+json')
    print(data)
    return data


# ratingDivs = getRatingDivs(soup)
# ratingTexts = getRatings(ratingDivs)


getReviewText(soup)