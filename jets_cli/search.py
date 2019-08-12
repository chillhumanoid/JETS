#import statements

import os, sys, click
from PyPDF2 import PdfFileReader, PdfFileWriter
from jets_cli.util import display_info as display
#global variables

rPath = os.path.realpath(__file__)
rPath = rPath.replace("search.py","")

#functions
def authSearch(author):
    name = author.split(" ")
    x = 0
    listoNames = []
    articles = []
    for x in name:
        for author in os.listdir(rPath + "Articles/Authors/"):
            names = author.lower().split(" ")
            if x.lower() in names:
                if not author in listoNames:
                    listoNames.append(author)
                else:
                    if author in listoNames:
                        listoNames.remove(author)
        for author in os.listdir(rPath + "Articles/Authors/"):
            if author in listoNames:
                for article in os.listdir(rPath + "Articles/Authors/" + author):
                    articles.append(article)
    display(articles)

def articleSearch(term):    #for searching articles
    path = rPath + "Articles/All/"
    found = []
    click.echo() #for formatting
    x = 0   #used in loop iterations
    term = term.lower()
    if len(term) == 1:  #if the length is 4 exactly
        for article in os.listdir(path):  #goes through all folders in base
            f = article.lower()
            if term in f:
                found.append(article)
    elif len(term) > 1:
        for article in os.listdir(path):
            f = article.lower()
            if term in f:    #if term is found
                found.append(article)
        if len(found) == 0:
            for article in os.listdir(path):
                terms = term.split(" ")
                f = article.lower()
                run = 1
                for y in terms:
                    y = y.lower()
                    if y == "the" or y == "of" or y == "a" or y == "and" or y == "or" or y == "if" or y == "&" or y == "is" or y == "on": #ignores major key words, otherwise everything would be displayed
                        temporary = 0
                    elif y in f and run == 1:
                        found.append(article)
                        run = run + 1
                    if y not in f:
                        run = run + 1
                        if article in found:
                            found.remove(article)
    display(found)
