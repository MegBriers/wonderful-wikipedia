"""

driver code

"""

import sys
import os
import re
import wikipedia
import spacyExtract
import scraper

import urlopen
from bs4 import BeautifulSoup

# code needs to

# methods : [option 1] [option 2] [option 3] [comparison option]

# for a specified wikipedia page and method
    # check we have the comparison data for that specified page ✓
        # if not then reject name ✓
        # if we have the comparison data ✓
            # if not comparison
                # get all the names using that specified method
                    # linked
                    # unlinked
                # give a statistical summary of how well it has performed
            # if no second argument given
                # do all three methods
                # provide individual statistical summary of how well each performed
                # do statistics for the comparison of methods

def getLinkedNames(page):
    print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")

    # can't do this line
    html = urlopen("https://en.wikipedia.org/wiki/Mary_Somerville")
    bsObj = BeautifulSoup(html)
    for link in bsObj.findAll("a"):
        if 'href' in link.attrs:
            print(link.attrs['href'])

def getUnlinkedNames(person):
    # title = person

    # need to get input into this form
    title = "Mary Somerville"

    # getting the relevant wikipedia page
    page = wikipedia.page(title)

    # getting all the text from the page
    content = page.content

    # removing the irrelevant sections
    split_string = content.split("== See also ==", 1)

    substring = split_string[0]

    # contains all the relevant text for a wikipedia article
    return substring


def validateName(name):
    print("hello")
    # reformat the names
    pattern = re.compile(r'\s+')
    name = re.sub(pattern, '', name.lower())
    filePath = './people/' + name + '.txt'
    return os.path.isfile(filePath)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("")
        print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
        print("usage : [desired mathematician] [options : specified NER method]")
        print("if desired NER method left out then a comparison of all three methods will be performed (warning : longer running time)")
        print("options : ")
        print("option1 = normal spacy methods")
        print("option2 = using wikidata")
        print("option3 = retrained spacy model")
        print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
        exit(0)

    if (validateName(sys.argv[1])):
        print("yay")
        if len(sys.argv) > 3:
            # perform the specific method

            if sys.argv[2].equals('option1'):
                spacyExtract.extractingUnlinkedSpacy()
                # from this point it is written in file
            elif sys.argv[2].equals('option2'):
                # this isn't an unlinked option
                # ntlk ??
                # find another option that extracts names from text that isn't spacy
                print("do wikidata methods")
            elif sys.argv[2].equals('option3'):
                print("do retrained spacy model")
            else:
                print("invalid option given, please refer to the accepted options below")
                print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
                print("option1 = normal spacy methods")
                print("option2 = using wikidata")
                print("option3 = retrained spacy model")
        else:
            # do all three methods
            print("hold on, this is going to take about 10 years")
            getLinkedNames("Dummy variable")

        # after the getlinked names
        # called get linked names here
        # do the comparison here (call from a comparison file?)
        # file for comparison : comparisonCurrent

    else:
        print("error message")