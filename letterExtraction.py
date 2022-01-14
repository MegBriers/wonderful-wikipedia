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

i = 2

correspondences = []

# replace the floating number
for i in range(2,649):
    D_cur = 'E' + str(i)
    E_cur = 'F' + str(i)

    D_val = sheet_ranges[D_cur].value
    E_val = sheet_ranges[E_cur].value

    if 'Somerville' in str(D_val):
        if not(E_val in correspondences):
            correspondences.append(E_val)
    else:
        if not(D_val in correspondences):
            correspondences.append(D_val)

print(correspondences)
# 148 unique correspondences
print(len(correspondences))

# need to compare to how many have mentions in the wikipedia
# and look at who wasn't

complete = []
manual = pd.read_csv("./people/Mary_Somerville.txt")

for index, row in manual.iterrows():
    complete.append(row["Target"])

print(complete)

common_names = []

for name in correspondences:
    found = False
    for line in complete:
        if not(found):
            if Levenshtein.ratio(name,line) > .7:
                print("")
                print("Identified correspondence:")
                print(name)
                print("Identified in article:")
                print(line)
                print("")
                common_names.append(line)
                found = True

print(len(common_names))
