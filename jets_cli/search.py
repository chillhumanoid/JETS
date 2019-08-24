#import statements

import os, sys, click, database as db
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
    name         = author.split(" ")
    x            = 0
    found_names  = []
    articles     = []
    all_authors  = db.get_all_names()

    for x in name:
        for author in all_authors:

            names      = author.lower()

            if x.lower() in names:
                if not author in found_names:

                    found_names.append(author)
                
            else:
                if author in found_names:

                    found_names.remove(author)

        for author in found_names:
            article_id_list  = db.get_article_ids(author)

    display(article_id_list)

def article_search(term):
    found        = []
    click.echo()                                        #for formatting
    x            = 0                                    #used in loop iterations
    term         = term.lower()
    titles       = db.get_all_titles()
    if len(term) == 1:
        
        for title in titles:   
            if term in title.lower():
                found.append(title)
    
    elif len(term) > 1:
        for title in titles:
            if term in title.lower():
                found.append(title)
        if len(found) == 0:
            for title in titles:
                
                terms         = term.split(" ")
                title_lower   = title.lower()
                run           = 1
                
                for term in terms:

                    term = term.lower()
                    
                    if term == "the" or term == "of" or term == "a" or term == "and" or term == "or" or term == "if" or term == "&" or term == "is" or term == "on":
                        temporary = 0
            
                    elif term in title_lower and run == 1:
                        found.append(title)
                        run = run + 1
                    
                    if term not in title_lower:
                        run = run + 1
                        
                        if title in found:
                            found.remove(title)
    display(found)
