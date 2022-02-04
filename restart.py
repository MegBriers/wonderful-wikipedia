# -*- coding: utf-8 -*-
"""
Created on Tue Jan 04 09:05:18 2022

driver code
@author: Meg
"""

import sys
import os
import wikipedia
import spacyExtract
import requests
from bs4 import BeautifulSoup
import scraper
import comparisonCurrent
import random


def choose_people():
    print(":)")
    URL = "https://en.wikipedia.org/wiki/Category:19th-century_British_mathematicians"
    # going to extract 3 random mathematicians from this file and write to a page
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

    values = []
    for i in range(3):
        val = random.choice(list(links.keys()))
        while val in values:
            val = random.choice(list(links.keys()))
        values.append(val)

    print(values)

    fileName = './output/test_people.txt'
    with open(fileName, 'w') as f:
        f.write('Mary Somerville\n')
        f.write('John Tyndall\n')
        for person in values:
            f.write(person)
            f.write('\n')
    f.close()


def formatting(name, char):
    parts = name.split()
    new_name = ""
    for i in range(len(parts)):
        if i == 0:
            new_name = new_name + parts[i].capitalize()
        else:
            new_name = new_name + char + parts[i].capitalize()
    return new_name


def get_test_data():
    # could be made into a method
    test_set = open("./output/test_people.txt", "r")

    content = test_set.read()
    people = content.split("\n")
    test_set.close()

    people.pop()
    people = list(set(people))
    return people


def get_linked_names(person):
    """

    A method that calls the relevant part of the code to access all the linked names

    Parameters
    ----------
    person : string
        the person whose wikipedia article we are looking at

    Returns
    -------
        None.

    """
    print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　getting linked names　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
    scraper.request_page(person)


def get_page_content(person):
    """

    A method that gets the relevant text content of the wikipedia for
    a given person

    Parameters
    ----------
    person : string
        the person whose wikipedia article we are looking at

    Returns
    -------
    substring : string
        the wikipedia page in text form ready for analysis

    """
    print("‧͙⁺˚*･༓☾　getting the page data for unlinked names　☽༓･*˚⁺‧͙")

    # getting the relevant wikipedia page
    page = wikipedia.page(person)

    # getting all the text from the page
    content = page.content

    # removing the irrelevant sections
    split_string = content.split("== See also ==", 1)

    substring = split_string[0]

    return substring


def usage_options():
    print("")
    print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
    print("usage : [type of run] [options : specified NER method]")
    print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
    print("type of run : ")
    print("test = evaluates the methods based off of annotated test data")
    print("network = applies the methods to a larger group with no test data or evaluation option")
    print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
    print("options : ")
    print("spacy = normal spacy methods")
    print("nltk = using NTLK")
    print("spacy_new = retrained spacy model")
    print("wikidata = only extracts the linked people")
    print("all = all three methods compared")
    print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")


def validate_name(name):
    """

    A method that calls the relevant part of the code to access all the linked names

    Parameters
    ----------
    name : string
        the passed in name to the method
        unformatted so must be correctly formatted
        desired format Firstname_Secondname

    Returns
    -------
    os.path.isfile(filePath) : boolean
        representing whether the file for the person passed in is present in folder

    newName : string
        the string of the person passed in in a format that can be manipulated easily for rest of code

    """
    # desired file path ./people/Firstname_Secondname.txt

    newName = formatting(name, "_")

    filePath = './people/' + newName + '.txt'

    return os.path.isfile(filePath), newName


if __name__ == '__main__':
    # assumptions with input - has a space between parts of name

    if len(sys.argv) < 2:
        usage_options()
        exit(0)

    if sys.argv[1] == "test":
        people = get_test_data()

        print("people")
        print(people)

        # if we have enough arguments
        for pep in people:
            print(pep)
            data = get_page_content(pep)
            if sys.argv[2] == 'spacy':
                spacyExtract.extracting_unlinked_spacy(data, pep, sys.argv[2])
            elif sys.argv[2] == 'nltk':
                spacyExtract.ntlk_names(data, pep)
            elif sys.argv[2] == 'spacy_new':
                spacyExtract.extracting_unlinked_spacy(data, pep, sys.argv[2])
            elif sys.argv[2] == 'wikidata':
                scraper.request_linked(pep)
            elif sys.argv[2] == 'all':
                print("buckle up")
                spacyExtract.extracting_unlinked_spacy(data, pep, "spacy")
                spacyExtract.nltk_names(data, pep)
                spacyExtract.extracting_unlinked_spacy(data, pep, "spacy_new")
            else:
                print("method is incorrect, please refer to usage instructions")
                usage_options()
                exit(0)

        print("time to do some stats")
        print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
        print(":)")
        comparisonCurrent.evaluate(sys.argv[2])

    elif sys.argv[1] == "network":
        print("🦆")
    else:
        print("The methods you have indicated are not accepted input")
        print(".・。.・゜✭・.・✫・゜・。.")
        print("Please follow the below usage instructions")
        print(".・。.・゜✭・.・✫・゜・。.")
        usage_options()
