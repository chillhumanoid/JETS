#import statements

import os, sys, click, database
from PyPDF2 import PdfFileReader, PdfFileWriter
from display import display
#global variables

path = os.path.realpath(__file__)
path = path.replace("search.py","")
path = path + "Articles/"
all_path = path + "All/"
author_path = path + "Authors/"
#functions

def auth_search(author):
    name = author.split(" ")
    x = 0
    found_names = []
    articles = []
    all_authors = database.get_names()
    for x in name:
        for author in all_authors:
            names = author.lower()
            if x.lower() in names:
                if not author in found_names:
                    found_names.append(author)
                else:
                    if author in found_names:
                        found_names.remove(author)
        for author in found_names:
            author_article_numbers = database.get_full_numbers(author)
            for number in author_article_numbers:
                for article in os.listdir(all_path):
                    if article.startswith(number):
                        articles.append(article)
    display(articles)

def article_search(term):    #for searching articles
    found = []
    click.echo() #for formatting
    x = 0   #used in loop iterations
    term = term.lower()
    if len(term) == 1:  #if the length is 4 exactly
        for article in os.listdir(all_path):  #goes through all folders in base
            f = article.lower()
            if term in f:
                found.append(article)
    elif len(term) > 1:
        for article in os.listdir(all_path):
            f = article.lower()
            if term in f:    #if term is found
                found.append(article)
        if len(found) == 0:
            for article in os.listdir(all_path):
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
