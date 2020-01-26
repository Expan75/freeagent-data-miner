# standard package imports
import re
import csv

# installed Modules
from bs4 import BeautifulSoup
from requests import get
import pandas as pd

BASE_URL = 'https://www.softwareadvice.com/accounting/freeagent-profile/reviews/'
# https://www.softwareadvice.com/accounting/freeagent-profile/reviews/?review.page=1

# If exceding pagination, will direct to last page of results


# NOTE: this does not check for repeat data or redirects to home page
def initDataFlow(paginatedLimit):
    """ Inits Data flow via function calls while keeping track of progress to ensure no data duplication """ 

    # Useful vars for control flow 
    paginatedLimit += 1
    cachedContent = None
    cachedNResults = None

    for n in range(1, paginatedLimit):

        url = BASE_URL + '?review.page=' + str(n)
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

        # Handles redirect
        if len(data) < cachedNResults:
            break

        if n==1:
            # Setups condition to prevent duplication if redirected to first page
            cachedContent = data[0]['content']
            # Setup condition to prevent duplication if redirected to last page
            # NOTE: DOESNT cover edge case were last page has exactly paginated Max
            cachedNResults = len(data[0])
    
    return
        


def getPageRes(url):
    return get(url)


def getSoup(res):
    return BeautifulSoup(res.text, 'html.parser')


def getReviewTagElements(soup):
    """ Takes in a beautifulSoup html doc as arg. and returns lists of reviewSCores, reviewTitles, and reviewContents """
   
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
    pd.DataFrame(objects).to_csv('softwareadvice.csv', mode='a', header=False, index=False, index_label=False)
    print("wrote " + str(len(objects)) + " reviews to file.")



# Inits data mining flow
# scores, titles, contents = getReviewTagElements(res)
# data = assembleReviewObjects(scores,titles,contents)
# saveObjects(data)

initDataFlow(4)