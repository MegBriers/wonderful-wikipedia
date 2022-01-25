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
#doc = nlp("She was among those who discussed a hypothetical planet perturbing Uranus.")
#displacy.serve(doc, style="dep")

text = "Somerville was the daughter of Vice-Admiral Sir William George Fairfax, scion of a distinguished family of Fairfaxes, and she was related to several prominent Scottish houses through her mother, the admiral's second wife, Margaret Charters, daughter of Samuel Charters, a solicitor."

text2 = "When Mary was 13 her mother sent her to writing school in Edinburgh during the winter months, where she improved her writing skills and studied the common rules of arithmetic"

# visualisation of NER 
colors = {"ORG": "linear-gradient(90deg, #aa9cfc, #fc9ce7)"}
doc = nlp(text)
doc2 = nlp(text2)
displacy.serve(doc2, style="ent")

#options = {"ents": ["PERSON"], "colors": colors}
#displacy.serve(doc, style="ent", options=options)
"""

from spacy.lang.en import English

nlp = English()
text = '''"Let's go!"'''
print(nlp.pipeline)
doc = nlp(text)
tok_exp = nlp.tokenizer.explain(text)
assert [t.text for t in doc if not t.is_space] == [t[1] for t in tok_exp]
for t in tok_exp:
    print(t[1], "\t", t[0])
    
"""