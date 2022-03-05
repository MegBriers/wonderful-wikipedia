# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 20:22:27 2021

@author: Meg
"""
import wikipedia

title = "Category:19th-century mathematicians"

page = wikipedia.page(title)

print(page.contents)