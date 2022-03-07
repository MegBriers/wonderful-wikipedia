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
plt.rc('figure', figsize=(8, 5))

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
    print(people)
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

    maths_pop = {}
    phil_pop = {}

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


            if subfolder[category] == "maths/":
                maths[0] += number_mentioned
                maths[1] += number_linked
                math_lengths_w.append({length_of_file : number_linked})
                math_lengths_s.append({length_of_file : number_mentioned})

                maths_pop = update_counts(maths_pop, mentioned, person, "spacy")
                phil_pop = update_counts(phil_pop, linked, person, "wikidata")

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
    pop_figs = [maths_pop, phil_pop]

    breakdown = [maths, male_maths, female_maths, phil, male_phil, female_phil]

    return breakdown, spacy_lengths, wikidata_lengths, pop_figs

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
    avg_maths_overall_s, avg_maths_length_s, avg_maths_normalized_s = statistics(spacy_counts[0])
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



# % linked
def analysis_part2(maths, phil, male_maths, female_maths, male_phil, female_phil):
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

    ax1.bar(labels_overall, chart3_unlinked, width, label='Unlinked', color='#1A85FF')
    ax1.bar(labels_overall, chart3_linked, width, label='Linked', bottom=chart3_unlinked, color='#D41159')

    ax1.set_ylabel('Proportion')
    ax1.set_title('Breakdown of maths and philosophy')
    ax1.legend(loc='best')

    ax2.bar(labels_maths, chart1_unlinked, width, label='Unlinked', color='#1A85FF')
    ax2.bar(labels_maths, chart1_linked, width, bottom=chart1_unlinked,
            label='Linked', color='#D41159')

    ax2.set_ylabel('Proportion')
    ax2.set_title('Breakdown of maths with gender')
    ax2.legend(loc='lower left')

    ax3.bar(labels_phil, chart2_unlinked, width, label='Unlinked', color='#1A85FF')
    ax3.bar(labels_phil, chart2_linked, width, bottom=chart2_unlinked,label='Linked', color='#D41159')

    ax3.set_ylabel('Proportion')
    ax3.set_title('Breakdown of phil with gender')
    ax3.legend(loc='lower left')

    plt.show()

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
    analysis_part1(spacy_lengths, wikidata_lengths)

    analysis_part2(breakdown[0], breakdown[1], breakdown[2], breakdown[3], breakdown[4], breakdown[5])

    #analysis_part3()

    #analysis_part4()

