import timeit
import spacy
import nltk

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
