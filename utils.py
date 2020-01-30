"""

Contains util functions that are common for all mining scripts

"""

# general library imports
import pandas as pd

# specific imports
from bs4 import BeautifulSoup
from requests import get


def getPageRes(url):
    """ takes in a string URL a returns a requests response object """
    return get(url)
    

def getSoup(res, usingDriver=False):
    """ takes in a requests res object OR a webdriver object and returns a beautiful soup HTML object """
    if usingDriver == True:
        return BeautifulSoup(res, 'html.parser')
    else:
        return BeautifulSoup(res.text, 'html.parser')


def saveObjects(objects, path):
    """ Takes in a list of objects and writes them to a csv at the specified path, returns n objects saved """
    pd.DataFrame(objects).to_csv(path, mode='a', header=False, index=False, index_label=False)
    print("wrote " + str(len(objects)) + " reviews to file.")

    return len(objects)