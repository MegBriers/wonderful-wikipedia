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


correspondences = {}

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
        if not(F_val in correspondences.keys()):
            correspondences[F_val] = 1
        else:
            correspondences[F_val] += 1
    else:
        if 'Somerville' in str(F_val):
            if not(E_val in correspondences):
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
        if not(found):
            # sort of arbitarily chosen, but experimentation with 0.7 meant too many false positives were getting through
            # could also add in a check for Ada Byron in Ada Byron (King) but then run the risk of combining fathers and sons if they are just
            # marked different by Jnr
            # at > 0.8 we get rid of a lot of misidentified williams but we also lose the Humboldt being identified by his proper title
            if Levenshtein.ratio(name,line) > .8 and not(line in common_names):
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
print("People written to in order of increasing number of correspondences")
new = {k: v for k, v in sorted(correspondences.items(), key=lambda item: item[1])}
print(new)
