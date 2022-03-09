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
import matplotlib.pyplot as plt
import numpy as np

plt.rc('figure', figsize=(15, 5))
my_colors = ['#79CDCD', '#FF7F00']

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
            figures[peep] = [cur_values[0] + 1, cur_values[1] + [cur_person]]
        else:
            figures[peep] = [1, [cur_person]]
    return figures


def setup():
    subfolder = {"https://en.wikipedia.org/wiki/Category:19th-century_British_philosophers": "philosophy/",
                 "https://en.wikipedia.org/wiki/Category:19th-century_British_mathematicians": "maths/"}

    maths = [0,0]
    phil = [0,0]

    pop = {'spacy' : [], 'wikidata' : []}

    maths_pop_s = {}
    phil_pop_s = {}

    maths_pop_w = {}
    phil_pop_w = {}

    phil_lengths_s = []
    math_lengths_s = []

    male_maths_lengths_s = []
    female_maths_lengths_s = []

    male_phil_lengths_s = []
    female_phil_lengths_s = []

    phil_lengths_w = []
    math_lengths_w = []

    male_maths_lengths_w = []
    female_maths_lengths_w = []

    male_phil_lengths_w = []
    female_phil_lengths_w = []

    female_maths = [0,0]
    female_phil = [0,0]

    male_maths = [0,0]
    male_phil = [0,0]

    # DOES IT THE OPPOSITE ORDER

    for category in subfolder.keys():
        print(category)
        print("")
        list_of_people = helper.get_list(category)
        for person in list_of_people:
            person_format = person.replace(" ", "_")

            file_path_linked = get_file_path(person_format + "_Linked.txt", "")
            file_path_unlinked = get_file_path(person_format + "_Unlinked.txt", "\output\spacy")

            if file_path_linked is None or file_path_unlinked is None:
                continue

            file_linked = open(file_path_linked)
            file_unlinked = open(file_path_unlinked)

            # get rid of the first line
            length_of_file = file_unlinked.readline().rstrip()

            # when number goes at the top put this back in
            mentioned = list(set(line.rstrip("\n") for count, line in enumerate(file_unlinked)))

            linked = list(set(line.rstrip("\n") for count, line in enumerate(file_linked)))

            # dealing with requests that went wrong
            if len(mentioned) == 0 and len(linked) == 0:
                continue

            number_linked = len(linked)
            number_mentioned = len(mentioned)

            print(person)
            print("number linked : " + str(number_linked))
            print("number mentioned : " + str(number_mentioned))
            print("file length : " + str(length_of_file))
            print("")

            if subfolder[category] == "maths/":
                maths[0] += number_mentioned
                maths[1] += number_linked
                math_lengths_w.append({length_of_file : number_linked})
                math_lengths_s.append({length_of_file : number_mentioned})

                maths_pop_s = update_counts(maths_pop_s, mentioned, person, "spacy")
                maths_pop_w = update_counts(maths_pop_w, linked, person, "wikidata")

                if "female" in file_path_linked:
                    female_maths[0] += number_mentioned
                    female_maths[1] += number_linked

                    female_maths_lengths_s.append({length_of_file : number_mentioned})
                    female_maths_lengths_w.append({length_of_file : number_linked})

                else:
                    male_maths[0] += number_mentioned
                    male_maths[1] += number_linked

                    male_maths_lengths_s.append({length_of_file : number_mentioned})
                    male_maths_lengths_w.append({length_of_file : number_linked})
            else:
                phil[0] += number_mentioned
                phil[1] += number_linked
                phil_lengths_w.append({length_of_file: number_linked})
                phil_lengths_s.append({length_of_file: number_mentioned})


                phil_pop_s = update_counts(phil_pop_s, mentioned, person, "spacy")
                phil_pop_w = update_counts(phil_pop_w, linked, person, "wikidata")

                if "female" in file_path_linked:
                    female_phil[0] += number_mentioned
                    female_phil[1] += number_linked

                    female_phil_lengths_s.append({length_of_file : number_mentioned})
                    female_phil_lengths_w.append({length_of_file : number_linked})
                else:
                    male_phil[0] += number_mentioned
                    male_phil[1] += number_linked

                    male_phil_lengths_s.append({length_of_file : number_mentioned})
                    male_phil_lengths_w.append({length_of_file : number_linked})

    spacy_lengths = [math_lengths_s, male_maths_lengths_s, female_maths_lengths_s, phil_lengths_s, male_phil_lengths_s, female_phil_lengths_s]
    wikidata_lengths = [math_lengths_w, male_maths_lengths_w, female_maths_lengths_w, phil_lengths_w, male_phil_lengths_w, female_phil_lengths_w]

    pop['spacy'] = [maths_pop_s, phil_pop_s]
    pop['wikidata'] = [maths_pop_w, phil_pop_w]

    breakdown = [maths, male_maths, female_maths, phil, male_phil, female_phil]

    return breakdown, spacy_lengths, wikidata_lengths, pop


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
    return float(format(avg_overall,".2f")), float(format(avg_length,".2f")), float(format(avg_normalized,".2f"))


