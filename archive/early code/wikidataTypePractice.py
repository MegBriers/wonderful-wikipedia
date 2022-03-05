# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 11:49:15 2022

@author: Meg
"""

from wikidata.client import Client
client = Client()
e = client.get('Q268702', load=True)

instance_of = client.get('P31', load=True)

types = e.getlist(instance_of)

for t in types:
    t.load()

print(types)