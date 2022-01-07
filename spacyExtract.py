# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 20:20:54 2021

CODE THAT EXTRACTS ALL THE NAMED PEOPLE WITHIN A GIVEN ARTICLE
USING THE STANDARD SPACY MODEL

@author: Meg
"""

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import spacy
from pyvis.network import Network
import nltk 

nlp = spacy.load("xx_ent_wiki_sm")


def spacy_links(links):
    """
    
    A method that checks which of the links from a given wikipedia
    page are pages of people 

    Parameters
    ----------
    links : array of strings 
        all the links from a wikipedia article 

    Returns
    -------
    names : array of strings 
        all the links from a wikipedia article that are names
        according to spacy 

    """
    print(".・。.・゜✭ getting names via spacy i think ・.・✫・゜・。.")
    names = []
    for doc in links:
        proper = nlp(doc)
        persons = [ent.text for ent in proper.ents if ent.label_ == "PERSON"]
        if len(persons) > 0:
            names.append(persons[0])
    return names 
    
    
def spacy_text(page):
    """
    

    Parameters
    ----------
    page : string
        the content of a wikipedia page EXCLUDING everything 
        after see also 

    Returns
    -------
    persons : array of strings
        all the people named in the article 

    """
    doc = nlp(page)
    persons = [ent.text for ent in doc.ents if ent.label_ == 'PER']
    return persons 

def write_to_file(title, names):
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

    underlinedTitle = title.replace(" ", "_")

    filename = "./output/spacy/" + underlinedTitle + "_Unlinked.txt"

    # whether it is necessary to have it in this form TO BE DECIDED
    f = open(filename,"a",encoding='utf-8')
    f.truncate(0) 
    f.write("Source,Target,weight,Type \n")
    i = 0 
    for key in names:
        f.write(title + "," + key + "," + title + ",Undirected" + "\n")
        i+=1             
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
    
    
def similarNames(name, names):
    print(":)")
    # methods to check against
    # levenshtein
    # jaro winkler
    # longest common substring
    

def ntlkNames(sentence, title):
    people = []
    for sent in nltk.sent_tokenize(sentence):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                if chunk.label() == "PERSON":
                    text = ' '.join(c[0] for c in chunk)
                    people.append(text)

    # replace with title
    write_to_file("ntlk", title, people)


def extractingUnlinkedSpacy(data, title):
    # getting all the names mentioned in the text
    spacyTextResult = spacy_text(data)

    # creating the data files
    write_to_file(title, spacyTextResult)

