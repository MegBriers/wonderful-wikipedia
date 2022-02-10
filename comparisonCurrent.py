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
import helper


def setup(name):
    """

    This method sets up all the information used for the rest of the methods, regardless if
    multiple evaluation or single evaluation

    Parameters
    ----------
    name : string
        the name of the person whose article we are evaluating

    Returns
    -------
    complete : array of strings
        all the manually identified UNIQUE people in the article

    linked : array of strings
        all the manually identified people that are linked in the article

    unlinked : array of strings
        all the manually identified people that are unlinked in the article

    relevant_linked : array of strings
        all the manually identified people that are ALIVE during lifespan of article's subject

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

    # all linked and alive people in the article
    relevant_linked = []

    # set up weirdly for the graph, may modify file structure
    for index, row in manual.iterrows():
        dob = row["alive"]
        complete.append(row["Target"])
        actualRow = row["link"].replace(' ', '')
        if actualRow == "linked":
            linked.append(row["Target"])
            if dob:
                relevant_linked.append(row["Target"])
        else:
            unlinked.append(row["Target"])

    complete = list(set(complete))
    relevant_linked = list(set(relevant_linked))
    return complete, linked, unlinked, relevant_linked


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
    f1 : float
        the f1 value based on the precision and recall from data
        (representation of how well the method is picking up the people)

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

    return f1


def wikidata_evaluation(person, rel_linked, linked):
    """

    A method that analyses the performance of the wikidata way of extracting
    people that are linked in an article

    Parameters
    ----------
    person : string
        the person whose wikipedia article is being analysed

    rel_linked : list of strings
        the people that were linked in the article (and alive at the right point)

    linked : list of strings
        the people that were linked in the article (regardless of status of life at relevant time)

    Returns
    -------
    f1 : float
        the f1 value based on the precision and recall from data
        (representation of how well the method is picking up the people)

    """
    stdoutOrigin = sys.stdout
    person = helper.formatting(person,"_")
    sys.stdout = open("./output/wikidata/evaluation/" + person + ".txt", "w", encoding="utf-8")

    print("")
    print("")
    print("＊*•̩̩͙✩•̩̩͙*˚　LINKED (WIKIDATA) PERFORMANCE　˚*•̩̩͙✩•̩̩͙*˚＊")
    print("")
    print("")

    print("proportion of the links that are going to contemporaries of the person")
    # does default to yes if it's unknown - statistically more likely (can be proven by looking at these values for all test files)
    print("%.2f" % (len(rel_linked) / len(linked) * 100))

    print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
    print("proportion of people linked who have been picked up by wikidata")
    # need to get the wikidata people at this point
    fileLinked = open("./output/wikidata/" + person + "_Linked.txt", "r")

    content = fileLinked.read()
    # identified by wikidata
    wikiData = content.split("\n")
    fileLinked.close()

    # additional line in the file due to the way it was set up
    wikiData.pop()
    wikiData = list(set(wikiData))

    allLinked = len(rel_linked)
    count = 0

    notIdentified = rel_linked[:]

    additional = wikiData[:]

    for human in rel_linked:
        for wiki in wikiData:
            if human in wiki or wiki in human or Levenshtein.ratio(human, wiki) > .85:
                count += 1
                notIdentified.remove(human)
                if wiki in additional:
                    additional.remove(wiki)
                break

    print("%.2f" % ((count / allLinked) * 100))
    print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")

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

    f1 = statistics(false_pos, false_neg, true_pos)

    sys.stdout.close()
    sys.stdout = stdoutOrigin

    return f1


def multiple_evaluation(person, complete):
    """
    A driver method that sets off the evaluation of the
    methods to do nlp processing of the text

    Parameters
    ----------
    person : string
        the person whose wikipedia article we are looking at
    complete : list of strings
        all the people both linked and mentioned in the article

    Returns
    -------
    performances : list of list of floats
        the precision, recall and f1 value for all the methods
    """
    performances = []
    for item in ["spacy", "nltk", "spacy_new"]:
        acc = method_evaluation(item, person, complete)
        performances.append(acc)
    return performances


def method_evaluation(method, person, complete):
    """

    A method to give statistics on how accurate the
    method passed in is performing on the wikipedia page

    Parameters
    ----------
    method : string
        how the list of names has been generated
    person : string
        the person whose wikipedia article we are looking at
    complete : list of strings
        all the people both linked and mentioned in the article

    Returns
    -------
    stats : list of floats
        the precision, recall and f1 value for the method

    """
    stdoutOrigin = sys.stdout
    person = helper.formatting(person,"_")
    sys.stdout = open("./output/" + method + "/evaluation/" + person + ".txt", "w", encoding="utf-8")

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
            if ((people in identified or identified in people) and Levenshtein.ratio(people,identified) > .75) or Levenshtein.ratio(people,identified) > 0.9:
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

    false_pos = len(noMatch)
    true_pos = numberIdentified
    false_neg = len(copyComplete)

    stats = statistics(false_pos, false_neg, true_pos)

    sys.stdout.close()
    sys.stdout = stdoutOrigin

    return stats


def evaluate_statistics(performances):
    """
    [DESCRIPTION OF METHOD HERE]

    Parameters
    ----------
    performances :

    Returns
    -------
    None.
    """
    stdoutOrigin = sys.stdout
    sys.stdout = open("./output/evaluation.txt", "w", encoding="utf-8")
    wikidata_scores = []
    spacy_scores = []
    nltk_scores = []
    new_spacy_scores = []

    for person in performances.keys():
        print(person + " performance")
        print("spacy " + str(performances[person][0]))
        spacy_scores.append(performances[person][0])
        print("nltk " + str(performances[person][1]))
        nltk_scores.append(performances[person][1])
        print("new spacy " + str(performances[person][2]))
        new_spacy_scores.append(performances[person][2])
        print("wikidata " + str(performances[person][3]))
        wikidata_scores.append(performances[person][3])
        print("")

    # take the average of each method
    num = len(performances.keys())
    spacy_average = sum(spacy_scores)/num
    nltk_average = sum(nltk_scores)/num
    new_spacy_average = sum(new_spacy_scores)/num
    wikidata_average = sum(wikidata_scores)/num

    print("spacy average : " + str(spacy_average))
    print("nltk_average : " + str(nltk_average))
    print("new spacy average : " + str(new_spacy_average))
    print("new wikidata average : " + str(wikidata_average))

    sys.stdout.close()
    sys.stdout = stdoutOrigin


def evaluate(method):
    """
    [DESCRIPTION OF METHOD HERE]

    Parameters
    ----------
    method :

    Returns
    -------
    None.
    """

    people = restart.get_test_data()
    if method == "all":
        performances = {}
        for peep in people:
            # need to do set up on each person
            complete, linked, unlinked, rel_linked = setup(peep)
            performance = multiple_evaluation(peep, complete)
            performance.append(wikidata_evaluation(peep, rel_linked, linked))
            performances[peep] = performance
        evaluate_statistics(performances)
    else:
        performances = []
        for peep in people:
            complete, linked, unlinked, rel_linked = setup(peep)
            value = method_evaluation(method, peep, complete)
            performances.append(value)
            print("")
            print(peep + ":" + str(value))
            print("")
        print("average")
        print(sum(performances)/len(performances))