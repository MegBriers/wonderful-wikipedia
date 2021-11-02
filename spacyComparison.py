# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 20:20:54 2021

@author: Meg
"""

import networkx as nx
import wikipedia
import pandas as pd
import matplotlib.pyplot as plt
import spacy
import time 
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

def write_to_file(method, name, names):
    """
    

    Parameters
    ----------
    method : string
        how the names were generated
    name : string
        the wikipedia article we are working with currently
    names : array of strings
        all of the people identified 

    Returns
    -------
    None.

    """
    filename = method + "_" + name + ".txt"
    f = open(filename,"a",encoding='utf-8')
    f.truncate(0) 
    f.write("Source,Target,weight,Type \n")
    i = 0 
    for key in names:
        f.write(name + "," + key + "," + name + ",Undirected" + "\n")   
        i+=1             
    f.close()  
    
def make_file(method, person):
    """
    
    A method to generate the graphs based on the data from
    each of the methods 

    Parameters
    ----------
    method : string
        how the people were identified 
    person : string 
        the personw hose wikipedia article we are looking at 

    Returns
    -------
    None.

    """
    filename = method + "_" + person
    
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
    
    
def ntlkNames(sentence):
    people = []
    for sent in nltk.sent_tokenize(sentence):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                if chunk.label() == "PERSON":
                    text = ' '.join(c[0] for c in chunk)
                    people.append(text)
    
    write_to_file("ntlk", "Mary Somerville", people)
    
def comparison_of_nodes(method, person):
    """
    
    A method to give statistics on how accurate the 
    method passed in is performing on the wikipedia page

    Parameters
    ----------
    method : string
        how the list of names has been generated
    person : string
        the person whose wikipedia article we are looking at 

    Returns
    -------
    None.

    """
    print(":)")
    
    filename = method + "_" + person
    
    df = pd.read_csv(filename + ".txt")

    df2 = pd.read_csv("marySomerville_manual.txt")
    
    columnManual = [] 
    
    manualLinked = []
    manualUnLinked = []
    
    columnMethod = []

    for index, row in df2.iterrows():
        columnManual.append(row["Target"])
        actualRow = row["link"].replace(' ', '')
        if actualRow == "linked":
            manualLinked.append(row["Target"])
        else:
            manualUnLinked.append(row["Target"])
    
    for index, row in df.iterrows():
        columnMethod.append(row["Target"])

    columnManual = list(set(columnManual))
    
    columnMethod = list(set(columnMethod))
    
    manualLinked = list(set(manualLinked))
    
    manualUnLinked = list(set(manualUnLinked))
    
    com = list(set(columnManual).intersection(columnMethod))
    
    print("")
    
    print("Overall proportion of people picked up")
    print("%.2f" % ((len(com)/len(columnManual))* 100)) 

    print("Proportion of unlinked people picked up")
    comUnlinked = list(set(manualUnLinked).intersection(columnMethod))
    print("%.2f" % ((len(comUnlinked)/len(manualUnLinked))* 100))    

    if method == "spacyText":
        print("Proportion of linked people picked up")    
        comLinked = list(set(manualLinked).intersection(columnMethod))
        print("%.2f" % ((len(comLinked)/len(manualLinked))* 100))    
        
    print("")
    print("Additional ones by the method")
    print(list(set(columnMethod).difference(set(columnManual))))
    print("")
    
    """
    print("unlinked people picked up")
    print(sorted(comUnlinked))
    print("")
    print("all unlinked people")
    print(sorted(manualUnLinked))
    """
    
    # not dealing with other languages very well, Greek, French 
    # print(list(set(manualLinked).difference(set(columnMethod))))
    
if __name__ == "__main__":
    title = "Mary Somerville"
    # getting the relevant wikipedia page 
    page = wikipedia.page(title)
    """
    # getting all the links in said wikipedia page (will include sources atm)
    links = page.links
    
    print(links)
    
    # getting all the links that link to names 
    spacyLinksResult = spacy_links(links)
    
    print("links analysis:")
    print(len(spacyLinksResult))
"""
    
    # getting all the text from the page 
    content = page.content 
    
    # removing the irrelevant sections 
    split_string = content.split("== See also ==", 1)

    substring = split_string[0]
    
    
    start_time_spacy = time.time()
    
    # getting all the names mentioned in the text
    spacyTextResult = spacy_text(substring)
    
    # creating the data files 
    #write_to_file("spacyLinks", title, spacyLinksResult)
    write_to_file("spacyText", title, spacyTextResult)
    
    # creating the graphs based on the files 
    #make_file("spacyLinks", title)
    make_file("spacyText", title)
    
    print("Spacy results using xx_ent_wiki_sm")
    comparison_of_nodes("spacyText", "Mary Somerville")
    
    print("--- %s seconds ---" % (time.time() - start_time_spacy))
    
    print("")
    print("NTLK results")
    
    start_time_ntlk = time.time()
    ntlkNames(substring)
    comparison_of_nodes("ntlk", "Mary Somerville")
    
    print("--- %s seconds ---" % (time.time() - start_time_ntlk))
    
    