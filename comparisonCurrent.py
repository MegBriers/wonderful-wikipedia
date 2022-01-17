# -*- coding: utf-8 -*-
"""
Created on Tue Jan 04 15:45:07 2022

code that should assess how well the methods have
performed against the manual test data

@author: Meg
"""
import pandas as pd


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
    print("＊*•̩̩͙✩•̩̩͙*˚　MULTIPLE ANALYSIS BEGIN　˚*•̩̩͙✩•̩̩͙*˚＊")
    max_accuracy = 0
    max_method = "🐸"
    for item in ["spacy", "ntlk", "spacy_new"]:
        acc = method_evaluation(item, person)
        if acc > max_accuracy:
            max_accuracy = acc
            max_method = item

    print("＊*•̩̩͙✩•̩̩͙*˚ THE BEST METHOD WAS　˚*•̩̩͙✩•̩̩͙*˚＊")
    print("＊*•̩̩͙✩•̩̩͙*˚ " + max_method + "　˚*•̩̩͙✩•̩̩͙*˚＊")
    print("＊*•̩̩͙✩•̩̩͙*˚　with an accuracy of　˚*•̩̩͙✩•̩̩͙*˚＊")
    print("＊*•̩̩͙✩•̩̩͙*˚ " + str(max_accuracy) + " ˚*•̩̩͙✩•̩̩͙*˚＊")


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

        # just line after line of the words
        # the file that stores linked names

        # needs renaming
        # doesn't work if there are multiple commas for the one person

        # read txt and just have a check for whether name IN the longer version of name
        # THIS GIVES SUCH A WEIRD DATA ITEM
        fileLinked = pd.read_csv("./output/wikidata/" + person + "_Linked.txt", sep="\n")

        fileLinked = open("./output/wikidata/" + person + "_Linked.txt", "r")
        content = fileLinked.read()
        # identified by wikidata
        identifiedLinked = content.split("\n")
        fileLinked.close()

        # the file that stores the manual names
        manual = pd.read_csv("./people/Mary_Somerville.txt")

        # all linked in the article
        linked = []
        # all unlinked names in the article
        unlinked = []
        # all names in article
        complete = []

        # identified by method
        identifiedUnlinked = []

        # manual
        for index, row in manual.iterrows():
            complete.append(row["Target"])
            actualRow = row["link"].replace(' ', '')
            if actualRow == "linked":
                linked.append(row["Target"])
            else:
                unlinked.append(row["Target"])

        # selected method
        for index, row in fileUnlinked.iterrows():
            identifiedUnlinked.append(row["Target"])

        # make them all sets, as we don't need duplicates
        linked = list(set(linked))

        unlinked = list(set(unlinked))

        identifiedUnlinked = list(set(identifiedUnlinked))

        print(":)")
        print(identifiedUnlinked)
        print("")
        print(identifiedLinked)

        # breaking at this line, but how is it getting past that first LINE
        identifiedLinked = list(set(identifiedLinked))

        completeIdentified = list(set(identifiedUnlinked).intersection(identifiedLinked))

        print("")
        print("·͙*̩̩͙˚̩̥̩̥*̩̩̥͙　✩　*̩̩̥͙˚̩̥̩̥*̩̩͙‧͙ 　　.·͙*̩̩͙˚̩̥̩̥*̩̩̥͙　✩　*̩̩̥͙˚̩̥̩̥*̩̩͙‧͙ .")
        print("Welcome to the statistical overview")
        print("·͙*̩̩͙˚̩̥̩̥*̩̩̥͙　✩　*̩̩̥͙˚̩̥̩̥*̩̩͙‧͙ 　　.·͙*̩̩͙˚̩̥̩̥*̩̩̥͙　✩　*̩̩̥͙˚̩̥̩̥*̩̩͙‧͙ .")

        print("＊*•̩̩͙✩•̩̩͙*˚　OVERALL PERFORMANCE　˚*•̩̩͙✩•̩̩͙*˚＊")
        print("Overall proportion of people picked up")
        print("%.2f" % ((len(completeIdentified) / len(complete)) * 100))

        print("")
        print("＊*•̩̩͙✩•̩̩͙*˚　UNLINKED (WIKIDATA) PERFORMANCE　˚*•̩̩͙✩•̩̩͙*˚＊")
        print("Proportion of unlinked people picked up")
        commonUnlinked = list(set(identifiedUnlinked).intersection(unlinked))
        print("%.2f" % ((len(commonUnlinked) / len(unlinked)) * 100))
        print("")

        print("＊*•̩̩͙✩•̩̩͙*˚　GIVEN METHOD PERFORMANCE　˚*•̩̩͙✩•̩̩͙*˚＊")
        print("＊*•̩̩͙✩•̩̩͙*˚　chosen method : " + method + "　˚*•̩̩͙✩•̩̩͙*˚＊")
        print("Proportion of linked people picked up")
        commonLinked = list(set(identifiedLinked).intersection(linked))
        print("%.2f" % ((len(commonLinked) / len(linked)) * 100))

        return (len(commonUnlinked) / len(unlinked)) * 100
