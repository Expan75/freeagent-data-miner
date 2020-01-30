# standard package general imports
import csv
import re
import json

# standard package specific imports
from time import sleep

# installed Modules
from bs4 import BeautifulSoup
import pandas as pd

# Relative Imports (util functions)
from utils import getPageRes, getSoup, saveObjects

# CONSTS
BASE_URL = 'https://www.reviews.co.uk/company-reviews/store/freeagent'
# example of page 2

# # https://www.reviews.co.uk/company-reviews/store/freeagent/1

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


def getReviewText(soup):

    # Text is actually wrapped inside a script tag as JSON data
    data = soup.find_all('script', 'application/ld+json')
    print(data)
    return data

res = getPageRes(BASE_URL)
soup = getSoup(res)

# ratingDivs = getRatingDivs(soup)
# ratingTexts = getRatings(ratingDivs)

import json

def extractScriptInnards(soup, index):
    """ takes in a soup object and returns the innards of the indexed script """

    # Gets raw json and parse
    jsonAsString = soup.find_all('script')[index].get_text().strip()
    loadedJson = json.loads(jsonAsString)

    # extract reviews and return reviews
    return loadedJson['review']


def extractReviewData(review):
    """ takes in a review object and transforms it into one of the following dict: 
        'reviewText' : str,
        'reviewValue' : str,
        'datePublished' : str,
    """

    # Extract rel. info
    reviewText = review['reviewBody']
    reviewValue = review['reviewRating']['ratingValue']
    datePublished = review['datePublished']

    return {
        "reviewText": reviewText,
        "reviewValue": reviewValue,
        "datePublished": datePublished
    }




rawScriptInnard = extractScriptInnards(soup, 8)

print(extractReviewData(rawScriptInnard[0]))


# sorted_string = json.dumps(loadedJson, indent=4, sort_keys=False)
# print(sorted_string)