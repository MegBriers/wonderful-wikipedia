import requests

session = requests.Session()

url = "https://en.wikipedia.org/w/api.php"
params = {
    "action": "query",
    "format": "json",
    "titles": "Bertrand Russell",
    "prop": "links",
    "pllimit": "max"
}

response = session.get(url=url, params=params)
data = response.json()
pages = data["query"]["pages"]

pg_count = 1
page_titles = []

print("Page %d" % pg_count)
for key, val in pages.items():
    for link in val["links"]:
        print(link["title"])
        page_titles.append(link["title"])

while "continue" in data:
    plcontinue = data["continue"]["plcontinue"]
    params["plcontinue"] = plcontinue

    response = session.get(url=url, params=params)
    data = response.json()
    pages = data["query"]["pages"]

    pg_count += 1

    print("\nPage %d" % pg_count)
    for key, val in pages.items():
        for link in val["links"]:
            print(link["title"])
            page_titles.append(link["title"])

print("%d titles found." % len(page_titles))