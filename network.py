import spacyExtract
import helper

def run_on_group(URLS, method):
    for category in URLS:
        list = helper.get_list(category)
        # send it through spacy processing, optionally send it through wikidata
        for person in list:
            data = helper.get_page_content(person)
            title = helper.get_page_title(person)

            if "," in title:
                substring = title.split(",",1)
                title = substring[0]

            print(title)
            print("🦆")

            spacyExtract.extracting_unlinked_spacy(data, title, "spacy")
            # do something with names

        if method != "spacy":
            print("do wikidata")
            # TO BE IMPLEMENTED