# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 21:29:36 2021

@author: Meg
"""


import wikipediaapi

wiki_wiki = wikipediaapi.Wikipedia('en')

page = wiki_wiki.page('Chinthamani Ragoonatha Chary')

print("wikipedia api")
print(page.summary)

print("")

from nerExtract.lang.en import English
import nerExtract

# Process the text
nlp = nerExtract.load("en_core_web_sm")

doc = nlp(page.text)

persons = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']

print(persons)

'''
for token in doc:
    # Get the token text, part-of-speech tag and dependency label
    token_text = token.text
    token_pos = token.pos_
    token_dep = token.dep_
    
    if(token_pos == 'PROPN'):
    # This is for formatting only
        print(f"{token_text:<12}{token_pos:<10}{token_dep:<10}")
        
''' 