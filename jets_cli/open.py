import os, sys, subprocess, click
from display import display

path = os.path.realpath(__file__)
path = path.replace("opener.py","")
fPath = path + "Articles/All/"
aPath = path + "Articles/Authors/"

def open_author(auth):
    articles = []
    aPaths = []
    x = 0
    for author in os.listdir(aPath):
        if auth.lower() in author.lower():
            x = x + 1
            for article in os.listdir(aPath + author):
                articles.append(article)
                aPaths.append(aPath + author + "/" + article)
    d(articles)
    if click.confirm("Open All?"):
        for pth in aPaths:
            os.startfile(pth)
    if x==0:
        print("Author Not Found")

def open_file(num):
    x = 0
    for article in os.listdir(fPath):
        if num in article:
            os.startfile(fPath + article)
            x = x + 1
    if x == 0:
        print("Article Not Found")
