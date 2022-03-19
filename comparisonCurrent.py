# -*- coding: utf-8 -*-
"""
Created on Tue Jan 04 15:45:07 2022
code that should assess how well the methods have
performed against the manual test data

@author: Meg
"""
import pandas as pd
import matplotlib.pyplot as plt
import Levenshtein
import sys
import helper
import csv
import os


# to be uncommented as required
# changes window size
# plt.rc('figure', figsize=(20, 15))
# changes the font size on the graph
# plt.rcParams.update({'font.size': 25})


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
    new_name = helper.formatting(name, "_")
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
        actual_row = row["link"].replace(' ', '')
        if actual_row == "linked":
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

    # f1 score = 2 x (precision * recall)/(precision + recall)
    f1 = 2 * ((precision * recall) / (precision + recall))

    print("f1")
    print(f1)
    print("")

    return f1, precision, recall


def wikidata_evaluation(person, rel_linked, linked):
    """

    A method that analyses the performance of the wikidata way of extracting
    people that are linked in an article

    This will write to a file related to person, and only be used on the
    test set of people

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
    f1, precision, recall : float
        the f1 value as well as the precision and recall
        (representation of how well the method is picking up the people)

    """
    stdoutOrigin = sys.stdout
    person = helper.formatting(person, "_")
    sys.stdout = open("./output/wikidata/evaluation/" + person + ".txt", "w", encoding="utf-8")

    print("＊*•̩̩͙✩•̩̩͙*˚　LINKED (WIKIDATA) PERFORMANCE　˚*•̩̩͙✩•̩̩͙*˚＊")
    print("")
    print("")

    print("proportion of the links that are going to contemporaries of the person")
    print("%.2f" % (len(rel_linked) / len(linked) * 100))

    print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
    print("proportion of people linked who have been picked up by wikidata")
    # need to get the wikidata people at this point
    file_linked = open("./output/wikidata/" + person + "_Linked.txt", "r")

    # just need to get rid of first line (not needed here)
    length_of_file = file_linked.readline().rstrip()
    content = file_linked.read()

    # identified by wikidata
    wiki_data = content.split("\n")
    file_linked.close()

    # additional line in the file due to the way it was set up
    wiki_data.pop()
    wiki_data = list(set(wiki_data))

    all_linked = len(rel_linked)
    count = 0

    not_identified = rel_linked[:]

    additional = wiki_data[:]

    for human in rel_linked:
        for wiki in wiki_data:
            # comparing the given names with previously identified names
            if human in wiki or wiki in human or Levenshtein.ratio(human, wiki) > .85:
                count += 1
                not_identified.remove(human)
                if wiki in additional:
                    additional.remove(wiki)
                break

    print("%.2f" % ((count / all_linked) * 100))
    print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　　 ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")

    print("those who were not identified: ")
    print("")
    for no in not_identified:
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
    false_neg = len(not_identified)  # how many of our true ones are missing

    f1, precision, recall = statistics(false_pos, false_neg, true_pos)

    sys.stdout.close()
    sys.stdout = stdoutOrigin

    return f1, precision, recall


def multiple_evaluation(person, complete):
    """
    A driver method that sets off the evaluation of all the
    methods to do nlp processing of the text

    Parameters
    ----------
    person : string
        the person whose wikipedia article we are looking at
    complete : list of strings
        all the people both linked and mentioned in the article

    Returns
    -------
    performances : list of floats
        the precision, recall and f1 value for all the methods
    """
    performances = []
    for item in ["spacy", "nltk", "spacy_new"]:
        f1, precision, recall = method_evaluation(item, person, complete)
        performances.append(f1)
        performances.append(precision)
        performances.append(recall)
    return performances


