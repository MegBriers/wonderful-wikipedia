# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 09:09:30 2022

CODE TO PERFORM ANALYSIS OF DATA EXTRACTED FROM WIKIPEDIA ARTICLES

@author: Meg
"""

import glob
import helper
import os
import Levenshtein
from openpyxl import load_workbook
import pandas as pd

folders = ['maths', 'philosophy']


def get_file_path(file, bonus):
    """

    A method to find the file path of the given file

    Parameters
    ----------
    file : string
        the file needed to be found

    bonus : string
        a string that (if spacy) will make sure the code finds the spacy output
        as opposed to other NER methods

    Returns
    -------
    file path of the given file (None if not found)


    """
    for (root, dirs, files) in os.walk('.' + bonus):
        if file in files:
            return os.path.join(root, file)


def update_counts(figures, people, cur_person, method):
    # add one into the dictionary counts of each person if mentioned in another article
    """

    A method to find the file path of the given file

    Parameters
    ----------
    figures : dictionary
        stores the people mentioned in articles, how many times they have been mentioned and who they have been mentioned by
        STRUCTURE -> figure : [no_of_mentions, [people mentioned]]

    people : array of strings
        all the unique people mentioned in the article of cur_person

    cur_person : string
        the person whose article mentions we are working with currently

    method : string
        the way these mentions have been identified (spacy or wikidata)

    Returns
    -------
    figures : dictionary
        as above, just updated for new counts


    """
    for peep in people:
        if peep in figures.keys():
            cur_values = figures.get(peep, 0)
            name = helper.get_name_from_filename(cur_person, method)
            figures[peep] = [cur_values[0] + 1, cur_values[1] + [name]]
        else:
            figures[peep] = [1, [helper.get_name_from_filename(cur_person, method)]]
    return figures


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

    # spacy doesn't separate people by gender, compared to wikidata that stores females and males separately
    # setting subfolders to a dummy value allows the files from the two methods to be read in using a common method
    if method == "spacy":
        subfolders = [""]
    else:
        subfolders = ['male/', 'female/']

    # stores the overall length of articles and the number mentioned for each of the disciplines
    # order - links[0] = mathematicians, links[1] = philosophers
    links = []

    # same as above but stores it with a breakdown for gender (only used for wikdata where there are separate folders)
    # order - links[0][0] = male mathematicians, links[0][1] = female mathematicians, links[1][0] = male philosophers, links[1][1] = female philosophers
    gender_links = []

    # stores the statistics for the number of mentions of individuals in the articles
    # mathematicians in first entry, philosophers in second
    pop_figs = []

    for folder in folders:
        discipline_mentions = []
        folder_gender_mentions = []
        discipline_pop = {}
        for subfolder in subfolders:
            gender_dict = []
            for filepath in glob.iglob('./output/' + method + '/network/' + folder + "/" + subfolder + '*.txt'):
                file_unlinked = open(filepath)
                # relies on the fact that you have the length of the article at the top of the file !!!
                length_of_file = file_unlinked.readline().rstrip()
                identified_unlinked = list(set(line.rstrip("\n") for count, line in enumerate(file_unlinked)))
                discipline_mentions.append({length_of_file: len(identified_unlinked)})
                gender_dict.append({length_of_file: len(identified_unlinked)})
                discipline_pop = update_counts(discipline_pop, identified_unlinked, filepath, method)
                file_unlinked.close()
            folder_gender_mentions.append(gender_dict)
        links.append(discipline_mentions)
        gender_links.append(folder_gender_mentions)
        pop_figs.append(discipline_pop)
    return links, gender_links, pop_figs


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
    """

    A method that outputs the average number of mentions (either linked or unlinked, depending on method)
    from articles of mathematicians and philosophers


    Parameters
    ----------
    method : string
        the method used to extract names from article

    Returns
    -------
    None.

    """
    links, total_links, pop = read_in_file(method)

    print(links)

    avg_maths_overall, avg_maths_length, avg_maths_normalized = statistics(links[0])
    avg_phil_overall, avg_phil_length, avg_phil_normalized = statistics(links[1])

    print("          average, length, normalized")
    print("maths      " + str(format(avg_maths_overall,".2f")), str(format(avg_maths_length,".2f")), str(format(avg_maths_normalized,".2f")))
    print("philosophy " + str(format(avg_phil_overall,".2f")), str(format(avg_phil_length,".2f")), str(format(avg_phil_normalized,".2f")))
    print("")


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

            avg = len(number_linked) / (len(number_mentioned) + len(number_linked))

            overall.append(avg)
            if "female" in file_path_linked:
                female.append(avg)
            else:
                male.append(avg)

        print("male % of overall mentions that are links")
        print(sum(male) / len(male))

        print("female % of overall mentions that are links")
        print(sum(female) / len(female))

        print("overall % of overall mentions that are links")
        print(sum(overall) / len(overall))

        print("")


# most popular people in articles
def analysis_part3(method):
    links, total_links, figs = read_in_file(method)

    sorted_maths = dict(sorted(figs[0].items(), key=lambda item: item[1], reverse=True))
    sorted_phil = dict(sorted(figs[1].items(), key=lambda item: item[1], reverse=True))

    print(sorted_maths)
    print(sorted_phil)

    with open('./analysis/commonly_linked_maths_' + method + '.txt', 'w') as f:
        for key in sorted_maths.keys():
            f.write("" + key + ", " + str(sorted_maths[key][0]) + ", " + str(sorted_maths[key][1]))
            f.write('\n')

    with open('./analysis/commonly_linked_phil_' + method + '.txt', 'w') as f:
        for key in sorted_phil.keys():
            f.write("" + key + ", " + str(sorted_phil[key][0]) + ", " + str(sorted_phil[key][1]))
            f.write('\n')
    print("")
    print("")


# comparison with epsilon data
def analysis_part4():
    wb = load_workbook('data\somerville_letters.xlsx')
    sheet_ranges = wb['Sheet1']

    correspondences = {}

    # currently unaware on how to get length of file from openpyxl hence the magic number
    for i in range(2, 649):
        # the relevant places in the excel file
        E_cur = 'E' + str(i)
        F_cur = 'F' + str(i)

        E_val = sheet_ranges[E_cur].value
        F_val = sheet_ranges[F_cur].value

        # either writing to or from her or her husband
        # getting rid of family members in the analysis
        if 'Somerville' in str(E_val):
            if not (F_val in correspondences.keys()):
                correspondences[F_val] = 1
            else:
                correspondences[F_val] += 1
        else:
            if 'Somerville' in str(F_val):
                if not (E_val in correspondences):
                    correspondences[E_val] = 1
                else:
                    correspondences[E_val] += 1

    print("The name of people in correspondence with Somerville:")
    print(correspondences)
    print(".・。.・゜✭・.・✫・゜・。.")
    # 148 unique correspondences
    print("Number of unique correspondences:")
    print(len(correspondences))
    print(".・。.・゜✭・.・✫・゜・。.")

    complete = []
    # the list of people manually identified from the somerville page
    manual = pd.read_csv("./people/Mary_Somerville.txt")

    # dealing with the way that file is set up
    for index, row in manual.iterrows():
        complete.append(row["Target"])

    print("Names manually identified from Somerville page:")
    print(complete)
    print(".・。.・゜✭・.・✫・゜・。.")
    print(len(complete))

    common_names = []

    for name in correspondences.keys():
        found = False
        for line in complete:
            if not (found):
                # sort of arbitarily chosen, but experimentation with 0.7 meant too many false positives were getting through
                # could also add in a check for Ada Byron in Ada Byron (King) but then run the risk of combining fathers and sons if they are just
                # marked different by Jnr
                # at > 0.8 we get rid of a lot of misidentified williams but we also lose the Humboldt being identified by his proper title
                if Levenshtein.ratio(name, line) > .8 and not (line in common_names):
                    print("")
                    print("Identified correspondence:")
                    print(name)
                    print("Identified in article:")
                    print(line)
                    print("Levenshtein ratio:")
                    print(Levenshtein.ratio(name, line))
                    common_names.append(line)
                    found = True

    print(".・。.・゜✭・.・✫・゜・。.")
    print("Number of people found in correspondence and Wikipedia")
    print(len(common_names))
    print("People identified in correspondence and Wikipedia")
    print(common_names)
    print(".・。.・゜✭・.・✫・゜・。.")
    print("People written to in order of decreasing number of correspondences")
    new = {k: v for k, v in sorted(correspondences.items(), key=lambda item: item[1], reverse=True)}
    print(new)

