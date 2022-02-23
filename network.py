import spacyExtract
import helper
import scraper


def run_on_group(URLS, method):
    subfolder = {"https://en.wikipedia.org/wiki/Category:19th-century_British_philosophers": "philosophy/",
                 "https://en.wikipedia.org/wiki/Category:19th-century_British_mathematicians": "maths/"}
    for category in URLS:
        list = helper.get_list(category)
        # send it through spacy processing, optionally send it through wikidata
        for person in list:
            data = helper.get_page_content(person)
            title = helper.get_page_title(person)

            if "," in title:
                substring = title.split(",", 1)
                title = substring[0]

            print(title)
            print("🦆")

            if method == "spacy":
                spacyExtract.extracting_unlinked_spacy(data, title, "spacy/network", subfolder[category])
            else:
                scraper.request_linked(title, "network/", subfolder[category])
