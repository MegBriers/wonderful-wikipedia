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
import restart


def statistics(false_pos, false_neg, true_pos):
    """

    A method that analyses the performance of the wikidata way of extracting
    people that are linked in an article

    Parameters
    ----------
    false_pos : integer
        the number of additional things picked up by method

    false_neg : integer
        the number of manually identified people who were NOT picked up

    true_pos : integer
        the number of manually identified people who were picked up

    Returns
    -------
    None.

    """
    # precision = (true positives)/(true positives + false positives)
    print("precision")
    precision = true_pos / (true_pos + false_pos)
    print(precision)
    print("")

    print("recall")
    # recall = (true positives)/(true positives + false negatives)
    recall = true_pos / (true_pos + false_neg)
    print(recall)
    print("")

    # f1 score = 2 x (precision * recall)/(precision + recll)
    f1 = 2 * ((precision * recall) / (precision + recall))

    print("the f1 score")
    print(f1)
    print("")

    return f1


def setup(name):
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
    new_name = restart.formatting(name, "_")
    manual = pd.read_csv("./people/" + new_name + ".txt")

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
    print("＊*•̩̩͙✩•̩̩͙*˚　with an f1 score of　˚*•̩̩͙✩•̩̩͙*˚＊")
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
    print("%.2f" % (len(linked) / len(complete) * 100))
    print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
    print("proportion of people linked who have been picked up by wikidata")
    # need to get the wikidata people at this point
    fileLinked = open("./output/wikidata/" + person + "_Linked.txt", "r")

    content = fileLinked.read()
    # identified by wikidata
    wikiData = content.split("\n")
    fileLinked.close()

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
            if (human in wiki or wiki in human or Levenshtein.ratio(human, wiki) > .85):
                count += 1
                notIdentified.remove(human)
                if wiki in additional:
                    additional.remove(wiki)
                break

    print("%.2f" % ((count / allLinked) * 100))
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

    true_pos = count  # how many were correctly identified
    false_pos = len(additional)  # how many were identified as human but are not human
    false_neg = len(notIdentified)  # how many of our true ones are missing

    # NOT REPRESENTATIVE BECAUSE WE'RE FILTERING BY HISTORICAL PEOPLE
    statistics(false_pos, false_neg, true_pos)


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

    print("")
    print(method)
    print("")
    filename = "./output/" + method + "/" + person + "_Unlinked"

    # the file that stores the method names
    # breaking here for john tyndall
    fileUnlinked = pd.read_csv(filename + ".txt", quotechar=",")

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
            if Levenshtein.ratio(people, identified) > 0.9:
                # if (people in identified and Levenshtein.ratio(people,identified) > 0.85) or (identified in people and Levenshtein.ratio(people,identified) > 0.85):
                copyComplete.remove(people)
                # method picks up the same person multiple time, so this is okay
                if not (identified in copyIdentified):
                    copyIdentified.append(identified)
                break

    print("Those not identified by method : ")
    print("")
    for cop in copyComplete:
        print(cop)
    print("")
    numberIdentified = len(complete) - len(copyComplete)

    print("Percentage identified from the proper data set (positive matches): ")
    print("%.2f" % ((numberIdentified / len(complete)) * 100))
    print("")
    print("Those identified by method that have not provided a match with the manual data :")
    print("")
    noMatch = list(set(identifiedUnlinked).difference(set(copyIdentified)))
    for no in noMatch:
        print(no)
    print("")

    # false_pos, false_neg, true_pos
    # i believe these are set up correctly
    false_pos = len(noMatch)
    true_pos = numberIdentified
    false_neg = len(copyComplete)

    return statistics(false_pos, false_neg, true_pos)


    # return (numberIdentified / len(complete)) * 100


def evaluation(method, newName):
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
    complete, linked, unlinked = setup(newName)
    if method == "all":
        multiple_evaluation(newName, complete, linked, unlinked)
    else:
        method_evaluation(method, newName, complete, linked, unlinked)
