# -*- coding: utf-8 -*-
"""
Created on Tue Jan 04 15:45:07 2022

code that should assess how well the methods have
performed against the manual test data

@author: Meg
"""
import pandas as pd
import Levenshtein

import sys

# the file that stores the manual names
manual = pd.read_csv("./people/Mary_Somerville.txt")

# all linked in the article
linked = []
# all unlinked names in the article
unlinked = []
# all names in article
complete = []

# manual
for index, row in manual.iterrows():
    complete.append(row["Target"])
    actualRow = row["link"].replace(' ', '')
    if actualRow == "linked":
        linked.append(row["Target"])
    else:
        unlinked.append(row["Target"])


def multiple_evaluation(person):
    """

    A method to call the analysis on multiple methods if all three methods want
    to be compared

    Parameters
    ----------
    person : string
        the person whose wikipedia article we are looking at

    Returns
    -------
    None.

    """
    stdoutOrigin = sys.stdout
    sys.stdout = open("./output/log.txt", "w", encoding="utf-8")

    print("＊*•̩̩͙✩•̩̩͙*˚　MULTIPLE ANALYSIS BEGIN　˚*•̩̩͙✩•̩̩͙*˚＊")
    print("")


    max_accuracy = 0
    max_method = "🐸"

    wikidata_evaluation(person)


    for item in ["spacy", "ntlk", "spacy_new"]:
        acc = method_evaluation(item, person)
        if acc > max_accuracy:
            max_accuracy = acc
            max_method = item

    print("")
    print("＊*•̩̩͙✩•̩̩͙*˚ THE BEST METHOD WAS　˚*•̩̩͙✩•̩̩͙*˚＊")
    print("＊*•̩̩͙✩•̩̩͙*˚ " + max_method + "　˚*•̩̩͙✩•̩̩͙*˚＊")
    print("＊*•̩̩͙✩•̩̩͙*˚　with an accuracy of　˚*•̩̩͙✩•̩̩͙*˚＊")
    print("＊*•̩̩͙✩•̩̩͙*˚ " + str(max_accuracy) + " ˚*•̩̩͙✩•̩̩͙*˚＊")
    sys.stdout.close()
    sys.stdout = stdoutOrigin


def wikidata_evaluation(person):
    print("＊*•̩̩͙✩•̩̩͙*˚　LINKED (WIKIDATA) PERFORMANCE　˚*•̩̩͙✩•̩̩͙*˚＊")
    # print how many of the people metioned on the article are linked
    print("proportion of people who are linked in the article")
    print(len(linked)/len(complete) * 100)
    print(len(linked))
    print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
    print("proportion of people linked who have been picked up by wikidata")
    # need to get the wikidata people at this point
    fileLinked = open("./output/wikidata/" + person + "_Linked.txt", "r")

    content = fileLinked.read()
    # identified by wikidata
    wikiData = content.split("\n")
    fileLinked.close()

    # manually removing last line (cheap fix - can do better)
    # also Ada Lovelace is popping up twice so just making it a set but needs to be fixed at the root
    wikiData.pop()
    wikiData = list(set(wikiData))

    allLinked = len(linked)
    count = 0

    notIdentified = linked[:]

    # THIS LOOPS THROUGH EVERY SECOND HUMAN IN LINKED WTF
    for human in linked:
        for wiki in wikiData:
            if human in wiki or wiki in human or Levenshtein.ratio(human,wiki) > .85:
                notIdentified.remove(human)
                count +=1
                break

    print((count/allLinked)*100)
    print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
    print("those who were not identified:")
    print(notIdentified)
    print("")
    print("")
    # PICKING UP PEOPLE WHO HAVE STUB ARTICLES THAT ARE NOT FILLED IN
    # these people have been identified it's just they go under different names/french symbols OR they have stub articles
    # couple due to different way to refer, others idk, may have to check what's happening with scraper for those specifics