# number of pages in an article
def analysis_part1(spacy_counts, wikidata_counts):
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
    print("DISCIPLINE ANALYSIS")
    print("maths")
    avg_maths_overall_s, avg_maths_length_s, avg_maths_normalized_s = statistics(spacy_counts[0])
    print("philosophy")
    avg_phil_overall_s, avg_phil_length_s, avg_phil_normalized_s = statistics(spacy_counts[3])

    print("spacy")
    print("          average, length, normalized")
    print("maths      " + str(avg_maths_overall_s), str(avg_maths_length_s), str(avg_maths_normalized_s))
    print("philosophy " + str(avg_phil_overall_s), str(avg_phil_length_s), str(avg_phil_normalized_s))


    avg_maths_overall_w, avg_maths_length_w, avg_maths_normalized_w = statistics(wikidata_counts[0])
    avg_phil_overall_w, avg_phil_length_w, avg_phil_normalized_w = statistics(wikidata_counts[3])

    print("wikidata")
    print("          average, length, normalized")
    print("maths      " + str(avg_maths_overall_w), str(avg_maths_length_w), str(avg_maths_normalized_w))
    print("philosophy " + str(avg_phil_overall_w), str(avg_phil_length_w), str(avg_phil_normalized_w))

    print("")
    print("gender breakdown")
    avg_maths_overall_s_f, avg_maths_length_s_f, avg_maths_normalized_s_f = statistics(spacy_counts[2])
    avg_phil_overall_s_f, avg_phil_length_s_f, avg_phil_normalized_s_f = statistics(spacy_counts[5])

    print("spacy female")
    print("          average, length, normalized")
    print("maths      " + str(avg_maths_overall_s_f), str(avg_maths_length_s_f), str(avg_maths_normalized_s_f))
    print("philosophy " + str(avg_phil_overall_s_f), str(avg_phil_length_s_f), str(avg_phil_normalized_s_f))


    avg_maths_overall_w_f, avg_maths_length_w_f, avg_maths_normalized_w_f = statistics(wikidata_counts[2])
    avg_phil_overall_w_f, avg_phil_length_w_f, avg_phil_normalized_w_f = statistics(wikidata_counts[5])

    print("wikidata female")
    print("          average, length, normalized")
    print("maths      " + str(avg_maths_overall_w_f), str(avg_maths_length_w_f), str(avg_maths_normalized_w_f))
    print("philosophy " + str(avg_phil_overall_w_f), str(avg_phil_length_w_f), str(avg_phil_normalized_w_f))

    print("MALE")

    avg_maths_overall_s_m, avg_maths_length_s_m, avg_maths_normalized_s_m = statistics(spacy_counts[1])
    avg_phil_overall_s_m, avg_phil_length_s_m, avg_phil_normalized_s_m = statistics(spacy_counts[4])

    print("spacy male")
    print("          average, length, normalized")
    print("maths      " + str(avg_maths_overall_s_m), str(avg_maths_length_s_m), str(avg_maths_normalized_s_m))
    print("philosophy " + str(avg_phil_overall_s_m), str(avg_phil_length_s_m), str(avg_phil_normalized_s_m))

    avg_maths_overall_w_m, avg_maths_length_w_m, avg_maths_normalized_w_m = statistics(wikidata_counts[1])
    avg_phil_overall_w_m, avg_phil_length_w_m, avg_phil_normalized_w_m = statistics(wikidata_counts[4])

    print("wikidata male")
    print("          average, length, normalized")
    print("maths      " + str(avg_maths_overall_w_m), str(avg_maths_length_w_m), str(avg_maths_normalized_w_m))
    print("philosophy " + str(avg_phil_overall_w_m), str(avg_phil_length_w_m), str(avg_phil_normalized_w_m))

    label_fig12 = ["maths", "philosophy"]

    label_fig34 = ["male math", "male phil", "female maths", "female phil"]

    data = []
    data.append([avg_maths_normalized_s_m, avg_phil_normalized_s_m, avg_maths_normalized_s_f, avg_phil_normalized_s_f])
    data.append([avg_maths_normalized_w_m, avg_phil_normalized_w_m, avg_maths_normalized_w_f, avg_phil_normalized_w_f])

    data2 = []
    data2.append([avg_maths_normalized_s, avg_phil_normalized_s])
    data2.append([avg_maths_normalized_w, avg_phil_normalized_w])

    df = pd.DataFrame({'Spacy' : data[0], 'Wikidata' : data[1]}, index = label_fig34)

    df2 = pd.DataFrame({'Spacy' : data2[0], 'Wikidata' : data2[1]}, index=label_fig12)

    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()

    df.plot.bar(rot=0, color=my_colors, ax=ax)
    df2.plot.bar(rot=0, color=my_colors, ax=ax2)

    ax.set_xlabel('Group classification')
    ax.set_ylabel('Number of mentions picked up by given method')
    ax.set_title('Mentions in an article by group and gender')


    ax2.set_xlabel('Group classification')
    ax2.set_ylabel('Number of mentions picked up by given method')
    ax2.set_title('Mentions in an article by group')

    plt.show()


