# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 22:29:14 2022

CODE CONTAINING SMALL PIECES OF FUNCTIONALITY USED IN MULTIPLE FILES
OR WITH THE POTENTIAL TO BE USED ACROSS THE FILES

@author: Meg
"""
import wikipedia
import requests
import os
from bs4 import BeautifulSoup
import scraper


def get_list(URL):
    """

    A method that returns the list of links in a given Wikipedia page
    Used to extract the list of mathematicians and philosophers from the category pages

    Parameters
    ----------
    URL : string
        the URL that needs to be scraped

    Returns
    -------
    links : dictionary with title of the page as the key and URL as the value

    """
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
    """

    A method that calls the relevant part of the code to access all the linked names

    Parameters
    ----------
    name : string
           the name that needs to be formatted

    char : character
        the single character that needs to go between first and second names
        normally a _ or " " depending on usage of the name needed

    Returns
    -------
    new_name : string
        the formatted string with char inserted in the correct place between
        parts

    """
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

    other_areas = ["== Works ==", "== Bibliography ==", "== Further Reading ==", "== References ==", "== Main Works ==",
                   "== Main works ==", "== Select bibliography =="]
    for area in other_areas:
        if area in split_string[0]:
            split_string = content.split(area, 1)

    substring = split_string[0]

    return substring


def get_page_title(person):
    """

    A method that calls the relevant part of the code to access all the linked names

    Parameters
    ----------
    person : string
        the name of the person whose Wikipedia article we want to retrieve

    Returns
    -------
    page.title : string
        the title of the person's wikipedia page

    """
    page = wikipedia.page(person, auto_suggest=False, redirect=True)

    return page.title


def get_test_data():
    """
    A method that gets the names of the figures in the test data set
    """
    test_set = open("./output/test_people.txt", "r")

    content = test_set.read()
    people = content.split("\n")
    test_set.close()

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


def output_file(file_name):
    """
    A method used to output the contents of a given file
    """
    f = open(file_name, "r")
    print(f.read())
    f.close()


def get_file_path(file, bonus):
    """

    A method to find the file path of the given file

    Parameters
    ----------
    file : string
        the file needed to be found

    bonus : string
        a string that (if spacy) will make sure the code finds the spacy output
        as opposed to other NER methods

    Returns
    -------
    file path of the given file (None if not found)


    """
    for (root, dirs, files) in os.walk('.' + bonus):
        if file in files:
            return os.path.join(root, file)


def substring_after(s, delim):
    """
    A method that returns the desired part of a string
    """
    return s.partition(delim)[2]
