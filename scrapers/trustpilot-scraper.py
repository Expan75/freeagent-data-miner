# standard package imports
import csv
import re
import json

from pprint import pprint

# installed Modules
from bs4 import BeautifulSoup
from requests import get
import pandas as pd

# Setup request/res object
# url = 'https://uk.trustpilot.com/review/www.freeagent.com?page=%s' % 1 
# res = get(url)
# html_soup = BeautifulSoup(res.text, 'html.parser')

BASE_URL = 'https://uk.trustpilot.com/review/www.freeagent.com'

# NOTE: this does not check for repeat data or redirects to home page
def initDataFlow(paginatedLimit):
    paginatedLimit += 1
    cachedContent = None

    for n in range(1, paginatedLimit):

        url = BASE_URL + '?page=' + str(n)
        res = getPageRes(url)

        # Handle 404's 
        if res.status_code == 404:
            break

        soup = getSoup(res)
        data = extractReviews(soup)

        # Handle redirect to frontpage when overstepping pagination (cache the first content)
        if data[0]['content'] == cachedContent:
            break

        # Save objects in CSV
        saveObjects(data)

        # only Cache first result (used by error handler)
        if n==1:
            cachedContent = data[0]['content']
    
    """ Data flow finished """
    return
        


def getPageRes(url):
    return get(url)


def getSoup(res):
    return BeautifulSoup(res.text, 'html.parser')


def extractReviews(soup):
    rawReviewData = soup.find_all('script', type="application/ld+json")
    rawReviewsJson = rawReviewData[0].get_text().strip()[:-1]
    decodedReviewsJson = json.loads(rawReviewsJson)
    rawReviews = decodedReviewsJson[0]['review'] 

    return list(map(lambda rawReview: extractedNestedReviewData(rawReview), rawReviews))


def extractedNestedReviewData(review):
    cleanedContent = " ".join(review["reviewBody"].split()).replace('"', '')
    
    reviewObject = {
        "rating"          : review["reviewRating"]["ratingValue"],
        "content"         : cleanedContent,
        "date"            : review["datePublished"],
        "author"          : review["author"]["name"],
        "date"            : review["datePublished"]
    }
    return reviewObject


def saveObjects(objects):
    """ Takes in a list of review objects """
    pd.DataFrame(objects).to_csv('data/trustpilot-reviews.csv', mode='a', header=False, index=False, index_label=False)
    print("wrote " + str(len(objects)) + " reviews to file.")

initDataFlow(99)