# % linked
def analysis_part2(maths, male_maths, female_maths, phil, male_phil, female_phil):
    avg_maths = float(format(maths[0]/(maths[0]+maths[1]),".4f"))
    avg_phil = float(format(phil[0]/(phil[0]+phil[1]), ".4f"))

    avg_maths_m = float(format(male_maths[0]/(male_maths[0]+male_maths[1]),".4f"))
    avg_maths_f = float(format(female_maths[0]/(female_maths[0]+female_maths[1]),".4f"))

    avg_phil_m = float(format(male_phil[0]/(male_phil[0]+male_phil[1]),".4f"))
    avg_phil_f = float(format(female_phil[0]/(female_phil[0]+female_phil[1]),".4f"))


    print("maths breakdown")
    print("average maths linked : " + str(1 - avg_maths))
    print("average male maths linked : " + str(1 - avg_maths_m))
    print("average female maths linked : " + str(1 - avg_maths_f))

    print("")
    print("phil breakdown")
    print("average phil linked : " + str(1 - avg_phil))
    print("average male phil linked : " + str(1 - avg_phil_m))
    print("average female phil linked : " + str(1 - avg_phil_f))

    labels_maths = ["maths", "male maths", "female maths"]

    labels_phil = ["phil", "male phil", "female phil"]

    labels_overall = ["maths", "phil"]

    chart1_linked = [1 - avg_maths, 1 - avg_maths_m, 1 - avg_maths_f]
    chart1_unlinked = [avg_maths, avg_maths_m, avg_maths_f]

    chart2_linked = [1 - avg_phil, 1 - avg_phil_m, 1 - avg_phil_f]
    chart2_unlinked = [avg_phil, avg_phil_m, avg_phil_f]

    chart3_linked = [1 - avg_maths, 1 - avg_phil]
    chart3_unlinked = [avg_maths, avg_phil]

    fig, (ax2, ax3) = plt.subplots(1, 2, sharey=True)

    fig2, ax1 = plt.subplots()

    width = 0.25

    ax1.bar(labels_overall, chart3_unlinked, width, label='Unlinked', color=my_colors[0])
    ax1.bar(labels_overall, chart3_linked, width, label='Linked', bottom=chart3_unlinked, color=my_colors[1])

    ax1.set_xlabel('Group classification')
    ax1.set_ylabel('Proportion')
    ax1.set_title('Breakdown of maths and philosophy')
    ax1.legend(loc='best')

    ax2.bar(labels_maths, chart1_unlinked, width, label='Unlinked', color=my_colors[0])
    ax2.bar(labels_maths, chart1_linked, width, bottom=chart1_unlinked,
            label='Linked', color=my_colors[1])

    ax2.set_ylabel('Group classification')
    ax2.set_ylabel('Proportion')
    ax2.set_title('Breakdown of maths with gender')
    ax2.legend(loc='lower left')

    ax3.bar(labels_phil, chart2_unlinked, width, label='Unlinked', color=my_colors[0])
    ax3.bar(labels_phil, chart2_linked, width, bottom=chart2_unlinked,label='Linked', color=my_colors[1])

    ax3.set_ylabel('Proportion')
    ax3.set_title('Breakdown of phil with gender')
    ax3.legend(loc='lower left')

    plt.show()

