# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 14:42:19 2021

@author: Meg
"""
# https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# trying to find how many names are mentioned in Bertrand Russell's wikipedia

ex = "European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices"

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

sent = preprocess(ex)
print(sent)

from bs4 import BeautifulSoup
import requests
import re

import nerExtract
from nerExtract import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

def url_to_string(url):
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html5lib')
    for script in soup(["script", "style", 'aside']):
        script.extract()
    return " ".join(re.split(r'[\n\t]+', soup.get_text()))
ny_bb = url_to_string('https://www.nytimes.com/2018/08/13/us/politics/peter-strzok-fired-fbi.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=first-column-region&region=top-news&WT.nav=top-news')
article = nlp(ny_bb)
print(len(article.ents))
