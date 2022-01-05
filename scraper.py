import requests
from bs4 import BeautifulSoup
from wikidata.client import Client
from wikimapper import WikiMapper
import concurrent.futures
import pandas as pd
import matplotlib.pyplot as plt
import lxml
import networkx as nx
import cchardet
import time 
from multiprocessing import Pool 
from itertools import compress

from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from concurrent.futures import Future

start_time = time.time()

"""
a method to map the wikipedia article to the wikidata id 
so we can figure out if the article refers to a human 
"""
def mapToWikiData(articles):
    wikidataIds = []
    for article in articles:
        mapper = WikiMapper("data/index_enwiki-latest.db")
        wikidata_id = mapper.url_to_id(article)
        wikidataIds.append(wikidata_id)
    return wikidataIds

"""
a method that checks whether a wikidata entity
is a human or not (only want links to other humans)
"""
def isName(id):
    client = Client()

    # assertion error : assert self.data is not None
    print(id)

    # some weird looking links that need chucking out so we are only left with proper links

    if id:
        entity = client.get(id, load=True)
        instance_of = client.get('P31', load=True)
        types = entity.getlist(instance_of)
        for t in types:
            t.load()
        print(types)

    return False

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

    keys = ["https://en.wikipedia.org" + i for i in values]

    # still very fast :)
    mapToWikiData(keys)

    futures = []
    futures2 = []
    # making it asynchronous
    # https://stackoverflow.com/questions/52082665/store-results-threadpoolexecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for url in keys:
            futures.append(executor.submit(isName, id=url))

        for future in concurrent.futures.as_completed(futures):
            # isName is not identifying the people who are named
            # apparently not getting any benefit of the parallelism
            print(future.result())
            if future.result():
                futures2.append(url)

    print("people who are people:")
    print(futures2)
    return keys


if __name__ == "__main__":
    print("Ragoonathachary")
    names = requestPage("https://en.wikipedia.org/wiki/Chinthamani_Ragoonatha_Chary")
    
    # CANNOT DEAL WITH THE FACT THAT N._R._POGSON AND N.R_.POGSON LINK TO SAME PLACE 
    print(set(names))
    
    """
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
    """
    
    print("--- %s seconds ---" % (time.time() - start_time))
