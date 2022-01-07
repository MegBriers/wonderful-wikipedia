# -*- coding: utf-8 -*-
"""
Created on Tue Jan 04 09:05:18 2022

driver code
🦆
@author: Meg
"""

import sys
import os
import wikipedia
import spacyExtract
import scraper
import comparisonCurrent

# code needs to

# methods : [option 1] [option 2] [option 3] [comparison option]

# for a specified wikipedia page and method
    # check we have the comparison data for that specified page ✓
        # if not then reject name ✓
        # if we have the comparison data ✓
            # if not comparison
                # get all the names using that specified method
                    # linked ✓
                    # unlinked (spacy ✓, ntlk, new spacy)
                # give a statistical summary of how well it has performed ✓
            # if no second argument given
                # do all three methods
                # provide individual statistical summary of how well each performed ✓
                # do statistics for the comparison of methods ✓

def getLinkedNames(person):
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
    scraper.requestPage(person)


def getPageContent(person):
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


def validateName(name):
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

    parts = name.split()
    newName = ""
    for i in range(len(parts)):
        if i == 0:
            # does this uncapitalize everything else in the string ?
            newName = newName + parts[i].capitalize()
        else:
            newName = newName + "_" + parts[i].capitalize()

    print(newName)

    filePath = './people/' + newName + '.txt'

    return os.path.isfile(filePath), newName


if __name__ == '__main__':
    Dict = {'option1': 'spacy', 'option2': 'ntlk', 'option3': 'retrained'}

    # assumptions with input - has a space between parts of name

    if len(sys.argv) < 2:
        print("")
        print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
        print("usage : [desired mathematician] [options : specified NER method]")
        print("if desired NER method left out then a comparison of all three methods will be performed (warning : longer running time)")
        print("options : ")
        print("option1 = normal spacy methods")
        print("option2 = using method 2")
        print("option3 = retrained spacy model")
        print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
        exit(0)

    res, newName = validateName(sys.argv[1])

    if (res):
        if len(sys.argv) >= 3:
            inp = sys.argv[1]

            spaceNewName = newName.replace("_", " ")

            print(spaceNewName)

            # the wikipedia page
            data = getPageContent(spaceNewName)

            if sys.argv[2] == 'option1':
                print("Getting all the names mentioned in the article using standard spacy....")
                print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
                spacyExtract.extractingUnlinkedSpacy(data, spaceNewName)
            elif sys.argv[2] == 'option2':
                print("Getting all the names mentioned in the article using [insert name here]....")
                print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
                # this isn't an unlinked option
                # ntlk ?? 🦆
                # find another option that extracts names from text that isn't spacy
                print("do a different method")
            elif sys.argv[2] == 'option3':
                # 🦆
                print("Getting all the names mentioned in the article using [retrained spacy]....")
                print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
            else:
                print("Invalid option given, please refer to the accepted options below")
                print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
                print("option1 = normal spacy methods")
                print("option2 = using wikidata")
                print("option3 = retrained spacy model")
        else:
            print("hold on, this is going to take about 10 years")
            print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
            # do all three methods 🦆


        print("Getting all linked names from the wikipedia article....")
        print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
        # must have name in form for wikipedia here
        scraper.request_linked(newName)

        print("phew we got through it")
        # do the comparison here (call from a comparison file?)
        # file for comparison : comparisonCurrent

        # there will not be a sys.argv[2] if all the methods
        # comparisonCurrent.method_evaluation(Dict[sys.argv[2]], newName)

    else:
        print("There does not seem to be manual data to allow comparison, apologies")
        print(".・。.・゜✭・.・✫・゜・。.")
        print("If you believe there is, please ensure the file is correctly formatted as below")
        print(".・。.・゜✭・.・✫・゜・。.")
        print("./data/Firstname_Secondname.txt")