# most popular people in articles
def analysis_part3(figs):

    # NEED TO LOOP THROUGH KEYS (different methods)

    for method in figs.keys():
        print(len(figs[method]))

        print("")
        print(figs[method][0])
        print("")
        print(figs[method][1])
        print("")

        sorted_maths = dict(sorted(figs[method][0].items(), key=lambda item: item[1], reverse=True))
        sorted_phil = dict(sorted(figs[method][1].items(), key=lambda item: item[1], reverse=True))

        top_phil = []
        top_maths = []

        math_num = []
        phil_num = []


        with open('./analysis/commonly_linked_maths_' + method + '.txt', 'w') as f:
            i = 0
            for key in sorted_maths.keys():
                f.write("" + key + ", " + str(sorted_maths[key][0]) + ", " + str(sorted_maths[key][1]))
                if i < 11 and key != "Recent changes in pages linked from this page [k]":
                    top_maths.append(key)
                    math_num.append(sorted_maths[key][0])
                i+=1
                f.write('\n')

        with open('./analysis/commonly_linked_phil_' + method + '.txt', 'w') as f:
            i = 0
            for key in sorted_phil.keys():
                f.write("" + key + ", " + str(sorted_phil[key][0]) + ", " + str(sorted_phil[key][1]))
                if i < 10:
                    top_phil.append(key)
                    phil_num.append(sorted_phil[key][0])
                i+=1
                f.write('\n')
        print("")
        print("")

        print(top_maths)
        print("")
        print("")
        print(math_num)

        fig, ax = plt.subplots()
        fig2, ax2 = plt.subplots()

        ax.barh(top_maths, math_num, color=my_colors[0])
        ax.invert_yaxis()
        ax.set_xlabel('Number of mentions')
        ax.set_title('Commonly identified mathematicians using ' + method)
        ax.set_xticks(np.arange(0, max(math_num) + 1, 1))

        ax2.barh(top_phil, phil_num, color=my_colors[0])
        ax2.invert_yaxis()
        ax2.set_xlabel('Number of mentions')
        ax2.set_title('Commonly identified philosophers using ' + method)
        ax2.set_xticks(np.arange(0, max(phil_num) +1, 1))

        plt.show()


# comparison with epsilon data
def analysis_part4():
    """

    Code that compares the unique people known to be in correspondence with
    Mary Somerville and those mentioned on her Wikipedia page


    Parameters
    ----------
    None.

    Returns
    -------
    None.

    """
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


def start():
    print("YEE HAW")
    breakdown, spacy_lengths, wikidata_lengths, pop_figs = setup()
    print("")
    #analysis_part1(spacy_lengths, wikidata_lengths)

    analysis_part2(breakdown[0], breakdown[1], breakdown[2], breakdown[3], breakdown[4], breakdown[5])

    analysis_part3(pop_figs)

    #analysis_part4()

