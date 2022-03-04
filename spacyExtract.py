# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 20:20:54 2021

CODE THAT EXTRACTS ALL THE NAMED PEOPLE WITHIN A GIVEN ARTICLE
USING THE STANDARD SPACY MODEL

AND NLTK

POSSIBLY NEEDS RENAMING

@author: Meg
"""

import networkx as nx
import pandas as pd
import spacy
from pyvis.network import Network
import nltk

nlp = spacy.load("en_core_web_trf")
nlp1 = spacy.load("xx_ent_wiki_sm")
nlp2 = spacy.load("maths_ner_model")


def spacy_text(page, nlp_cur):
    """

    A method to extract all the identified people in
    the file getting analysised

    Parameters
    ----------
    page : string
        the content of a wikipedia page EXCLUDING everything 
        after see also

    nlp : nlp model
        the relevant model for the method requested

    Returns
    -------
    persons : array of strings
        all the people named in the article

    """
    doc = nlp_cur(page)
    # 'PERSON'?
    persons = [ent.text for ent in doc.ents if ent.label_ == 'PER']
    return persons


def write_to_file(method, title, names, folder, file_length):
    """
    

    Parameters
    ----------
    method : string
        how the names were generated
    title : string
        the wikipedia article we are working with currently
    names : array of strings
        all of the people identified 

    Returns
    -------
    None.

    """

    # THIS NEEDS TO BE FIXED THEN HOPEFULLY ACCURACY SHOULD BE BACK UP TO USUAL NUMBERS

    underlinedTitle = title.replace(" ", "_")


    filename = "./output/" +  method  + "/" + folder + underlinedTitle + "_Unlinked.txt"

    # whether it is necessary to have it in this form TO BE DECIDED 🦆
    f = open(filename, "a", encoding='utf-8')
    f.truncate(0)
    # should write file name first

    f.write(str(file_length))
    f.write("\n")
    i = 0
    for key in names:
        f.write(key.replace('\r', ' ').replace('\n', ' ').replace(',',' '))
        if i != len(names)-1:
            f.write("\n")
        i += 1
    # NEED TO NOT RIGHT A NEW LINE AT THE END BECAUSE IT WILL CAUSE AN ERROR CLOSING FILE
    f.close()


def make_graph(method, title):
    """
    
    A method to generate the graphs based on the data from
    each of the methods 

    Parameters
    ----------
    method : string
        how the people were identified 
    title : string
        the personw hose wikipedia article we are looking at 

    Returns
    -------
    None.

    """
    filename = method + "_" + title

    df = pd.read_csv(filename + ".txt")

    # load pandas df as networkx graph
    G = nx.from_pandas_edgelist(df,
                                source='Source',
                                target='Target',
                                edge_attr='weight')

    # create vis network
    net = Network(notebook=True)
    # load the networkx graph
    net.from_nx(G)

    net.save_graph(filename + ".html")

def nltk_names(text, title):
    people = []
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                if chunk.label() == "PERSON":
                    text = ' '.join(c[0] for c in chunk)
                    people.append(text)

    write_to_file("nltk", title, list(set(people)), len(text))


def extracting_unlinked_spacy(data, title, method, folder):
    # getting all the names mentioned in the text
    if method == "spacy":
        text_result = spacy_text(data, nlp1)
    elif method == "transformers":
        text_result = spacy_text(data, nlp)
    else:
        text_result = spacy_text(data,nlp2)

    # creating the data files
    write_to_file(method, title, text_result, folder, len(data))
