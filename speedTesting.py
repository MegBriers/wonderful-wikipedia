import timeit
import spacy
import nltk
import wikipedia
from bs4 import BeautifulSoup
import requests

page = wikipedia.page("John Ruskin", auto_suggest=False, redirect=True)

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
print(substring)
print(len(substring))

response = requests.get(
    url="https://en.wikipedia.org/wiki/John_Ruskin",
)

assert response.status_code == 200, "request did not succeed"

soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf-8')

links = {}

unaccepted_headings = ['Works', 'Bibliography', 'Further Reading', 'References', 'Main Works', 'Main works', 'See also',
                       'Select bibliography']

try:
    for item in soup.select('a'):
        cur_h2 = item.find_previous('h2')
        # magic number-y
        # the ones at the top
        if cur_h2 == None or not (cur_h2.text[:len(cur_h2.text) - 6] in unaccepted_headings):
            url = item.get("href", "")
            if url.startswith("/wiki/") and "/wiki/Category" not in url and "/wiki/Special" not in url:
                title = item.get("title")
                if title in links.keys():
                    continue
                else:
                    links[title] = url
        else:
            print("breaking at : " + cur_h2.text[:len(cur_h2.text) - 6])
            break
except:
    print("uh oh")
"""
text = "Somerville was the daughter of Vice-Admiral Sir William George Fairfax, scion of a distinguished family of Fairfaxes, and she was related to several prominent Scottish houses through her mother, the admiral's second wife, Margaret Charters, daughter of Samuel Charters, a solicitor."
nlp1 = spacy.load("xx_ent_wiki_sm")

def spacy_ner():
    doc = nlp1(text)
    # 'PERSON'?
    persons = [ent.text for ent in doc.ents if ent.label_ == 'PER']
    return persons

def nltk_ner():
    people = []
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                if chunk.label() == "PERSON":
                    text = ' '.join(c[0] for c in chunk)
                    people.append(text)
    return people

if __name__ == "__main__":
    print("Spacy running time")
    print(timeit.timeit("spacy_ner()", setup="from __main__ import spacy_ner"))
    print("NLTK running time")
    print(timeit.timeit("nltk_ner()", setup="from __main__ import nltk_ner"))
"""