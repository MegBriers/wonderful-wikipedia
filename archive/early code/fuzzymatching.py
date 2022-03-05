# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 11:46:35 2021

@author: Meg
"""

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import numpy 


def printMatrix(distances, stringALength, stringBLength):
    for tA in range(stringALength + 1):
        for tB in range(stringBLength + 1):
            print(int(distances[tA][tB]), end=" ")
        print()

def levenshteinDistance(stringA, stringB):
    # https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/
    distances = numpy.zeros((len(stringA) + 1, len(stringB) + 1))
    
    # initializing the first row and column of matrix with integers related to length of string
    for tA in range(len(stringA)+1):
        distances[tA][0] = tA
    
    for tB in range(len(stringB)+1):
        distances[0][tB] = tB
    
    
    for tA in range(1,len(stringA)+1):
        for tB in range(1,len(stringB)+1):
            # if the two last characters are the same, distance is the same as top left
            # corner in the relevant 2 x 2 mini matrix
            # third condition wikipedia 
            if(stringA[tA-1] == stringB[tB-1]):
                distances[tA][tB] = distances[tA-1][tB-1]
            else:
                a = distances[tA][tB-1]
                b = distances[tA - 1][tB]
                c = distances[tA - 1][tB - 1]
                
                minValue = min(a,b,c)
                distances[tA][tB] = minValue + 1 
    
    printMatrix(distances,len(stringA),len(stringB))
    return int(distances[len(stringA)][len(stringB)])


def levensteinRatio(stringA,stringB):
    statistic = ((len(stringA) + len(stringB)) - levenshteinDistance(stringA,stringB))/(len(stringA) + len(stringB))
    return statistic 


# optimal partial ratio 

print("")
print(levenshteinDistance("kitten", "sitting"))

print("")
print(fuzz.partial_ratio("Somerville","Mary Somerville"))