def method_evaluation(method, person):
    """

    A method to give statistics on how accurate the
    method passed in is performing on the wikipedia page

    Parameters
    ----------
    method : string
        how the list of names has been generated
    person : string
        the person whose wikipedia article we are looking at

    Returns
    -------
    float
        the proportion of unlinked people identified

    """
    # ASSUME THAT THE PERSON HAS BEEN PASSED THROUGH IN DESIRED FORM

    if method == "all":
        multiple_evaluation(person)
    else:
        filename = "./output/" + method + "/" + person + "_Unlinked"

        # the file that stores the method names
        fileUnlinked = pd.read_csv(filename + ".txt")

        fileLinked = open("./output/wikidata/" + person + "_Linked.txt", "r")

        content = fileLinked.read()
        # identified by wikidata
        identifiedLinked = content.split("\n")
        fileLinked.close()

        # identified by method
        identifiedUnlinked = []

        # selected method
        for index, row in fileUnlinked.iterrows():
            identifiedUnlinked.append(row["Target"])

        identifiedUnlinked = list(set(identifiedUnlinked))

        # breaking at this line, but how is it getting past that first LINE
        identifiedLinked = list(set(identifiedLinked))

        strippedLinked = []
        for ele in identifiedLinked:
            if ele.strip():
                strippedLinked.append(ele)

        strippedUnlinked = []
        for ele in identifiedUnlinked:
            if ele.strip():
                strippedUnlinked.append(ele)

        # this'll be identifying Thomas Somerville and Thomas Somerville (minister) as two separate entities
        # how to filter this so that they are the same
        completeIdentified = list(set(strippedLinked).union(strippedUnlinked))
        print("＊*•̩̩͙✩•̩̩͙*˚　" + method + " PERFORMANCE　˚*•̩̩͙✩•̩̩͙*˚＊")
        print("")

        copyComplete = complete[:]
        # stores all the people who have NOT been identified as having a match
        copyFound = completeIdentified[:]
        # stores the people who have tried to be matched with two instances (shouldn't happen)
        identifiedTwice = []


        # ANOTHER WAY TO DO THIS WOULD BE TO CHECK FOR ALL THE COMPLETE WHETHER THEY WERE LINKED OR UNLINKED AND THEN
        # CHECK THE RIGHT LIST OF PEOPLE TO SEE IF THEY WERE IDENTIFIED <- JUST A POSSIBILITY

        # checking how many people were identified from the list of people who should have been recognised
        for people in complete:
            for identified in completeIdentified:
                # this might be letting in some false positives
                if people in identified or identified in people or Levenshtein.ratio(people,identified) > 0.85:
                    # 🦆 need a way of being able to stop people getting identified multiple times
                    # filter the actual proper matches
                    # previous method was not working
                    copyComplete.remove(people)
                    #copyFound.remove(identified)
                    break

        print("those not identified by method")
        # there should be no griegs in here for a start
        print(copyComplete)

        print("")
        print("those who the program tried to match with more than once instance in the text")
        print(identifiedTwice)

        numberIdentified = len(complete) - len(copyComplete)

        print("Percentage identified from the proper data set (positive matches): ")
        print("%.2f" % ((numberIdentified/len(complete))*100))
        print("")
        print("")

        """
        # checking how many additional people were picked up
        # GOING TO BE HIGH UNTIL I HAVE FILTERED DOWN BY AGE !!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print("People falsely identified from the method (false positives):")
        print(copyFound)
        print("")

        print("Percentage of false positives")
        print("%.2f" % ((len(copyFound)/len(completeIdentified))*100))
        """

        # do proper stats for the methods - 🦆 (week 2)
        """Correct (COR) : both are the same;
        Incorrect (INC) : the output of a system and the golden annotation don’t match;
        Partial (PAR) : system and the golden annotation are somewhat “similar” but not the same;
        Missing (MIS) : a golden annotation is not captured by a system;
        Spurius (SPU) : system produces a response which doesn’t exist in the golden annotation;"""


        return (numberIdentified / len(complete)) * 100


