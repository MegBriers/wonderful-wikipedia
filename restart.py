# -*- coding: utf-8 -*-
"""
Created on Tue Jan 04 09:05:18 2022

driver code
@author: Meg
"""

import sys
import os
import spacyExtract
import scraper
import comparisonCurrent
import time
import network
import helper


def usage_options():
    """
    A method to output the usage instructions if the wrong set of parameters is entered
    """
    helper.output_file("usage.txt")


def validate_name(name):
    """

    A method that calls the relevant part of the code to access all the linked names

    Parameters
    ----------
    name : string
        the passed in name to the method
        unformatted so must be correctly formatted
        desired format Firstname_Secondname

    Returns
    -------
    os.path.isfile(filePath) : boolean
        representing whether the file for the person passed in is present in folder

    newName : string
        the string of the person passed in in a format that can be manipulated easily for rest of code

    """
    # desired file path ./people/Firstname_Secondname.txt

    newName = helper.formatting(name, "_")

    filePath = './people/' + newName + '.txt'

    return os.path.isfile(filePath), newName


if __name__ == '__main__':
    start_time = time.time()

    if len(sys.argv) < 2:
        print("number of arguments is incorrect, please refer to usage instructions")
        usage_options()
        exit(0)

    if sys.argv[1] == "test":
        people = helper.get_test_data()
        for pep in people:
            print(pep)
            print("🦆")
            data = helper.get_page_content(pep)
            if sys.argv[2] == 'spacy':
                spacyExtract.extracting_unlinked_spacy(data, pep, sys.argv[2])
            elif sys.argv[2] == 'nltk':
                spacyExtract.nltk_names(data, pep)
            elif sys.argv[2] == 'spacy_new':
                spacyExtract.extracting_unlinked_spacy(data, pep, sys.argv[2])
            elif sys.argv[2] == 'wikidata':
                scraper.request_linked(pep, "", "")
            elif sys.argv[2] == 'all':
                spacyExtract.extracting_unlinked_spacy(data, pep, "spacy")
                spacyExtract.nltk_names(data, pep)
                spacyExtract.extracting_unlinked_spacy(data, pep, "spacy_new")
                scraper.request_linked(pep, "", "")
            else:
                print("method is incorrect, please refer to usage instructions")
                usage_options()
                exit(0)

        comparisonCurrent.evaluate(sys.argv[2])
        end_time = time.time()
        time_taken = end_time - start_time
        print("time taken to run code : %.2f \n" % time_taken)

    elif sys.argv[1] == "network":
        URLS = ["https://en.wikipedia.org/wiki/Category:19th-century_British_philosophers",
                "https://en.wikipedia.org/wiki/Category:19th-century_British_mathematicians"]
        network.run_on_group(URLS, sys.argv[2])
    else:
        print("The methods you have indicated are not accepted input")
        print(".・。.・゜✭・.・✫・゜・。.")
        print("Please follow the below usage instructions")
        print(".・。.・゜✭・.・✫・゜・。.")
        usage_options()
