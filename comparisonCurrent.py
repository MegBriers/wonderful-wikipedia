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

def setup():
    """

    This method sets up all the information used for the rest of the methods, regardless if
    multiple evaluation or single evaluation

    Parameters
    ----------
    None.

    Returns
    -------
    complete : array of strings
        all the manually identified UNIQUE people in the article

    linked : array of strings
        all the manually identified people that are linked in the article

    unlinked : TYPE
        all the manually identified people that are unlinked in the article

    """

    # the file that stores the manual names
    manual = pd.read_csv("./people/Mary_Somerville.txt")

    # all linked in the article
    linked = []
    # all unlinked names in the article
    unlinked = []
    # all names in article
    complete = []

    # set up weirdly for the graph, may modify file structure
    for index, row in manual.iterrows():
        complete.append(row["Target"])
        actualRow = row["link"].replace(' ', '')
        if actualRow == "linked":
            linked.append(row["Target"])
        else:
            unlinked.append(row["Target"])
    complete = list(set(complete))
    return complete, linked, unlinked


def multiple_evaluation(person, complete, linked, unlinked):
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

    # dummy values, will be replaced
    max_accuracy = 0
    max_method = "🐸"

    wikidata_evaluation(person, complete, linked, unlinked)

    for item in ["spacy", "ntlk", "spacy_new"]:
        acc = method_evaluation(item, person, complete, linked, unlinked)
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


def wikidata_evaluation(person, complete, linked, unlinked):
    # THIS IS NOT PICKING UP EVERYONE WHO SHOULD BE GETTING PICKED UP
    """

    A method that analyses the performance of the wikidata way of extracting
    people that are linked in an article

    Parameters
    ----------
    person : string
        the person whose wikipedia article is being analysed

    Returns
    -------
    None.

    """
    print("")
    print("")
    print("＊*•̩̩͙✩•̩̩͙*˚　LINKED (WIKIDATA) PERFORMANCE　˚*•̩̩͙✩•̩̩͙*˚＊")
    print("")
    print("")
    print("proportion of people who are linked in the article")
    print("%.2f" % (len(linked)/len(complete) * 100))
    print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
    print("proportion of people linked who have been picked up by wikidata")
    # need to get the wikidata people at this point
    fileLinked = open("./output/wikidata/" + person + "_Linked.txt", "r", encoding="utf-8")

    content = fileLinked.read()
    # identified by wikidata
    wikiData = content.split("\n")
    fileLinked.close()

    # manually removing last line (cheap fix - can do better) 🦆 TO DO : FIX THIS
    # also Ada Lovelace is popping up twice so just making it a set but needs to be fixed at the root
    wikiData.pop()
    wikiData = list(set(wikiData))

    allLinked = len(linked)
    count = 0

    notIdentified = linked[:]

    additional = wikiData[:]

    for human in linked:
        for wiki in wikiData:
            # TO DO - remove everything after a comma in a string !!
            # this is a fair enough analysis, not picking up any false positives but unsure how many true positives are being missed
            if (human in wiki or wiki in human or Levenshtein.ratio(human,wiki) > .85):
                count +=1
                notIdentified.remove(human)
                if wiki in additional:
                    additional.remove(wiki)
                break

    print("%.2f" % ((count/allLinked)*100))
    print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")

    # filtered people out now
    # this is no longer representative of whether it is performing well
    # only want people in the time frame to be compared
    print("those who were not identified: ")
    print("")
    for no in notIdentified:
        print(no)
    print("")
    print("")

    print("those who were picked up additionally by wikidata")
    print("")
    for add in additional:
        print(add)
    print("")
    print("")

    # PICKING UP PEOPLE WHO HAVE STUB ARTICLES THAT ARE NOT FILLED IN
    # these people have been identified it's just they go under different names/french symbols OR they have stub articles
    # couple due to different way to refer, others idk, may have to check what's happening with scraper for those specifics

def method_evaluation(method, person, complete, linked, unlinked):
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

    filename = "./output/" + method + "/" + person + "_Unlinked"

    # the file that stores the method names
    # breaking here for john tyndall
    print(method)
    fileUnlinked = pd.read_csv(filename + ".txt")

    # identified by method
    identifiedUnlinked = []

    # selected method
    for index, row in fileUnlinked.iterrows():
        identifiedUnlinked.append(row["Target"])

    identifiedUnlinked = list(set(identifiedUnlinked))

    strippedUnlinked = []
    for ele in identifiedUnlinked:
        if ele.strip():
            strippedUnlinked.append(ele)

    print("")
    print("")
    print("＊*•̩̩͙✩•̩̩͙*˚　" + method + " PERFORMANCE　˚*•̩̩͙✩•̩̩͙*˚＊")
    print("")
    print("")

    # remove all the typical titles - is leaving a space at the start
    typicalTitles = ["Dr", "Miss", "Mrs", "Sir", "Mr", "Lord"]

    for title in typicalTitles:
        complete = [name.replace(title, '') for name in complete]
        identifiedUnlinked = [name.replace(title, '') for name in identifiedUnlinked]

    copyComplete = complete[:]

    copyIdentified = []

    for people in complete:
        for identified in identifiedUnlinked:
            # this might be letting in some false positives
            if Levenshtein.ratio(people,identified) > 0.9:
            #if (people in identified and Levenshtein.ratio(people,identified) > 0.85) or (identified in people and Levenshtein.ratio(people,identified) > 0.85):
                copyComplete.remove(people)
                # method picks up the same person multiple time, so this is okay
                if not(identified in copyIdentified):
                    copyIdentified.append(identified)
                break

    print("Those not identified by method : ")
    print("")
    for cop in copyComplete:
        print(cop)
    print("")
    numberIdentified = len(complete) - len(copyComplete)

    print("Percentage identified from the proper data set (positive matches): ")
    print("%.2f" % ((numberIdentified/len(complete))*100))
    print("")
    print("Those identified by method that have not provided a match with the manual data :")
    print("")
    noMatch = list(set(identifiedUnlinked).difference(set(copyIdentified)))
    for no in noMatch:
        print(no)
    print("")

    # do proper stats for the methods - 🦆 (week 2)
    """Correct (COR) : both are the same;
        Incorrect (INC) : the output of a system and the golden annotation don’t match;
        Partial (PAR) : system and the golden annotation are somewhat “similar” but not the same;
        Missing (MIS) : a golden annotation is not captured by a system;
        Spurius (SPU) : system produces a response which doesn’t exist in the golden annotation;"""


    return (numberIdentified / len(complete)) * 100


def evaluation(method,newName):
    """

    Driver method for this code to deal with the problem of the three arrays
    (complete, linked, unlinked) needed for both methods but don't want to read file in
    multiple times

    Parameters
    ----------
    method : string
        the method we want to evaluate

    newName : string
        the person whose article we are evaluating in the correct form for file retrieval

    Returns
    -------
    None.

    """
    complete, linked, unlinked = setup()
    if method == "all":
        multiple_evaluation(newName, complete, linked, unlinked)
    else:
        method_evaluation(method, newName, complete, linked, unlinked)