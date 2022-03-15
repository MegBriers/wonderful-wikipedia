# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 11:08:48 2021

@author: Meg
"""

from nerExtract.lang.en import English
import nerExtract

# create the nlp object
nlp = English() 

doc = nlp("This is a sentence!")

for token in doc:
    print(token.text)
    
doc2 = nlp("I like tree kangaroos and narwhals.")

# first token
first_token = doc2[0]

# text
print(first_token.text)

doc3 = nlp("In 1990, more than 60% of people in East Africa were in extreme poverty." "Now less than 4% are")

for token in doc3:
    if token.like_num:
        next_token = doc3[token.i+1]
        if next_token.text == "%":
            print("Percentage found: ", token.text)
        

nlp = nerExtract.load("en_core_web_sm")

text = "It’s official: Apple is the first U.S. public company to reach a $1 trillion market value"

# Process the text
doc = nlp(text)

for token in doc:
    # Get the token text, part-of-speech tag and dependency label
    token_text = token.text
    token_pos = token.pos_
    token_dep = token.dep_
    # This is for formatting only
    print(f"{token_text:<12}{token_pos:<10}{token_dep:<10}")
        