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

    A method that uses NLTK to extract named people in the text
    from a Wikipedia article

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
            data = helper.get_page_content(person)
            title = helper.get_page_title(person)

            # to avoid messing up csv files
            # is this messing up wikidata ?
            if "," in title:
                substring = title.split(",", 1)
                title = substring[0]

            if method == "spacy":
                nerExtract.extracting_unlinked_spacy(data, title, "spacy/network", subfolder[category])
            else:
                scraper.request_linked(title, "network/", subfolder[category], len(data))
