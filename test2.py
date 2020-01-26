# standard package imports
import re
import csv

# installed Modules
from bs4 import BeautifulSoup
from requests import get
import pandas as pd

BASE_URL = 'https://www.softwareadvice.com/accounting/freeagent-profile/reviews/'
# https://www.softwareadvice.com/accounting/freeagent-profile/reviews/?review.page=1

"""

TODO: 
        1. Rewrite scrape rules (allow for fusing pros & cons section)
                - if n of results < than last n results => probably final page
        2. Handle redirect to last result

"""

def getPageRes(url):
    """ takes in a string URL a returns a requests response object """
    return get(url)

def getSoup(res):
    """ takes in a requests res object and returns a beautiful soup HTML object """
    return BeautifulSoup(res.text, 'html.parser')


def getReviewScores(soup):
    """ takes in a soup object and extracts all the reviewScores, returns a list of strings """
    reviewScores = soup.find_all('div', class_=re.compile(r'new-stars-rank__'))
    return list(map(lambda tagComponents: tagComponents['class'][-1], reviewScores))


def getReviewTitles(soup):
    """ takes in a soup object and extracts all the reviewTitles, returns a list of strings """
    extractedTitlesText = soup.find_all('p', class_='review-copy-header strong')
    return list(map(lambda tagComponenets: tagComponenets.text, extractedTitlesText))


def getReviewContents(soup):
    """ takes in a soup object and extracts all the review contents, returns a list of strings"""
    reviewContainerDivs = soup.find_all('div', class_='review-copy-container')
    
    # gets all p-tags stored in reviews
    reviewContainerPtags = list(map(lambda x: x.find_all('p', class_='ui'), reviewContainerDivs))

    return extractReviewContents(reviewContainerPtags)


def extractReviewContents(listOfContainersPtags):
    """ takes a list of lists (containerPtags) and returns a list of review contents """

    reviewContents = []
    for setOfPtags in listOfContainersPtags:
        extractedPtext = list(map(lambda x: x.text, setOfPtags))

        # Handle missing info by simply subbing review info for empty string
        if len(extractedPtext) < 4:
            reviewContents.append("")
        else:
            content = extractedPtext[-3] + extractedPtext[-1] 
            reviewContents.append(content)

    return reviewContents

def constructReviewObjects(scores, titles, contents):

    reviewObjects = []
    for index, content in enumerate(contents, 0):
        review = {
            "score": scores[index],
            "title": titles[index],
            "content": content
        }
        reviewObjects.append(review)

    return reviewObjects

# just double checkin
soup = getSoup(getPageRes(BASE_URL+'?review.page='+str(1)))

scores      = getReviewScores(soup)
titles      = getReviewTitles(soup)
contents    = getReviewContents(soup)

reviews = constructReviewObjects(scores, titles, contents)


def printNfirstObjects(n, objects):
    """ outputs the first n (int input) objects in a given list of objects; returns nothing """
    listOfObjects = constructReviewObjects(scores, titles, contents)
    for obj in listOfObjects[:n]:
        print("")
        print(obj)
        print("")
    return "Output done! printed: %s objects" %n 

printNfirstObjects(15, reviews)