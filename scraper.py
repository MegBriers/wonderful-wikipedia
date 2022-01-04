import requests
from bs4 import BeautifulSoup
from wikidata.client import Client
from wikimapper import WikiMapper
import pandas as pd
import matplotlib.pyplot as plt
import lxml
import networkx as nx
import cchardet
import time 
from multiprocessing import Pool 
from itertools import compress

start_time = time.time()

"""
a method to map the wikipedia article to the wikidata id 
so we can figure out if the article refers to a human 
"""
def mapToWikiData(article):
    mapper = WikiMapper("data/index_enwiki-latest.db")
    wikidata_id = mapper.url_to_id(article)
    return wikidata_id

"""
a method that checks whether a wikidata entity
is a human or not (only want links to other humans)
"""
def isName(id):
    client = Client()
    entity = client.get(id, load=True)
    try:
        val = client.get('P31')
        typeOfThing = entity[val]
        if str(typeOfThing.label) == "human":
            return True
    except:
        return False
    return False

    
"""
a method to get the title of the 
current wikipedia article we are looking at
"""
def titleGetter(link):
    if "http" not in link['href']:
        return False
    
    response = requests.get(
        url=link['href'],
    )
    
    if response.status_code != 200:
        return False
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.find(id="firstHeading")
    if title:
        return title.text
    return False 

def handler(method, x):
    p = Pool(10)
    r = p.map(method, x)
    return r 

"""
kinda the driver method but should send requests out
and get all the links of the wikipedia page that are human 
"""
def requestPage(URL):
    response = requests.get(
        url=URL,
    )
    # 200 so we're chill
    assert response.status_code == 200, "request did not succeed"

    soup = BeautifulSoup(response.content, 'lxml')
    
    """

    for headline in soup('span', {'class' : 'mw-headline'}):
        print(headline.text)
        if(headline.text=="Sources"):
            break
        else:  
            links = headline.find_all('a')
            for link in links:
                print('*', link.text)   
                      
        
            links = headline.find_all('a')
            for link in links:
                print('*', link.text) 
        
        # what we need to do now 
        # go through get all links 
        # extract the names
        
        # as soon as we get to see also we are out 
        
      """  
    
    title = soup.find(id="firstHeading")

    print(title.string)

    # gets all the links within the article

    links = {}
    for link in soup.find(id="bodyContent").find_all("a"):
        url = link.get("href", "")
        # only looking for the links in the article that are wiki links atm 
        if "/wiki/" in url and "/wiki/Category" not in url:
            links[link.text.strip()] = url

    # need to go through and get all the links that are humans
    
    values = list(links.values())
    keys1 = list(links.keys())
    length = len(values)
    
    # add any spaces after each dot?? 
    
    keys = ["https://en.wikipedia.org" + i for i in values]
    
    wikiData = handler(mapToWikiData, keys)
    names = handler(isName, wikiData)
    
    indexes = list(compress(range(len(names)), names))    

    return [keys1[i] for i in indexes]


if __name__ == "__main__":
    print("Ragoonathachary")
    names = requestPage("https://en.wikipedia.org/wiki/Chinthamani_Ragoonatha_Chary")
    
    # CANNOT DEAL WITH THE FACT THAT N._R._POGSON AND N.R_.POGSON LINK TO SAME PLACE 
    print(set(names))
    
    
    f = open("demo2.txt","a")
    f.truncate(0) 
    f.write("Source,Target,weight,Type \n")
    for name in names:
        f.write("Ragoonathachary, " + name + ", Undirected" + "Ragoonathachary" + "\n")                
    f.close()  
    
    
    df = pd.read_csv('demo2.txt')
    G = nx.from_pandas_edgelist(df, 
                            source='Source',
                            target='Target',
                            edge_attr='weight')

    # create vis network
    from pyvis.network import Network

    net = Network(notebook=True)
    # load the networkx graph
    net.from_nx(G)
    # show
    net.save_graph("beautiful.html")

    
    print("--- %s seconds ---" % (time.time() - start_time))
