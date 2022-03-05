# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 15:18:20 2021

@author: Meg
"""

import networkx as nx
import wikipedia
import pandas as pd
import matplotlib.pyplot as plt
import spacyExtract
import time 
# import pyvis
from pyvis.network import Network

# cleaning the data, remove this from the start of strings
# with being careful for cases such as missy 
# split the string by space and if there are any that are just equal to one of these prepositions
# then they're gone 
prepositions = ['Dr', 'Miss', 'Mrs', 'Ms', 'Professor', 'Sir', 'Commander', 'Messers']

"""
import nltk
# need to sort out where these things are 
from nltk.tag.stanford import NERTagger
st = NERTagger('stanford-ner/all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')
"""

nlp = spacyExtract.load("en_core_web_sm")

def identify_links(title):
    print("a")
    page = wikipedia.page(title)
    links= page.links
    return page,links 
    
    
def identify_names(docs):
    names = []
    for doc in docs:
        proper = nlp(doc)
        persons = [ent.text for ent in proper.ents if ent.label_ == "PERSON"]
        if len(persons) > 0:
            names.append(persons[0])
    return names



def identify_names_2(docs):
    doc = nlp(docs)
    persons = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
    return persons 


def write_to_file(collect):
    f = open("demofile.txt","a")
    f.truncate(0) 
    f.write("Source,Target,weight,Type \n")
    for key in collect:
        f.write("Ragoonathachary," + key + ",Ragoonathachary" + ",Undirected," + "\n")                
    f.close()  


def create_network(collect):
    write_to_file(collect)
    
    df = pd.read_csv('demofile.txt')

    # load pandas df as networkx graph
    G = nx.from_pandas_edgelist(df, 
                            source='Source',
                            target='Target',
                            edge_attr='weight')

    # create vis network
    net = Network(notebook=True)
    # load the networkx graph
    net.from_nx(G)
    # show
    net.save_graph("example.html")
 
    
def create_two_networks(spacylinks, text):
    from pyvis.network import Network

    print("a")

    write_to_file(spacylinks)
    
    df = pd.read_csv('demofile.txt')


    # load pandas df as networkx graph
    G = nx.from_pandas_edgelist(df, 
                            source='Source',
                            target='Target',
                            edge_attr='weight')


    # create vis network
    net = Network(notebook=True)
    # load the networkx graph
    net.from_nx(G)
    
    net.save_graph("spacy.html")
    
    write_to_file(text)
    
    df = pd.read_csv('demofile.txt')

    # load pandas df as networkx graph
    G = nx.from_pandas_edgelist(df, 
                            source='Source',
                            target='Target',
                            edge_attr='Source')
    # import pyvis
    from pyvis.network import Network
    # create vis network
    net = Network(notebook=True)
    # load the networkx graph
    net.from_nx(G)
    
    net.save_graph("text.html")
    
def comparison():
    # cleaning 
    # leverhulstein
    # jaro winkler
    # metaphone / SONEX 
    
    # if at least two of these are at a critical level then we can accept
    # that the strings represent the same things
    
    print("aaaaaa")
       
if __name__ == "__main__":
    start_time = time.time()
    page, links = identify_links("Chinthamani Ragoonatha Chary")
    names = identify_names(links)
    allnames = identify_names_2(page.content)
    print("Method 1 - spacy + links")
    print(names)
    print("")
    print("Method 2 - text")
    print(allnames)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    print("")
    print("Names mentioned")
    
    """
    collect = {}
    [collect.__setitem__(item,1+collect.get(item,0)) for item in names]
    [collect.__setitem__(item,1+collect.get(item,0)) for item in allnames]

    print(collect)
    
    create_network(collect)
    """
    create_two_networks(names,allnames)
    
    
