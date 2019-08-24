#import statements

import os, sys, click, database as db, time
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
    found            = []
    article_id_list  = []
    click.echo()                                                                           
    term             = term.lower()
    full_list        = db.get_all_titles()

    if len(term) == 1:
        for item in full_list:
            if term in item[0].lower():
                found.append(item[1])
    
    elif len(term) > 1:
        for item in full_list:
            if term in item[0].lower():
                found.append(item[1])
        if len(found) == 0:
            for item in full_list:
                
                terms         = term.split(" ")
                title_lower   = item[0].lower()
                run           = 1
                
                for term in terms:

                    term = term.lower()
                    
                    if term == "the" or term == "of" or term == "a" or term == "and" or term == "or" or term == "if" or term == "&" or term == "is" or term == "on":
                        temporary = 0
            
                    elif term in title_lower and run == 1:
                        found.append(item[1])
                        run = run + 1
                    
                    if term not in title_lower:
                        run = run + 1
                        
                        if item[0] in found:
                            found.remove(item[1])
    for full_number in found:
        article_id_list.append(db.get_article_id(full_number))
    display(article_id_list)
