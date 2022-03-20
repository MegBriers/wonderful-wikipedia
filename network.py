# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 22:14:37 2022

Code that allows the NER and Wikidata methods to run across the whole networks of
19th century British Mathematicians and Philosophers

@author: Meg
"""
import nerExtract
import helper
import scraper


def run_on_group(method):
    """

    A method that extracts the names of the articles in each of the categories
    and uses the given method to extract names (spacy) or articles about people (wikidata)
    from each of the pages in the category

    Parameters
    ----------
    method : string
        how the names should be extracted from the page (spacy or wikidata)

    Returns
    -------
    None.

    """
    subfolder = {"https://en.wikipedia.org/wiki/Category:19th-century_British_philosophers": "philosophy/",
                 "https://en.wikipedia.org/wiki/Category:19th-century_British_mathematicians": "maths/"}
    for category in subfolder.keys():
        # list of people within the category
        list = helper.get_list(category)
        for person in list:
            # the text from the wikipedia page
            data = helper.get_page_content(person)
            # the title of the wikipedia page
            title = helper.get_page_title(person)

            # to avoid csv errors when writing to file
            if "," in title:
                substring = title.split(",", 1)
                title = substring[0]

            if method == "spacy":
                nerExtract.extracting_unlinked_spacy(data, title, "spacy/network", subfolder[category])
            else:
                scraper.request_linked(title, "network/", subfolder[category], len(data))