def method_evaluation(method, person, complete):
    """

    A method to give statistics on how accurate the
    method passed in is performing on the wikipedia page

    Compares the list of identified people with the list of manually
    extracted people from the page to assess accuracy

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
    person = helper.formatting(person, "_")
    sys.stdout = open("./output/" + method + "/evaluation/" + person + ".txt", "w", encoding="utf-8")

    filename = "./output/" + method + "/" + person + "_Unlinked.txt"

    # the file that stores the method names
    file_unlinked = open(filename, encoding="utf-8")
    # first line of the file stores the length of the file in characters so needs to be ignored
    identified_unlinked = list(set(line.rstrip("\n") for count, line in enumerate(file_unlinked) if count != 0))

    stripped_unlinked = []
    for ele in identified_unlinked:
        if ele.strip():
            stripped_unlinked.append(ele)

    print("＊*•̩̩͙✩•̩̩͙*˚　" + method + " PERFORMANCE　˚*•̩̩͙✩•̩̩͙*˚＊")
    print("")
    print("")

    # remove all the typical titles
    typical_titles = ["Dr", "Miss", "Mrs", "Sir", "Mr", "Lord", "Professor"]

    for title in typical_titles:
        complete = [name.replace(title, '') for name in complete]
        identified_unlinked = [name.replace(title, '') for name in identified_unlinked]

    copy_complete = complete[:]

    copy_identified = []

    for people in complete:
        for identified in identified_unlinked:
            # criteria used to evaluate if referring to the same people (not infallible, but multiple references is
            # not an easy problem to solve)
            if ((people in identified or identified in people) and Levenshtein.ratio(people,identified) > .75) or Levenshtein.ratio(people, identified) > 0.9:
                copy_complete.remove(people)
                if not (identified in copy_identified):
                    copy_identified.append(identified)
                break

    print("Those not identified by method : ")
    print("")
    for cop in copy_complete:
        print(cop)
    print("")
    number_identified = len(complete) - len(copy_complete)

    print("Percentage identified from the proper data set (positive matches): ")
    print("%.2f" % ((number_identified / len(complete)) * 100))
    print("")
    print("Those identified by method that have not provided a match with the manual data :")
    print("")
    no_match = list(set(identified_unlinked).difference(set(copy_identified)))
    for no in no_match:
        print(no)
    print("")

    false_pos = len(no_match)
    true_pos = number_identified
    false_neg = len(copy_complete)

    f1, precision, recall = statistics(false_pos, false_neg, true_pos)

    sys.stdout.close()
    sys.stdout = stdoutOrigin

    return f1, precision, recall


def evaluate_statistics():
    """
    A method to produce graphs to illustrate the f1, precision
    and recall values for the various methods

    Not the most efficient storage system, but double indexing
    dictionaries was not the way I wanted to do it.

    Parameters
    ----------
    None.

    Returns
    -------
    None.
    """
    stdoutOrigin = sys.stdout
    sys.stdout = open("./output/evaluation.txt", "w", encoding="utf-8")

    small_methods = ['spacy', 'nltk', 'spacy_new']

    people = []

    values = ["f1", "precision", "recall"]
    methods = ["spacy", "nltk", "spacy new", "wikidata"]

    mathematicians = ["Mary Somerville", "Charles Howard Hinton"]
    results = {"f1": [[] for _ in range(4)], "precision": [[] for _ in range(4)], "recall": [[] for _ in range(4)]}
    non_maths = {"f1": [[] for _ in range(3)], "precision": [[] for _ in range(3)],
                 "recall": [[] for _ in range(3)]}

    with open('./analysis/evaluation.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            people.append(row["name"])

            for value in values:
                i = 0
                for method in methods:
                    fig = float(row[value + " " + method])
                    results[value][i].append(fig)
                    if row["name"] not in mathematicians and method != "wikidata":
                        non_maths[value][i].append(fig)
                    i += 1

    averages = {"overall": {"f1": [], "precision": [], "recall": []},
                "non maths": {"f1": [], "precision": [], "recall": []}}
    arrays = [results, non_maths]
    for i, group in enumerate(averages.keys()):
        for value in values:
            averages[group][value] = ([sum(cur_vals) / len(cur_vals) for cur_vals in arrays[i][value]])

    # used to ensure that the size of the graph was not excessive while having readable axis labels
    shrunk_peep = [helper.initials(peep, 1) for peep in people]

    non_maths_peep = [peep for peep in shrunk_peep if
                      peep not in [helper.initials(mathematician, 1) for mathematician in mathematicians]]

    print("overall f1s")
    print(averages["overall"]["f1"])
    print("non maths f1s")
    print(averages["non maths"]["f1"])

    print("overall precisions")
    print(averages["overall"]["precision"])
    print("non maths precisions")
    print(averages["non maths"]["precision"])

    print("overall recalls")
    print(averages["overall"]["recall"])
    print("non maths recalls")
    print(averages["non maths"]["recall"])

    # named entity recognition methods comparison
    # whole group - graph 1
    df0 = pd.DataFrame({'f1': averages["overall"]["f1"][:-2], 'precision': averages["overall"]["precision"][:-2],
                        'recall': averages["overall"]["recall"][:-2]}, index=small_methods[:-1])

    # non maths subset - graph 2
    df1 = pd.DataFrame({'f1': averages["non maths"]["f1"], 'precision': averages["non maths"]["precision"],
                        'recall': averages["non maths"]["recall"]}, index=small_methods)

    # nltk vs spacy precision comparison - graph 3
    df2 = pd.DataFrame({'nltk': results["precision"][1], 'spacy': results["precision"][0]}, index=shrunk_peep)

    # nltk vs spacy recall comparison - graph 4
    df2_b = pd.DataFrame({'nltk': results["recall"][1], 'spacy': results["recall"][0]}, index=shrunk_peep)

    my_colors = ['#00B2EE', '#E9967A', '#3CB371', '#8B475D']

    # comparing all NER methods f1, precision and recall
    ax = plt.subplot(111)
    df0.plot.bar(rot=0, color=my_colors, ax=ax)
    plt.xlabel('method for NER')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    # moving the legend outside of the graph
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

    ax1 = plt.subplot(111)
    df1.plot.bar(rot=0, color=my_colors, ax=ax1)
    plt.xlabel('method for NER')
    box = ax1.get_position()
    ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    # moving the legend outside of the graph
    ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

    # comparing the precision values for nltk on each test figure
    ax2 = plt.subplot(111)
    df2.plot.bar(rot=0, color=my_colors, ax=ax2)
    plt.xlabel('test figure')
    plt.xticks(rotation=45)
    plt.ylabel('precision value')
    plt.show()

    ax3 = plt.subplot(111)
    df2_b.plot.bar(rot=0, color=my_colors, ax=ax3)
    plt.xlabel('test figure')
    plt.xticks(rotation=45)
    plt.ylabel('recall value')
    plt.show()

    index_cur = shrunk_peep
    cur_values = results
    for i in range(4):
        if i == 2:
            index_cur = non_maths_peep
            cur_values = non_maths
        df_cur = pd.DataFrame(
            {'f1': cur_values["f1"][i], 'precision': cur_values["precision"][i], 'recall': cur_values["recall"][i]},
            index=index_cur)
        ax_cur = plt.subplot(111)
        df_cur.plot.bar(rot=0, color=my_colors, ax=ax_cur)
        plt.xlabel('test figure')
        plt.xticks(rotation=45)
        plt.title(i)
        box = ax_cur.get_position()
        ax_cur.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax_cur.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()
        index_cur = shrunk_peep
        cur_values = results

    sys.stdout.close()
    sys.stdout = stdoutOrigin


def write_data():
    """
    A method that writes the f1, precision and recall values of the methods to a file
    to minimise the time spent on each run generating these numbers

    If the code is re-run on the network and new .txt files have been generated for each
    person then the evaluation.csv file should be deleted to this is run again and the
    statistics are re-generated

    Parameters
    ----------
    None.

    Returns
    -------
    None.
    """
    people = helper.get_test_data()
    performances = {}
    for peep in people:
        complete, linked, unlinked, rel_linked = setup(peep)
        values = multiple_evaluation(peep, complete)
        f1_w, precision_w, recall_w = wikidata_evaluation(peep, rel_linked, linked)
        values.append(f1_w)
        values.append(precision_w)
        values.append(recall_w)
        performances[peep] = values

    with open('./analysis/evaluation.csv', 'w') as f:
        f.write(
            'name,f1 spacy,precision spacy,recall spacy,f1 nltk,precision nltk,recall nltk,f1 spacy new,precision '
            'spacy new,recall spacy new,f1 wikidata,precision wikidata,recall wikidata')
        f.write('\n')

        for peep in people:
            first_name = peep
            # prevents names with commas from ruining csv storage
            if "," in peep:
                split = peep.split(",", 1)
                first_name = split[0]

            output_line = first_name
            for i in range(12):
                output_line = output_line + "," + str(performances[peep][i])

            f.write(output_line)
            f.write('\n')
    f.close()


def evaluate(method):
    """

    A method used to ensure that the statistics data is written to the correct place
    and call analysis on this data once written

    Parameters
    ----------
    method : string
        has to be "all" because we want to compare across methods

    Returns
    -------
    None.
    """
    if method == "all":
        if not (os.path.isfile('./analysis/evaluation.csv')):
            write_data()
        evaluate_statistics()
