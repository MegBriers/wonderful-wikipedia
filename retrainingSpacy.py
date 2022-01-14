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

#   NAMED ENTITY RECOGNITION SERIES   #
#             Lesson 04.02            #
#        Leveraging spaCy's NER       #
#               with                  #
#        Dr. W.J.B. Mattingly         #
import spacy
import json
import random

def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)

def save_data(file, data):
    with open (file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def test_model(model, text):
    doc = nlp(text)
    results = []
    entities = []
    for ent in doc.ents:
        entities.append((ent.start_char, ent.end_char, ent.label_))
    if len(entities) > 0:
        results = [text, {"entities": entities}]
        return (results)

def train_model():
    #TRAIN_DATA = [(text, {"entities": [(start, end, label)]})]

    nlp = spacy.load("math_ner")
    TRAIN_DATA = []
    with open ("data/training_data_maths.txt", "r")as f:
        text = f.read()

        # need to have a split word
        chapters = text.split("CHAPTER")[1:]
        for chapter in chapters:
            chapter_num, chapter_title = chapter.split("\n\n")[0:2]
            chapter_num = chapter_num.strip()
            segments = chapter.split("\n\n")[2:]
            hits = []
            for segment in segments:
                segment = segment.strip()
                segment = segment.replace("\n", " ")
                results = test_model(nlp, segment)
                if results != None:
                    TRAIN_DATA.append(results)

    print(len(TRAIN_DATA))
    save_data("data/training_data_m.json", TRAIN_DATA)

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