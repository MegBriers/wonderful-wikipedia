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
import helper
import json

start_time = time.time()

string_thing = "https://en.wikipedia.org/wiki/"


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
    fileName = './output/wikidata/network/' + helper.formatting(person,"_") + "_Linked.txt"
    with open(fileName, "w", encoding="utf-8") as f:
        for tup in links:
            f.write(tup)
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

    for title in articles.keys():
        article = articles[title]
        mapper = WikiMapper("data/index_enwiki-latest.db")
        wikidata_id = mapper.url_to_id(article)

        title2 = substring_after(article, string_thing)

        if wikidata_id is not None:
            wikidataIds[wikidata_id] = title
        else:
            try:
                response = requests.get(
                    "https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&ppprop=wikibase_item&redirects=1&titles=" + title2 + "&format=json")

                metainfo = response.json()

                key = json_extract(metainfo, 'wikibase_item')
                if len(key) > 0:
                    wikidataIds[key[0]] = title
            except:
                pass

    return wikidataIds


def is_name(id, client_id):
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
    # Q268702 - Mary Somerville (can be used as the dummy variable regardless of the person being tested)
    entityCompare = client.get(client_id, load=True)
    # P31 - 'instance of'
    instance_of = client.get('P31', load=True)
    typesCompare = entityCompare.getlist(instance_of)
    for t in typesCompare:
        t.load()

    try:
        dob = client.get('P569', load=True)
        dod = client.get('P570', load=True)


        if type((entityCompare.getlist(dob)[0])) == int:
            date_of_birth = (entityCompare.getlist(dob)[0])
        else:
            date_of_birth = (entityCompare.getlist(dob)[0]).year

        if type((entityCompare.getlist(dod)[0])) == int:
            date_of_death = entityCompare.getlist(dod)[0]
        else:
            date_of_death = (entityCompare.getlist(dod)[0]).year
    except:
        # broad exception to catch people in the 19th century
        date_of_birth = 1900
        date_of_death = 1899

    try:
        entity = client.get(id, load=True)
        # this will throw an error whenever the item loaded is not a person currently (hence the need for try, except blocks)

        instance_of = client.get('P31', load=True)
        types = entity.getlist(instance_of)
        for t in types:
            t.load()
        result = 0
        # statistically more contemporaries on wikipedia pages than dead people ??? - design choice
        alive = True
        if (len(types) > 0):
            result = (types[0] == typesCompare[0])
        # if result is true then can check age here to see if the timelines overlapped
        if result:
            # check dob of the person lies within date_of_birth and date_of_death
            dob_compare = client.get('P569', load=True)
            dod_compare = client.get('P570', load=True)

            dates_ob = entity.getlist(dob_compare)
            dates_od = entity.getlist(dod_compare)

            if len(dates_ob) > 0 and len(dates_od) > 0:
                caught = [False, False]
                if type(dates_ob[0]) == int:
                    date_of_birth_compare = dates_ob[0]
                    caught[0] = True
                if type(dates_od[0]) == int:
                    date_of_death_compare = dates_od[0]
                    caught[1] = True

                if caught[0] == False and caught[1] == False:
                    date_of_birth_compare = (entity.getlist(dob)[0]).year
                    date_of_death_compare = (entity.getlist(dod)[0]).year
                elif caught[0] == False:
                    date_of_birth_compare = (entity.getlist(dob)[0]).year
                elif caught[1] == False:
                    date_of_death_compare = (entity.getlist(dod)[0]).year

                # used to check if the person falls within the same time span as the person whose page we are analysing
                # only checked when we know that it is a person (so we definitely have a date)
                if (date_of_birth <= date_of_birth_compare <= date_of_death) or (
                        date_of_birth_compare <= date_of_birth and date_of_death_compare >= date_of_birth):#
                    result = True
                else:
                    # doesn't matter that they are a person, because they are not a relevant person (f)
                    result = False
        return result, id

    except:
        # IF WE DON'T HAVE A GREGORIAN CALENDAR WE CAN DISREGARD THE PERSON BC THEY ARE NOT IN THE 19TH CENTURY
        pass

    return False, id


def convert_fake_unicode_to_real_unicode(string):
    return ''.join(map(chr, map(ord, string))).decode('utf-8')


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

    soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf-8')

    links = {}

    accepted_headings = ['Co']

    try:
        div3 = soup.find(id="toc")
        ul = div3.find_next('ul')
        for l in ul:
            if 'See also' in l.text or 'Bibliography' in l.text or 'Works' in l.text:
                new_links = l.find_all('a',href=True)
                accepted_headings.append(l.find_next("span", {"class": "toctext"}).text)
                break
            else:
                try:
                    new_links = l.find_all('a', href=True)
                    accepted_headings.append(l.find_next("span", {"class": "toctext"}).text)
                except:
                    pass

        for item in soup.select('a'):
            cur_h2 = item.find_next('h2')
            # magic number-y
            if cur_h2 != None and (cur_h2.text[:len(cur_h2.text)-6] in accepted_headings):
                url = item.get("href", "")
                if url.startswith("/wiki/") and "/wiki/Category" not in url:
                    title = item.get("title")
                    if title in links.keys():
                        continue
                    else:
                        links[title] = url
            else:
                break

        values = {title: "https://en.wikipedia.org" + links[title] for title in links.keys()}

        # getting the wikidata keys for all the linked articles
        dictionary = map_to_wiki_data(values)

        title_true = get_title(URL)
        dictionary_true = {title_true : "https://en.wikipedia.org/wiki/" + helper.formatting(title_true,"_")}

        wikidata_true = map_to_wiki_data(dictionary_true)

        futures = []
        results = []

        # https://stackoverflow.com/questions/52082665/store-results-threadpoolexecutor
        # concurrent execution so it is faster
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for wikidataId in dictionary.keys():
                futures.append(executor.submit(is_name, id=wikidataId, client_id=list(wikidata_true.keys())[0]))
            for future in concurrent.futures.as_completed(futures):
                # exception here
                try:
                    if future.result()[0]:
                        results.append(future.result()[1])
                except Exception as inst:
                    print(type(inst))
                    print("uh oh")

        res = [dictionary[fut] for fut in results]

        return res
    except Exception as inst:
        print(type(inst))
        return []

def request_linked(person):
    page = "https://en.wikipedia.org/wiki/" + person

    names = request_page(page)

    write_to_file(person, names)
