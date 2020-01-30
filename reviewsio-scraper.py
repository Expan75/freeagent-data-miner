# standard package general imports
import csv
import re
import json

# standard package specific imports
from time import sleep

# installed Modules
from bs4 import BeautifulSoup
import pandas as pd
from requests import get


# Relative Imports (util functions)
from utils import getPageRes, getSoup, saveObjects

# CONSTS
BASE_URL = 'https://www.reviews.co.uk/company-reviews/store/freeagent'
# example of page 2
# # https://www.reviews.co.uk/company-reviews/store/freeagent/1


def getReviewText(soup):
    """ extracts all the script tags within a soup object """
    # Text is actually wrapped inside a script tag as JSON data
    data = soup.find_all('script', 'application/ld+json')

    return data


def extractScriptInnards(soup, index):
    """ takes in a soup object and returns the innards of the indexed script """

    # Gets raw json and parse
    jsonAsString = soup.find_all('script')[index].get_text().strip()
    loadedJson = json.loads(jsonAsString)

    # extract reviews and return reviews
    return loadedJson['review']


def extractReviewData(reviewObject):
    """ takes in a review object and transforms it into one of the following dict: 
        'reviewText' : str,
        'reviewValue' : str,
        'datePublished' : str,
    """

    # Extract rel. info
    reviewText = reviewObject['reviewBody']
    reviewValue = reviewObject['reviewRating']['ratingValue']
    datePublished = reviewObject['datePublished']

    return {
        "reviewValue": reviewValue,
        "reviewText": reviewText,
        "datePublished": datePublished
    }


def transformRawReviewData(rawReviewData):
    """ transforms rawReviewsData into a list of object contianing only rel. info """
    return list(map(lambda rawObject: extractReviewData(rawObject), rawReviewData))


def initDataFlow(maxPageLimit):
    """ Continually scrapes review objects and saves them to file until hitting 404 """
    
    loggedResults = 0

    for resultPageIndex in range(0, maxPageLimit):
        # for n == 1; basic URL is fine
        constructedURL = BASE_URL
        if resultPageIndex >= 1:
            constructedURL = constructedURL + '/%s' %resultPageIndex

        # get page soup & handle potential 404s
        res = getPageRes(constructedURL)
        if str(res.status_code) == '404':
            break

        soup = getSoup(res)

        # TODO: find a better way than to hardcode index
        rawReviewData = extractScriptInnards(soup, 8)
        data = transformRawReviewData(rawReviewData)

        # save objects and log it
        loggedResults += saveObjects(data, "data/reviews-io-reviews.csv")

    return "Ended gracefully with %s saved." %loggedResults

print(initDataFlow(99))