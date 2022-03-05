# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 14:12:28 2021

@author: Meg
"""
import multiprocessing

output=[]
data = range(0,10)

def f(x):
    print("a")
    return x**2

def handler():
    p = multiprocessing.Pool(64)
    r=p.map(f, data)
    return r

if __name__ == '__main__':
    output.append(handler())
    print(output)