# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 10:22:32 2022

@author: Meg
"""


import requests
from bs4 import BeautifulSoup
from wikidata.client import Client
import nltk

client = Client()
"""
# manually setting up an entity we know is a person to compare the entity types
  # Q268702 - Mary Somerville
entityCompare = client.get('Q268702', load=True)
   # P31 - 'instance of'
dob = client.get('P569', load=True)
dod = client.get('P570', load=True)

print(entityCompare.getlist(dob))

types = (entityCompare.getlist(dob)[0]).year
print(types)

types2 = ((entityCompare.getlist(dod))[0]).year
print(types2)

dob = 2000
dod = 2008
set1 = [1980,1990]
set2 = [1999,2008]
set3 = [2002,2006]
set4 = [2006,2012]
set5 = [2013,2020]
set6 = [1999,2009]

sets = [set1,set2,set3,set4,set5,set6]

for i in range(len(sets)):
    set = sets[i]
    if dob <= set[0] <= dod or (set[0] <= dob and set[1] >= dod):
        print("accepted")
    else:
        print("rejected")


text = "Somerville was the daughter of Vice-Admiral Sir William George Fairfax, scion of a distinguished family of Fairfaxes, and she was related to several prominent Scottish houses through her mother, the admiral's second wife, Margaret Charters, daughter of Samuel Charters, a solicitor."
people = []

print("Sentence tokenised \n")
sentToken = nltk.sent_tokenize(text)
print("")

for sent in nltk.sent_tokenize(text):
    print("Word tokenised \n")
    sent2 = nltk.word_tokenize(sent)
    print("")
    print("Pos Tagging \n")
    posTag = nltk.pos_tag(sent2)
    print("Chunking \n")
    chunks = nltk.ne_chunk(posTag)

    for chunk in chunks:
        if hasattr(chunk, 'label'):
            if chunk.label() == "PERSON":
                text = ' '.join(c[0] for c in chunk)
                people.append(text)

print("Final identified people \n")
print(people)


typesCompare = entityCompare.getlist(instance_of)
for t in typesCompare:
    t.load()

entity = client.get('Q323650', load=True)

instance_of = client.get('P31', load=True)
types = entity.getlist(instance_of)
for p in types:
    p.load()
result = 0

if (len(types) > 0):
    result = (types[0] == typesCompare[0])

print(result)
"""

entityCompare = client.get('Q268702', load=True)
    # P31 - 'instance of'
instance_of = client.get('P31', load=True)
typesCompare = entityCompare.getlist(instance_of)
for t in typesCompare:
    t.load()

dob = client.get('P569', load=True)
dod = client.get('P570', load=True)

date_of_birth = (entityCompare.getlist(dob)[0]).year

date_of_death = (entityCompare.getlist(dod)[0]).year


try:
    entity = client.get('Q169566', load=True)
    # this will throw an error whenever the item loaded is not a person currently (hence the need for try, except blocks)

    instance_of = client.get('P31', load=True)
    types = entity.getlist(instance_of)
    for t in types:
        t.load()
    result = True
    # statistically more contemporaries on wikipedia pages than dead people ??? - design choice
    alive = True

    if result:
        # check dob of the person lies within date_of_birth and date_of_death
        dob_compare = client.get('P569', load=True)
        dod_compare = client.get('P570', load=True)

        dates_ob = entity.getlist(dob_compare)
        dates_od = entity.getlist(dod_compare)

        print("Dates of birth")
        print(dates_ob)
        print("Dates of death")
        print(dates_od)

        if len(dates_ob) > 0 and len(dates_od) > 0:
            caught = [False, False]
            if type(dates_ob[0]) == int:
                date_of_birth_compare = dates_ob[0]
                caught[0] = True
            if type(dates_od[0]) == int:
                date_of_death_compare = dates_od[0]
                caught[1] = True

            if caught[0] == False and caught[1] == False:
                date_of_birth_compare = (entity.getlist(dob)[0]).year
                date_of_death_compare = (entity.getlist(dod)[0]).year
            elif caught[0] == False:
                date_of_birth_compare = (entity.getlist(dob)[0]).year
            elif caught[1] == False:
                date_of_death_compare = (entity.getlist(dod)[0]).year

            # used to check if the person falls within the same time span as the person whose page we are analysing
            # only checked when we know that it is a person (so we definitely have a date)
            if (1853 <= date_of_birth_compare <= 1907) or (
                    date_of_birth_compare <= 1853 and date_of_death_compare >= 1907):
                result = True
            else:
                # doesn't matter that they are a person, because they are not a relevant person (f)
                print("definitely going here")
                result = False

    print(result)

except Exception as inst:
    # IF WE DON'T HAVE A GREGORIAN CALENDAR WE CAN DISREGARD THE PERSON BC THEY ARE NOT IN THE 19TH CENTURY
    print("✨")

print("fell out")