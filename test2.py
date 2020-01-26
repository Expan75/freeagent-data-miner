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



soup = getSoup(getPageRes(BASE_URL+'?review.page='+str(1)))

# # Should not include first result as this is merely the page summary
# reviewScores = soup.find_all('div', class_=re.compile(r'new-stars-rank__')) 
# # print(reviewScores[1]['class'][-1])

# # returns all the objects containing the review titles
# reviewTitles = soup.find_all('p', class_='review-copy-header strong')

# print(reviewTitles[0].text)

# gets all review containers
reviewContainerDivs = soup.find_all('div', class_='review-copy-container')

# gets all p-tags stored in reviews
reviewContainerPtags = list(map(lambda x: x.find_all('p', class_='ui'), reviewContainerDivs))

def extractReviewObjects(listOfContainersPtags):
    """ takes a list of lists (containerPtags) and returns a list of review objects """

    reviewObjects = []
    for setOfPtags in reviewContainerPtags:
        extractedPtext = list(map(lambda x: x.text, setOfPtags))

        # Handle missing info by simply subbing review info for empty string
        if len(extractedPtext) < 4:
            reviewObject = {
                "review" : "" 
            }
        else:
            # go backwards to ensure we don't get the review summary, only pros & cons if they exist
            reviewObject = {
                "review" : extractedPtext[-3] + extractedPtext[-1] 
            }

        reviewObjects.append(reviewObject)
    return reviewObjects




data = extractReviewObjects(reviewContainerPtags)
# extracts all the text between p-tags while excluding pros & cons labels
for reviewObject in data:
    print("")
    print(reviewObject)
    if len(reviewObject['review']) == 0:
        break
    print("")