# standard package imports
import re
import csv

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
        scores, titles, contents = getReviewTagElements(soup)
        data = assembleReviewObjects(scores,titles,contents)

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


def getReviewTagElements(soup):
    """ Takes in a beautiful html doc as arg. and returns lists of reviewSCores, reviewTitles, and reviewContents """
   
    # Should not include first result as this is merely the page summary
    reviewScores = soup.find_all(alt=re.compile(r'stars'))
    
    # returns all the objects containing the review titles
    reviewTitles = soup.find_all('a', class_='link link--large link--dark')
    
    # returns all the objects containing the review contents
    reviewContents = soup.find_all('p', class_='review-content__text')

    return reviewScores, reviewTitles, reviewContents


def assembleReviewObjects(scores, titles, contents):
    """ 
        Takes in arrays with scores, titles, and contents and returns 
        a list of data objects with the structure:
            {
                'score': string,
                'title': string,
                'content': string
            }
    """
    data = []
    for index, score in enumerate(scores[1:], 0):
        data.append({
            'score': score['alt'][0],
            'title': titles[index].text.strip(),
            'content': contents[index].text.strip()
        })
        
    return data


def saveObjects(objects):
    """ Takes in a list of review objects """
    pd.DataFrame(objects).to_csv('reviews.csv', mode='a', header=False, index=False, index_label=False)
    print("wrote " + str(len(objects)) + " reviews to file.")



# Inits data mining flow
# scores, titles, contents = getReviewTagElements(res)
# data = assembleReviewObjects(scores,titles,contents)
# saveObjects(data)

initDataFlow(100)