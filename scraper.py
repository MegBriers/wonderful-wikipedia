import requests
from bs4 import BeautifulSoup
from wikidata.client import Client
from wikimapper import WikiMapper

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

    soup = BeautifulSoup(response.content, 'html.parser')

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
    keys = list(links.keys())
    length = len(keys)
    
    for i in range(length):
        key = keys[i]
        # trouble links and also definitely not webpages for a human 
        if 'http' in links[key]:
            del links[key]
            continue
        
        # getting the link for their wikipedia page 
        links[key] = mapToWikiData("https://en.wikipedia.org" + links[key])
        if not (isName(links[key])):
            del links[key]
            
    # now need to sort through links and see if the items is a name
    print("Number of PEOPLE linked to")
    print(len(links))
    print("people linked to")
    # not all people, but mostly people 
    print(links) 
    return links

if __name__ == "__main__":
    names = requestPage("https://en.wikipedia.org/wiki/Chinthamani_Ragoonatha_Chary")
