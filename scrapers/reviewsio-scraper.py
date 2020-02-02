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
# Example of Page 2: https://www.reviews.co.uk/company-reviews/store/freeagent/1


def extractReviews(soup):
    """ takes in a soup object and returns the innards of the indexed script """

    # Gets raw json and parse
    rawReviewData = soup.find_all('script', type="application/ld+json")
    rawReviewsJson = rawReviewData[0].get_text().strip()
    decodedReviewsJson = json.loads(rawReviewsJson)
    rawReviews = decodedReviewsJson['review'] 

    # extract reviews and return reviews
    return list(map(lambda rawReview: extractReviewData(rawReview), rawReviews))


def extractReviewData(rawReviewObject):
    """ takes in a review object and transforms it into one of the following dict: """

    reviewObject = {
        "rating"          : rawReviewObject["reviewRating"]["ratingValue"],
        "content"         : rawReviewObject['reviewBody'],
        "date"            : rawReviewObject["datePublished"],
        "author"          : rawReviewObject["author"]["name"],
        "date"            : rawReviewObject["datePublished"]
    }

    return reviewObject


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
        data = extractReviews(soup)

        # save objects and log it
        loggedResults += saveObjects(data, "data/reviews-io-reviews.csv")

    return "Ended gracefully with %s saved." %loggedResults

print(initDataFlow(99))