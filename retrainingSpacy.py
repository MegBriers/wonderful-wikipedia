# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 09:08:08 2022

GENERATING THE TEST DATA (for philosophers and mathematicians)
AND TRAINING A DOMAIN SPECIFIC MODEL
(currently the data has some interesting maths embedded)

based off the code from https://github.com/wjbmattingly/ner_youtube
(named entity recognition for digital humanities series by Dr Mattingly

@author: Meg
"""

import requests
from bs4 import BeautifulSoup
import os
import restart
import spacy
import json
import random
from spacy.training.example import Example


# block methods to do basic tasks
def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)


def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def test_model(model, text):
    doc = nlp(text)
    results = []
    entities = []
    for ent in doc.ents:
        entities.append((ent.start_char, ent.end_char, ent.label_))
    if len(entities) > 0:
        results = [text, {"entities": entities}]
        return (results)


def train_spacy(data, iterations):
    """

    A method that trains the new spacy model
    based on the JSON training data generated

    Parameters
    ----------
    data : list
        the training data in json form

    iterations : int
        how many iterations to be performed

    Returns
    -------
    nlp :
        new nlp trained model on the data passed in

    """
    TRAIN_DATA = data
    # creating a new blank model ready to be modified
    nlp = spacy.blank("en")
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe('ner', last=True)
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            # just interested in person 
            ner.add_label(ent[2])
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print("Starting iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                nlp.update([example], losses=losses, drop=0.2, sgd=optimizer)
            print(losses)
    return nlp


def train_model():
    """

    A method that turns our text based training data into the required
    JSON form

    the form that the training data has to be in is as follows
    TRAIN_DATA = [(text, {"entities": [(start, end, label)]})]
     text - the specified bit of text
     start - the starting character of that entity
     end - the ending character of that entity
     label - what kind of entity is it (person, organisation etc)

    Parameters
    ----------
    None.

    Returns
    -------
    None.

    """

    with open("data/training_data_maths.txt", "r", encoding="utf-8")as f:
        text = f.read()

        # setting up in desired form for future analysis
        chapters = text.split("PERSON")[1:]
        for chapter in chapters:
            segments = chapter.split("\n\n")[2:]
            for segment in segments:
                segment = segment.strip()
                segment = segment.replace("\n", " ")
                results = test_model(nlp, segment)
                if results is not None:
                    TRAIN_DATA.append(results)

    print(len(TRAIN_DATA))
    save_data("data/training_data_m.json", TRAIN_DATA)


def write_lists_to_file(identified, subject):
    """

    A method that writes the person and their wikipedia content to the
    text file that will be converted to JSON for training purposes.

    Parameters
    ----------
    identified : list of strings
        all the identified people in the given category

    subject : string
        the given category (maths or philosophy)

    Returns
    -------
    None.

    """
    fileName = './data/training_data_' + subject + '.txt'
    with open(fileName, 'w', encoding="utf-8") as f:
        f.write("PERSON")
        f.write('\n \n')
        for person in identified:
            print(person)
            try:
                content = restart.get_page_content(person)
                f.write(person)
                f.write('\n \n')
                f.write(content)
                f.write('\n \n')
                f.write("PERSON")
                f.write('\n \n')
            except Exception as e:
                # does trip up on a few pages (like George Boole?)
                print(e)


def get_list_data(URL):
    """

    A method that identifies all the people on each of the
    category pages for mathematicians or philosophers

    Parameters
    ----------
    URL : string
        the url of the category we are wanting to identify people from

    Returns
    -------
    links : the wikipedia part of the link for all the people linked on the page

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
            print(url)
            links[link.text.strip()] = url

    return links


if __name__ == '__main__':
    filePath1 = './data/training_data_maths.txt'
    filePath2 = './data/training_data_philosophy.txt'
    # if the files are not present then the data needs to be created
    if not (os.path.isfile(filePath1)) or not (os.path.isfile(filePath2)):
        print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　creating test data for retraining   ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
        print("")
        webpages = ["https://en.wikipedia.org/wiki/Category:19th-century_British_mathematicians",
                    "https://en.wikipedia.org/wiki/Category:19th-century_British_philosophers"]
        subjects = ["maths", "philosophy"]
        for i in range(2):
            webpage = webpages[i]
            links = get_list_data(webpage)
            write_lists_to_file(links, subjects[i])

    print("｡･:*:･ﾟ★,｡･:*:･ﾟ☆　retraining spacy, this might take a while   ｡･:*:･ﾟ★,｡･:*:･ﾟ☆")
    # just training on maths data atm
    nlp = spacy.load("xx_ent_wiki_sm")
    TRAIN_DATA = load_data("data/training_data_m.json")
    nlp = train_spacy(TRAIN_DATA, 30)
    nlp.to_disk("maths_ner_model")
