import requests
from bs4 import BeautifulSoup
from wikidata.client import Client
from wikimapper import WikiMapper
import concurrent.futures
import time

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
    entityCompare = client.get('Q268702',load=True)
    instance_of = client.get('P31', load=True)
    typesCompare = entityCompare.getlist(instance_of)
    for t in typesCompare:
        t.load()

    try:
        entity = client.get(id, load=True)
        instance_of = client.get('P31', load=True)
        # breaks after here
        types = entity.getlist(instance_of)
        for t in types:
            t.load()
        result = 0
        if(len(types) > 0):
            result = (types[0] == typesCompare[0])
        return result, id

    except Exception as inst:
        print(type(inst))
        print(id)

    return False, id

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
        if url.startswith("/wiki/") and "/wiki/Category" not in url:
            links[link.text.strip()] = url

    # need to go through and get all the links that are humans
    
    values = list(links.values())
    values = ["https://en.wikipedia.org" + i for i in values]

    # still very fast :)
    keys = mapToWikiData(values)

    # create a dictionary at this point with the ids as the keys
    dictionary = dict(zip(keys, values))

    futures = []
    results = []

    # https://stackoverflow.com/questions/52082665/store-results-threadpoolexecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for url in keys:
            futures.append(executor.submit(isName, id=url))

        for future in concurrent.futures.as_completed(futures):
            if future.result()[0]:
                results.append(future.result()[1])

    print("wikidata ids for the items who are people:")
    print(results)

    res = [dictionary[fut] for fut in results]

    return res


if __name__ == "__main__":
    print("Ragoonathachary")
    names = requestPage("https://en.wikipedia.org/wiki/Chinthamani_Ragoonatha_Chary")
    
    # can now deal with unique by the id function but also gives back the wikipedia pages and not the titles
    print(set(names))
    # would probably be very quick from here to get the titles

    print("--- %s seconds ---" % (time.time() - start_time))
