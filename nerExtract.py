# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 20:20:54 2021

CODE THAT EXTRACTS ALL THE NAMED PEOPLE WITHIN A GIVEN ARTICLE
USING THE STANDARD SPACY AND NLTK METHODS

@author: Meg
"""

import spacy
import nltk

nlp1 = spacy.load("xx_ent_wiki_sm")
nlp2 = spacy.load("maths_ner_model")


def spacy_text(page, nlp_cur):
    """

    A method to extract all the identified people in
    the file currently being worked with using SPACY

    Parameters
    ----------
    page : string
        the content of a wikipedia page EXCLUDING everything 
        after see also

    nlp_cur : nlp model
        the relevant model for the method requested

    Returns
    -------
    persons : array of strings
        all the people named in the article

    """
    doc = nlp_cur(page)
    persons = [ent.text for ent in doc.ents if ent.label_ == 'PER']
    return persons


def write_to_file(method, title, names, folder, file_length):
    """

    A method that writes the identified names to a file
    for each person in the correct subfolder

    Parameters
    ----------
    method : string
        how the names were generated

    title : string
        the wikipedia article we are working with currently

    names : array of strings
        all of the people identified

    folder : string
        the desired folder that the file should go in
        (will always be "" when using NER but Wikidata code uses this to separate
        articles on male and female mathematicians/philosophers)

    file_length : int
        the number of characters in the given Wikipedia article

    Returns
    -------
    None.

    """
    underlined_title = title.replace(" ", "_")

    filename = "./output/" +  method  + "/" + folder + underlined_title + "_Unlinked.txt"

    f = open(filename, "a", encoding='utf-8')
    f.truncate(0)

    f.write(str(file_length))
    f.write("\n")
    i = 0
    for key in names:
        f.write(key.replace('\r', ' ').replace('\n', ' ').replace(',',' '))
        if i != len(names)-1:
            f.write("\n")
        i += 1
    f.close()


def nltk_names(text, title):
    """

    A method that uses NLTK to extract named people in the text
    from a Wikipedia article

    Parameters
    ----------
    text : string
        the text from the Wikipedia article

    title : string
        the title of the Wikipedia article whose text is being worked with

    Returns
    -------
    None.

    """
    people = []
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                if chunk.label() == "PERSON":
                    text = ' '.join(c[0] for c in chunk)
                    people.append(text)

    write_to_file("nltk", title, list(set(people)), "", len(text))


def extracting_unlinked_spacy(data, title, method, folder):
    """

    A method that allows the correct spacy model to be chosen for the method that
    was chosen for NER and ensures the names are then written to a file

    Parameters
    ----------
    data : string
        the text contents of the Wikipedia page

    title : string
        the title of the Wikipedia page from which the text came from

    method : string
        the method used to extract the names

    folder : string
        the folder in which the file should be stored
        (will always be "" for NER but can be male or female for Wikidata - aiming for consistency across files)

    Returns
    -------
    None.

    """

    # should spacy new be allowed as part of run ???

    if method == "spacy":
        text_result = spacy_text(data, nlp1)
    else:
        text_result = spacy_text(data, nlp2)

    # creating the data files
    write_to_file(method, title, text_result, folder, len(data))
