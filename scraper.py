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

start_time = time.time()


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
    wikidataIds = []
    for article in articles:
        mapper = WikiMapper("data/index_enwiki-latest.db")
        wikidata_id = mapper.url_to_id(article)
        wikidataIds.append(wikidata_id)
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

    values = list(links.values())

    values = ["https://en.wikipedia.org" + i for i in values]

    # getting the wikidata keys for all the linked articles
    keys = map_to_wiki_data(values)

    # create a dictionary at this point with the ids as the keys
    dictionary = dict(zip(keys, values))

    futures = []
    results = []

    # https://stackoverflow.com/questions/52082665/store-results-threadpoolexecutor
    # concurrent execution so it is faster
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for url in keys:
            futures.append(executor.submit(is_name, id=url))

        for future in concurrent.futures.as_completed(futures):
            # exception here
            try:
                if future.result()[0]:
                    results.append(future.result()[1])
            except:
                print("uh oh")
                
    res = [dictionary[fut] for fut in results]

    return res


def request_linked(person):
    print("*＊✿❀ Requesting links　❀✿＊*")
    page = "https://en.wikipedia.org/wiki/" + person

    names = request_page(page)

    print("*＊✿❀　Writing linked people to a file ❀✿＊*")

    write_to_file(person, names)

    print("Time taken to extract articles linked to that where the subject atter is human : ")
    print("--- %s seconds ---" % (time.time() - start_time))
