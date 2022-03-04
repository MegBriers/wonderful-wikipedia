# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 09:09:30 2022

CODE TO PERFORM ANALYSIS OF DATA EXTRACTED FROM WIKIPEDIA ARTICLES

@author: Meg
"""

import glob
import helper
import os
from operator import itemgetter
import networkx as nx
from networkx.algorithms import community

folders = ['maths', 'philosophy']
subfolders = ['male', 'female']


def get_file_path(file, bonus):
    for (root, dirs, files) in os.walk('.' + bonus):
        if file in files:
            return os.path.join(root, file)


def read_in_file(method):
    """

    A method that reads in the files outputted by the method

    Parameters
    ----------
    method : string
        the method used to extract names from article

    Returns
    -------
    links : array of dictionaries
        for each item in array
            key - length of the article
            value - number of people mentioned in that article

    """
    links = []
    total_links = []
    for folder in folders:
        new_dict = []
        total_length = 0
        total_identified = 0
        # getting all the files within the correct folders
        for subfolder in subfolders:
            print('./output/' + method + '/network/' + folder + "/" + subfolder + '/*.txt')
            for filepath in glob.iglob('./output/' + method + '/network/' + folder + "/" + subfolder + '/*.txt'):
                fileUnlinked = open(filepath)
                length_of_file = fileUnlinked.readline().rstrip()
                identifiedUnlinked = list(
                    set(line.rstrip("\n") for count, line in enumerate(fileUnlinked) if count != 0))
                new_dict.append({length_of_file: len(identifiedUnlinked)})
                total_length += length_of_file
                total_identified += len(identifiedUnlinked)
                fileUnlinked.close()
        total_links.append({total_length: total_identified})
        links.append(new_dict)
    return links, total_links


def statistics(values):
    """

    A method that reads in the files outputted by the method

    Parameters
    ----------
    values : array of dictionaries
        the dictionaries relating to the article lengths and number of people linked

    Returns
    -------
    avg_overall : float
        the average number of links in the articles

    avg_length : float
        the average length of the wikipedia article (in characters of main text)

    avg_normalized : float
        the average number of links in the articles in relation to the average length of the articles
        avg number of links per character * average number of characters

    """
    avg_overall = sum(list(list(cur.values())[0] for cur in values)) / len(values)
    avg_numerator = sum([cur[list(cur.keys())[0]] / int(list(cur.keys())[0]) for cur in values]) / len(values)
    avg_length = sum(list(int(list(cur.keys())[0]) for cur in values)) / len(values)
    avg_normalized = avg_numerator * avg_length
    return avg_overall, avg_length, avg_normalized


# number of pages in an article
def analysis_part1(method):
    links, total_links = read_in_file(method)

    print(total_links)

    print(links)

    avg_maths_overall, avg_maths_length, avg_maths_normalized = statistics(total_links[0])
    avg_phil_overall, avg_phil_length, avg_phil_normalized = statistics(total_links[1])

    print("            average overall, length, normalized")
    # need to round properly
    print("maths      " + str(avg_maths_overall), str(avg_maths_length), str(avg_maths_normalized))
    print("philosophy " + str(avg_phil_overall), str(avg_phil_length), str(avg_phil_normalized))


# % linked
def analysis_part2():
    subfolder = {"https://en.wikipedia.org/wiki/Category:19th-century_British_philosophers": "philosophy/",
                 "https://en.wikipedia.org/wiki/Category:19th-century_British_mathematicians": "maths/"}
    for category in subfolder.keys():
        print(subfolder[category])
        male = []
        female = []
        overall = []

        list_of_people = helper.get_list(category)
        for person in list_of_people:
            person_format = person.replace(" ", "_")

            file_path_linked = get_file_path(person_format + "_Linked.txt", "")
            file_path_unlinked = get_file_path(person_format + "_Unlinked.txt", "\output\spacy")

            if file_path_linked is None or file_path_unlinked is None:
                continue

            file_linked = open(file_path_linked)
            file_unlinked = open(file_path_unlinked)

            file_unlinked.readline().rstrip()

            # when number goes at the top put this back in
            number_mentioned = list(set(line.rstrip("\n") for count, line in enumerate(file_unlinked)))

            number_linked = list(set(line.rstrip("\n") for count, line in enumerate(file_linked)))

            if len(number_linked) == 0 and len(number_mentioned) == 0:
                continue

            avg = len(number_linked)/(len(number_mentioned) + len(number_linked))

            overall.append(avg)
            if "female" in file_path_linked:
                female.append(avg)
            else:
                male.append(avg)

        print("male % of overall mentions that are links")
        print(sum(male)/len(male))

        print("female % of overall mentions that are links")
        print(sum(female)/len(female))

        print("overall % of overall mentions that are links")
        print(sum(overall)/len(overall))

        print("")

# most popular people in articles
def analysis_part3():
    print(";)")


# comparison with epsilon data
def analysis_part4():
    print(";0")
