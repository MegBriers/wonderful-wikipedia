import wikipediaapi
import requests
import wikipedia

""" 
A method that
"""
def print_links(page):
    links = page.links
    for title in sorted(links.keys()):
        print("%s: %s" % (title, links[title]))

"""
A method that gets all the categories that the page is related to 
(could use this to check that the people linked to are mathematicians??) 
"""
def print_categories(page):
    categories = page.categories
    for title in sorted(categories.keys()):
        print("%s: %s" % (title, categories[title]))

def links2():
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": "Albert Einstein",
        "prop": "links"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    PAGES = DATA["query"]["pages"]

    for k, v in PAGES.items():
        for l in v["links"]:
            print(l["title"])

def links3():
    print(wikipedia.summary("Bertrand Russell", sentences=3))
    print("")
    print(wikipedia.page("Bertrand Russell").links)


if __name__ == "__main__":
    wiki_wiki = wikipediaapi.Wikipedia('en')

    page_py = wiki_wiki.page('Bertrand Russell')

    print_links(page_py)

    print("")
    print_categories(page_py)
