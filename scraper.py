# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 09:42:25 2021

CODE THAT EXTRACTS ALL THE LINKED PEOPLE IN AN ARTICLE

@author: Meg
"""
import urllib
import requests
from bs4 import BeautifulSoup
from wikidata.client import Client
from wikimapper import WikiMapper
import concurrent.futures
import helper

string_thing = "https://en.wikipedia.org/wiki/"


# based off code from : https://hackersandslackers.com/extract-data-from-complex-json-python/
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
    """

    A method that extracts the title of a wikipedia page (if given URL as opposed to article subject's name in helper file)

    Parameters
    ----------
    URL : string
        the URL of the wikipedia whose title we would like to get

    Returns
    ----------
    title.string : string
        the title of the given Wikipedia article

    """
    response = requests.get(
        url=URL,
    )

    assert response.status_code == 200, "request did not succeed"

    soup = BeautifulSoup(response.content, 'lxml')

    title = soup.find(id="firstHeading")

    return title.string


def write_to_file(person, links, length_of_file, network, subfolder, subsubfolder):
    """

    A method that outputs all the titles of the linked articles to a text file
    that can be found in the /output/wikidata/category/gender folder

    Parameters
    ----------
    person : string
        the person whose wikipedia article we have been scraping

    links : array of strings
        all the urls from wikipedia articles linked

    length_of_file : int
        the number of characters in the given wikipedia file of the person

    network : string
        "" if run on the test set of figures, and network/ if a member of the overall network
        (allows files to go in the right folder)

    subfolder : string
        contains information on category that the person comes from
        (maths or philosopher)

    subsubfolder : string
        contains information of the gender of the person
        (male or female)

    """
    if network == "" or not (subsubfolder in ["male", "female"]): subsubfolder = ""

    file_name = './output/wikidata/' + network + subfolder + subsubfolder + "/" + helper.formatting(person,
                                                                                                    "_") + "_Linked.txt"

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(str(length_of_file))
        f.write('\n')
        for tup in links:
            if tup is not None:
                f.write(tup)
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
    wikidata_ids : array of strings
        all the wikidata id's from the articles passed in so the wikidata information
        can be accessed

    """
    wikidata_ids = {}
    string_thing = "https://en.wikipedia.org/wiki/"

    for title in articles.keys():
        article = articles[title]
        mapper = WikiMapper("data/index_enwiki-latest.db")
        wikidata_id = mapper.url_to_id(article)

        # removes the front of the string (the wikipedia URL part)
        new_title = helper.substring_after(article, string_thing)

        if wikidata_id is not None:
            wikidata_ids[wikidata_id] = title
        else:
            # request only sent if wikidata id cannot be found using local database
            # trying to minimise reliance on external requests at this stage
            try:
                response = requests.get(
                    "https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&ppprop=wikibase_item&redirects=1&titles=" + new_title + "&format=json")

                metainfo = response.json()

                # extracting the key from the json fle
                key = json_extract(metainfo, 'wikibase_item')
                if len(key) > 0:
                    wikidata_ids[key[0]] = title
            except:
                pass

    return wikidata_ids


def is_name(id, client, date_of_birth, date_of_death, types_compare):
    """

    A method that checks whether a wikidata entity
    is a human or not (as we only want links to other humans)

    Parameters
    ----------
    id : string
        wikidata id

    client : wikidata client
        allows requests to be dealt with by the api

    date_of_birth : int
        the date of birth of the person whose article we are working with

    date_of_death : int
        the date of death of the person whose article we are working with

    types_compare : list of instance_of instances from the given wikipedia page
        the type of article we are looking for (human)

    Returns
    -------
    result, id : Bool, string
        whether of not the relevant id was a person and the id of the person

    """

    try:
        entity = client.get(id, load=True)
        instance_of = client.get('P31', load=True)
        types = entity.getlist(instance_of)
        for t in types:
            t.load()
        result = 0
        # if type has been successfully retrieved
        if len(types) > 0:
            # making sure the article is written about a human
            result = (types[0] == types_compare[0])
        # if article is about person then can check age here to see if the timelines overlapped
        if result:
            # check there is an overlap between the times of the article subject and the linked person
            dob_compare = client.get('P569', load=True)
            dod_compare = client.get('P570', load=True)

            dates_ob = entity.getlist(dob_compare)
            dates_od = entity.getlist(dod_compare)

            if len(dates_ob) > 0 and len(dates_od) > 0:
                caught = [False, False]

                # dealing with the various ways that date of birth could be stored (either just year, or (date,birth,
                # year))
                if type(dates_ob[0]) == int:
                    date_of_birth_compare = dates_ob[0]
                    caught[0] = True
                if type(dates_od[0]) == int:
                    date_of_death_compare = dates_od[0]
                    caught[1] = True

                if not caught[0] and not caught[1]:
                    date_of_birth_compare = dates_ob[0].year
                    date_of_death_compare = dates_od[0].year
                elif not caught[0]:
                    date_of_birth_compare = dates_ob[0].year
                elif not caught[1]:
                    date_of_death_compare = dates_od[0].year

                # used to check if the person falls within the same time span as the person whose page we are analysing
                # only checked when we know that it is a person (so we definitely have a date)
                if (date_of_birth <= date_of_birth_compare <= date_of_death) or (
                        date_of_birth_compare <= date_of_birth <= date_of_death_compare):
                    result = True
                else:
                    # they aren't a relevant person
                    result = False
            else:
                # probably still alive (doesn't still assume this)
                result = False
        return result, id

    except:
        # IF WE DON'T HAVE A GREGORIAN CALENDAR WE CAN DISREGARD THE PERSON BC THEY ARE NOT IN THE 19TH CENTURY
        return False, id


def convert_fake_unicode_to_real_unicode(string):
    """
    Used to deal with the foreign characters that get complex when moving between URL representation
    and title representation
    """
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

    gender : string
        the gender of the subject of the article at URL

    """

    response = requests.get(
        url=URL,
    )

    assert response.status_code == 200, "request did not succeed"

    soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf-8')

    links = {}

    # a list of headings that we do not care for the content after this point in the article
    unaccepted_headings = ['Works', 'Bibliography', 'Further Reading', 'References', 'Main Works', 'Main works',
                           'See also', 'Select bibliography']

    try:
        for item in soup.select('a'):
            cur_h2 = item.find_previous('h2')
            # cur_h2 is None deals with text before the first heading (still useful)
            # [edit] follows the h2 tags so must be removed (hence the -6)
            if cur_h2 is None or not (cur_h2.text[:len(cur_h2.text) - 6] in unaccepted_headings):
                url = item.get("href", "")
                # urls that we do not care about (not going to be linking to people)
                if url.startswith("/wiki/") and "/wiki/Category" not in url and "/wiki/Special" not in url:
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

        # getting the title of the wikipedia article
        title_true = get_title(URL)

        dictionary_true = {title_true: "https://en.wikipedia.org/wiki/" + helper.formatting(title_true, "_")}

        # the wikidata value of the article being scraped
        wikidata_true = map_to_wiki_data(dictionary_true)

        futures = []
        results = []

        client = Client()

        # entity to compare to is the wikidata information of the current person whose page we are looking at
        entity_compare = client.get(list(wikidata_true.keys())[0], load=True)
        # P31 - 'instance of'
        instance_of = client.get('P31', load=True)
        gender = client.get('P21', load=True)
        types_compare = entity_compare.getlist(instance_of)
        for t in types_compare:
            t.load()

        # if we can't get the date successfully, fall back on dates that span the whole 19t century
        date_of_birth = 1900
        date_of_death = 1899

        try:
            dob = client.get('P569', load=True)
            dod = client.get('P570', load=True)

            # dealing with the various ways that date may be stored (as above)
            if type((entity_compare.getlist(dob)[0])) == int:
                date_of_birth = (entity_compare.getlist(dob)[0])
            else:
                date_of_birth = (entity_compare.getlist(dob)[0]).year

            if type((entity_compare.getlist(dod)[0])) == int:
                date_of_death = entity_compare.getlist(dod)[0]
            else:
                date_of_death = (entity_compare.getlist(dod)[0]).year
        except Exception as e:
            # broad exception to catch people in the 19th century
            print("had to go manual style")
            print(type(e))

        # based on code from : https://stackoverflow.com/questions/52082665/store-results-threadpoolexecutor
        # requests are sent concurrently in order to decrease execution time
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for wikidataId in dictionary.keys():
                futures.append(executor.submit(is_name, id=wikidataId, client=client, date_of_birth=date_of_birth,
                                               date_of_death=date_of_death, typesCompare=types_compare))
            for future in concurrent.futures.as_completed(futures):
                try:
                    if future.result()[0]:
                        results.append(future.result()[1])
                except urllib.error.URLError as e:
                    response_data = e.read().decode("utf8", 'ignore')
                    print(response_data)
                except Exception as inst:
                    print(type(inst))

        # returns the linked article titles and the gender of the person whose article we are scraping
        return [dictionary[fut] for fut in results], str(entity_compare.getlist(gender)[0].label)

    except Exception as inst:
        print(type(inst))
        return "", ""


def request_linked(person, network, subfolder, length_of_file):
    """

    A  method to map the wikipedia article to the wikidata id
    so we can figure out if the article refers to a human

    Parameters
    ----------
    person : string
        the person whose wikipedia article we are looking at

    network : string
        whether this has been called as part of evaluating network or test set
        "" if working on test set, "network/" if not

    subfolder : string
        the way we are going to be extracting the names (always wikidata in this case, but trying
        to keep consistency on write_to_file across types of NER)

    length_of_file : string
        the number of characters in the given wikipedia page

    Returns
    -------
    None.

    """
    page = "https://en.wikipedia.org/wiki/" + person

    # subsubfolder deals with gender
    names, subsubfolder = request_page(page)

    write_to_file(person, names, length_of_file, network, subfolder, subsubfolder)
