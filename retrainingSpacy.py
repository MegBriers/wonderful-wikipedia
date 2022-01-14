# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 09:08:08 2022

GENERATING THE TEST DATA (for philosophers and mathematicians)
AND RETRAINING THE SPACY
(currently the data has some interesting maths embedded)

@author: Meg
"""

import requests
from bs4 import BeautifulSoup
import os
# used to get the content of wikipedia pages
import restart

def writeContentsToFile(mathematicians, subject):
    print("✰⋆🌟✪🔯✨")
    fileName = './data/training_data_' + subject + '.txt'
    with open(fileName, 'w',encoding="utf-8") as f:
        for mathematician in mathematicians:
            print(mathematician)
            try:
                content = restart.getPageContent(mathematician)
                f.write(mathematician)
                f.write('\n')
                f.write(content)
            except Exception as e:
                # does trip up on a few pages
                print(e)

def getListData(URL):
    response = requests.get(
        url=URL,
    )

    assert response.status_code == 200, "request did not succeed"

    soup = BeautifulSoup(response.content, 'lxml')

    links = {}
    for link in soup.find(id="bodyContent").find_all("a"):
        url = link.get("href", "")
        # looking for relevant links only
        if url.startswith("/wiki/") and "/wiki/Category" not in url and "Categor" not in url:
            print(url)
            links[link.text.strip()] = url

    return links


if __name__ == '__main__':
    # if the files are not present in the folder
    filePath1 = './data/training_data_maths.txt'
    filePath2 = './data/training_data_philosophy.txt'
    if not(os.path.isfile(filePath1)) or not(os.path.isfile(filePath2)):
        webpages = ["https://en.wikipedia.org/wiki/Category:19th-century_British_mathematicians", "https://en.wikipedia.org/wiki/Category:19th-century_British_philosophers"]
        subjects = ["maths","philosophy"]
        for i in range(2):
            webpage = webpages[i]
            links = getListData(webpage)
            writeContentsToFile(links, subjects[i])
    else:
        print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　retraining spacy, this might take a while   ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
        # insert all the stuff to retrain spacy