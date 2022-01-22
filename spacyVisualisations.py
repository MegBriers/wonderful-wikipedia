# -*- coding: utf-8 -*-
"""

Small file that can be used to produce visualisations fortthe report

Created on Sat Jan 22 07:39:49 2022

@author: Meg
"""

import spacy
from spacy import displacy

# visualisation of dependency parser 
nlp = spacy.load("en_core_web_sm")
doc = nlp("She was among those who discussed a hypothetical planet perturbing Uranus.")
#displacy.serve(doc, style="dep")

text = "Somerville was the daughter of Vice-Admiral Sir William George Fairfax, scion of a distinguished family of Fairfaxes, and she was related to several prominent Scottish houses through her mother, the admiral's second wife, Margaret Charters, daughter of Samuel Charters, a solicitor."

# visualisation of NER 
colors = {"ORG": "linear-gradient(90deg, #aa9cfc, #fc9ce7)"}
doc = nlp(text)
options = {"ents": ["PERSON"], "colors": colors}
displacy.serve(doc, style="ent", options=options)
