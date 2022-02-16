import wikipedia
import requests
from bs4 import BeautifulSoup
import scraper
import random


def get_list(URL):
    response = requests.get(
        url=URL,
    )

    assert response.status_code == 200, "request did not succeed"

    soup = BeautifulSoup(response.content, 'lxml')

    links = {}
    for link in soup.find(id="bodyContent").find_all("a"):
        url = link.get("href", "")
        # looking for relevant links only
        if url.startswith("/wiki/") and "/wiki/Category" not in url and "Categor" not in url:
            links[link.text.strip()] = url
    return links


def formatting(name, char):
    parts = name.split()
    new_name = ""
    for i in range(len(parts)):
        if i == 0:
            new_name = new_name + parts[i]
        else:
            new_name = new_name + char + parts[i]
    return new_name



def get_page_content(person):
    """

    A method that gets the relevant text content of the wikipedia for
    a given person

    Parameters
    ----------
    person : string
        the person whose wikipedia article we are looking at

    Returns
    -------
    substring : string
        the wikipedia page in text form ready for analysis

    """
    page = wikipedia.page(person, auto_suggest=False, redirect=True)

    # getting all the text from the page
    content = page.content

    # removing the irrelevant sections
    split_string = content.split("== See also ==", 1)

    other_areas = ["== Works ==", "== Bibliography ==", "== Further Reading ==", "== References ==", "== Main Works ==", "== Main works =="]
    for area in other_areas:
        if area in split_string[0]:
            split_string = content.split(area, 1)

    substring = split_string[0]

    return substring

def get_page_title(person):

    page = wikipedia.page(person, auto_suggest=False, redirect=True)

    return page.title

def choose_people():
    links = get_list("https://en.wikipedia.org/wiki/Category:19th-century_British_philosophers")

    values = []
    for i in range(2):
        val = random.choice(list(links.keys()))
        while val in values:
            val = random.choice(list(links.keys()))
        values.append(val)

    print(values)

def get_test_data():
    # could be made into a method
    test_set = open("./output/test_people.txt", "r")

    content = test_set.read()
    people = content.split("\n")
    test_set.close()

    people.pop()
    people = list(set(people))
    return people


def get_linked_names(person):
    """

    A method that calls the relevant part of the code to access all the linked names

    Parameters
    ----------
    person : string
        the person whose wikipedia article we are looking at

    Returns
    -------
        None.

    """
    scraper.request_page(person)