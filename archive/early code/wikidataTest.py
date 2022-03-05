# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 10:37:55 2021

@author: Meg
"""
from wikimapper import WikiMapper
from wikidata.client import Client

def mapToWikiData(article):
    mapper = WikiMapper("data/index_enwiki-latest.db")
    wikidata_id = mapper.url_to_id(article)
    return wikidata_id

def isName(id):
    client = Client()
    entity = client.get(id, load=True)
    try:
        val = client.get('P31')
        image = entity[val]
        print(str(image))
        # has Q5 in it but can't extract it currently
        
        print("why is this not doing anything")
        print(image.label)
        if str(image.label) == "human":
            print(":)")
            return True 
    except:
        print("rip")
        return False
    return False
    
if __name__ == "__main__":
    #doctrine of internal relations
    #Q5287598
    isName("Q8023")
