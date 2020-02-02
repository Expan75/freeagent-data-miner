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

BASE_URL = 'https://www.softwareadvice.com/accounting/freeagent-profile/reviews/'
# example of page 2
# https://www.softwareadvice.com/accounting/freeagent-profile/reviews/?review.page=1

"""

TODO: 
        1. Rewrite scrape rules (allow for fusing pros & cons section)
                - if n of results < than last n results => probably final page
        2. Handle redirect to last result

"""

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
    """ takes lists of extracted scores, titles & contents, and returns a list with assembled review objects. """

    reviewObjects = []
    for index, content in enumerate(contents, 0):
        review = {
            "score": scores[index],
            "title": titles[index],
            "content": content
        }
        reviewObjects.append(review)

    return reviewObjects

# trial Dataflow & Debugging
# soup = getSoup(getPageRes(BASE_URL+'?review.page='+str(1)))

# scores      = getReviewScores(soup)
# titles      = getReviewTitles(soup)
# contents    = getReviewContents(soup)

# reviews = constructReviewObjects(scores, titles, contents)

# DEBUG FUNCTION
# def printNfirstObjects(n, objects):
#     """ outputs the first n (int input) objects in a given list of objects; returns nothing """
#     listOfObjects = constructReviewObjects(scores, titles, contents)
#     for obj in listOfObjects[:n]:
#         print("")
#         print(obj)
#         print("")
#     return "Output done! printed: %s objects" %n 
# printNfirstObjects(15, reviews)

def initDataFlow(maxPageLimit):
    """ inits scraping loop for each page until reaching maxPageLimit or when directed to already seen results """

    cachedContent = {
        "score": None,
        "title": None,
        "content": None
    }

    nReviewsSaved = 0

    for page_index in range(1, maxPageLimit+1):
        # print("loop Iteration %s" %page_index)
        # construct specific page url and get a soup object for the served HTML doc
        soup = getSoup(getPageRes(BASE_URL+'?review.page='+str(page_index)))

        scores      = getReviewScores(soup)
        titles      = getReviewTitles(soup)
        contents    = getReviewContents(soup)
        
        # constructs a list of review objects
        reviews = constructReviewObjects(scores, titles, contents)

        # print("printing CachedContent: %s" %cachedContent)
        # check cache if repeating content
        # print("printing reviews[0]: %s" %reviews[0])
        if reviews[0] == cachedContent:
            break

        # cache setup
        if page_index == 1:
            cachedContent = reviews[0]

        # and writes them to csv
        nReviewsSaved += saveObjects(reviews, "data/sw-advice-reviews.csv")
    
    print("dataflow ended gracefully with %s saved results." %nReviewsSaved)
    return

initDataFlow(100)