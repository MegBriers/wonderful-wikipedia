# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:13:11 2022

Code that compares the unique people known to be in correspondance with
Mary Somerville and those mentioned on her Wikipedia page

@author: Meg
"""

import Levenshtein

from openpyxl import load_workbook
import pandas as pd

wb = load_workbook('data\somerville_letters.xlsx')
sheet_ranges = wb['Sheet1']


correspondences = []

# currently unaware on how to get length of file from openpyxl hence the magic number
for i in range(2,649):
    # the relevant places in the excel file
    E_cur = 'E' + str(i)
    F_cur = 'F' + str(i)

    E_val = sheet_ranges[E_cur].value
    F_val = sheet_ranges[F_cur].value

    # either writing to or from her or her husband
    # getting rid of family members in the analysis
    if 'Somerville' in str(E_val):
        if not(F_val in correspondences):
            correspondences.append(F_val)
    else:
        if not(E_val in correspondences):
            correspondences.append(E_val)

print("The name of people in correspondence with Somerville:")
print(correspondences)
print("")
# 148 unique correspondences
print("Number of unique correspondences:")
print(len(correspondences))
print("")

complete = []
# the list of people manually identified from the somerville page
manual = pd.read_csv("./people/Mary_Somerville.txt")

# dealing with the way that file is set up
for index, row in manual.iterrows():
    complete.append(row["Target"])

print("Names manually identified from Somerville page:")
print(complete)
print("")

common_names = []

for name in correspondences:
    found = False
    for line in complete:
        if not(found):
            # arbitarily chosen
            # at > 0.8 we get rid of a lot of misidentified williams but we also lose the Humboldt being identified by his proper title
            if Levenshtein.ratio(name,line) > .8:
                print("")
                print("Identified correspondence:")
                print(name)
                print("Identified in article:")
                print(line)
                print("")
                print(Levenshtein.ratio(name, line))
                common_names.append(line)
                found = True

print(len(common_names))


