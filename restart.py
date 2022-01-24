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
import scraper
import comparisonCurrent


def formatting(name, char):
    parts = name.split()
    new_name = ""
    for i in range(len(parts)):
        if i == 0:
            new_name = new_name + parts[i].capitalize()
        else:
            new_name = new_name + char + parts[i].capitalize()
    return new_name


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

    # contains all the relevant text for a wikipedia article
    return substring


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
    Dict = {'option1': 'spacy', 'option2': 'ntlk', 'option3': 'retrained'}

    # assumptions with input - has a space between parts of name

    if len(sys.argv) < 2:
        print("")
        print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
        print("usage : [desired mathematician] [options : specified NER method]")
        print(
            "if desired NER method left out then a comparison of all three methods will be performed (warning : longer running time)")
        print("options : ")
        print("option1 = normal spacy methods")
        print("option2 = using NTLK")
        print("option3 = retrained spacy model")
        print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
        exit(0)

    res, newName = validate_name(sys.argv[1])

    if (res):
        spaceNewName = newName.replace("_", " ")

        # the wikipedia page

        data = get_page_content(spaceNewName)

        """
        if len(sys.argv) >= 3:

            if sys.argv[2] == 'option1':
                print("Getting all the names mentioned in the article using standard spacy....")
                print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
                spacyExtract.extracting_unlinked_spacy(data, spaceNewName, "spacy")
            elif sys.argv[2] == 'option2':
                print("Getting all the names mentioned in the article using NTLK....")
                print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
                spacyExtract.ntlk_names(data, spaceNewName)
            elif sys.argv[2] == 'option3':
                print("Getting all the names mentioned in the article using [retrained spacy]....")
                print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
                spacyExtract.extracting_unlinked_spacy(data, spaceNewName, "spacy_new")
            else:
                print("Invalid option given, please refer to the accepted options below")
                print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
                print("option1 = normal spacy methods")
                print("option2 = using wikidata")
                print("option3 = retrained spacy model")
        else:
            print("hold on, this is going to take about 10 years")
            print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")

            print("Performing all methods of named entity recognition....")
            print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
            print(".・。.・゜✭spacy・.・✫・゜・。.")
            spacyExtract.extracting_unlinked_spacy(data, spaceNewName, "spacy")
            print(".・。.・゜✭ntlk・.・✫・゜・。.")
            spacyExtract.ntlk_names(data, spaceNewName)
            print(".・。.・゜✭retrained spacy・.・✫・゜・。.")
            spacyExtract.extracting_unlinked_spacy(data, spaceNewName, "spacy_new")

        
        """
        print("Getting all linked names from the wikipedia article....")
        print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
        # must have name in form for wikipedia here
        scraper.request_linked(newName)

        print("time to do some stats")
        print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")

        if len(sys.argv) >= 3:
            comparisonCurrent.evaluation(Dict[sys.argv[2]], newName)
        else:
            comparisonCurrent.evaluation("all", newName)

    else:
        print("There does not seem to be manual data to allow comparison, apologies")
        print(".・。.・゜✭・.・✫・゜・。.")
        print("If you believe there is, please ensure the file is correctly formatted as below")
        print(".・。.・゜✭・.・✫・゜・。.")
        print("./data/Firstname_Secondname.txt")
