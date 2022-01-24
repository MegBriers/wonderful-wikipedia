# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 09:42:25 2021

CODE THAT EXTRACTS ALL THE LINKED PEOPLE IN AN ARTICLE
(INCLUDING IRRELEVANT SECTIONS ATM and irrelevant people by year of birth)

@author: Meg
"""
import requests
from bs4 import BeautifulSoup
from wikidata.client import Client
from wikimapper import WikiMapper
import concurrent.futures
import time
import restart
import json

start_time = time.time()


# https://hackersandslackers.com/extract-data-from-complex-json-python/
def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


def get_title(URL):
    response = requests.get(
        url=URL,
    )

    assert response.status_code == 200, "request did not succeed"

    soup = BeautifulSoup(response.content, 'lxml')

    title = soup.find(id="firstHeading")

    return (title.string)


def write_to_file(person, links):
    """

    A method that outputs all the titles of the linked articles to a text file
    that can be found in the /output/wikidata folder

    Parameters
    ----------
    person : string
        the person whose wikipedia article we have been scraping

    links : array of strings
        all the urls from wikipedia articles linked

    """
    print("✰⋆🌟✪🔯✨")
    fileName = './output/wikidata/' + person + "_Linked.txt"
    with open(fileName, 'w') as f:
        # Ada Lovelace making it in twice ???
        for URL in links:
            response = requests.get(
                url=URL,
            )

            assert response.status_code == 200, "request did not succeed"

            soup = BeautifulSoup(response.content, 'lxml')

            title = soup.find(id="firstHeading")

            f.write(title.string)
            f.write('\n')

def substring_after(s, delim):
    return s.partition(delim)[2]

# NEED TO MAKE CONCURRENT
def map_to_wiki_data(articles):
    """

    A  method to map the wikipedia article to the wikidata id
    so we can figure out if the article refers to a human

    Parameters
    ----------
    articles : array of strings
        all the links from a wikipedia article

    Returns
    -------
    wikidataIds : array of strings
        all the wikidata id's from the articles passed in so the wikidata information
        can be accessed

    """
    wikidataIds = {}
    string_thing = "https://en.wikipedia.org/wiki/"
    for article in articles:
        # MUST BE DOWNLOADED
        mapper = WikiMapper("data/index_enwiki-latest.db")
        wikidata_id = mapper.url_to_id(article)

        title2 = substring_after(article, string_thing)

        if wikidata_id is not None:
            wikidataIds[wikidata_id] = article
        else:
            try:
                response = requests.get(
                    "https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&ppprop=wikibase_item&redirects=1&titles=" + title2 + "&format=json")

                metainfo = response.json()

                key = json_extract(metainfo, 'wikibase_item')
                if len(key) > 0:
                    wikidataIds[key[0]] = string_thing + title2
            except:
                print("aw no")


    return wikidataIds


def is_name(id):
    """

    A method that checks whether a wikidata entity
    is a human or not (as we only want links to other humans)

    Parameters
    ----------
    id : string
        wikidata id

    Returns
    -------
    result, id : Bool, string
        whether of not the relevant id was a person and the id of the person

    """

    client = Client()
    # manually setting up an entity we know is a person to compare the entity types
    # Q268702 - Mary Somerville
    entityCompare = client.get('Q268702', load=True)
    # P31 - 'instance of'
    instance_of = client.get('P31', load=True)
    typesCompare = entityCompare.getlist(instance_of)
    for t in typesCompare:
        t.load()

    # get date of birth here 🦆

    try:
        entity = client.get(id, load=True)
        # this will throw an error whenever the item loaded is not a person currently (hence the need for try, except blocks)

        instance_of = client.get('P31', load=True)
        types = entity.getlist(instance_of)
        for t in types:
            t.load()
        result = 0
        if (len(types) > 0):
            result = (types[0] == typesCompare[0])
        # if result is true then can check age here to see if the timelines overlapped
        return result, id

    except Exception as inst:
        # 🦆 TO DO - what is the source of this problem, potentially causing people to be missed from Wikidata recognition
        # throwing way too many of these
        print(inst)
        print("✨")

    return False, id


def request_page(URL):
    """

    The driver method, gets all the titles of the wikipedia
    pages of people linked to on a given page

    Parameters
    ----------
    URL : string
        url of the wikipedia article we want to get links from

    Returns
    -------
    res : list of strings
        the title of all wikipedia pages that are linked to from main article

    """

    response = requests.get(
        url=URL,
    )

    assert response.status_code == 200, "request did not succeed"

    soup = BeautifulSoup(response.content, 'lxml')

    title = soup.find(id="firstHeading")

    print(title.string)

    links = {}
    for link in soup.find(id="bodyContent").find_all("a"):
        url = link.get("href", "")
        # only looking for the links in the article that are wiki links
        if url.startswith("/wiki/") and "/wiki/Category" not in url:
            links[link.text.strip()] = url

    values1 = list(links.values())
    print(values1)

    values = ["https://en.wikipedia.org" + i for i in values1]
    print(len(values))

    # getting the wikidata keys for all the linked articles
    dictionary = map_to_wiki_data(values)
    print(dictionary)

    futures = []
    results = []

    # https://stackoverflow.com/questions/52082665/store-results-threadpoolexecutor
    # concurrent execution so it is faster
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for wikidataId in dictionary.keys():
            futures.append(executor.submit(is_name, id=wikidataId))

        for future in concurrent.futures.as_completed(futures):
            # exception here
            try:
                if future.result()[0]:
                    results.append(future.result()[1])
            except:
                print("uh oh")

    # breaking at this part
    res = [dictionary[fut] for fut in results]

    print(res)
    return res


def request_linked(person):
    print("*＊✿❀ Requesting links　❀✿＊*")
    page = "https://en.wikipedia.org/wiki/" + person

    names = request_page(page)

    print("*＊✿❀　Writing linked people to a file ❀✿＊*")

    print(names)
    print(len(names))

    write_to_file(person, names)

    print("Time taken to extract articles linked to that where the subject atter is human : ")
    print("--- %s seconds ---" % (time.time() - start_time))
