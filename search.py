#import statements

import os, sys, click
from PyPDF2 import PdfFileReader, PdfFileWriter

#global variables

base = "C:/Users/jonat/OneDrive/Documents/JETS/"

#functions
def main():
    if len(sys.argv) > 3:
        arg = sys.argv[2]
        if arg == "-t":
            searchArticles()
        if arg == "-a":
            searchAuthors()

def searchAuthors():
    articles = []
    if len(sys.argv) < 4:
        print()
        print("Please enter a name")
    else:
        x = 0
        listoNames = []
        name = [sys.argv[3]]
        if len(sys.argv) > 4:
            for x in range(4, len(sys.argv)):
                name.append(sys.argv[x])
        for x in name:
            for author in os.listdir(base + "Authors/"):
                names = author.split(" ")
                if x in names:
                    if not author in listoNames:
                        listoNames.append(author)
                else:
                    if author in listoNames:
                        listoNames.remove(author)
        for author in os.listdir(base + "Authors/"):
            if author in listoNames:
                for article in os.listdir(base + "Authors/" + author):
                    articles.append(article)
        printFiles(articles)

def searchArticles():    #for searching articles
    path = base + "All/"
    if len(sys.argv) < 4:    #If under 4, no search term given
        print()   #for formatting
        print("Please enter a search term.")

    else:
        found = []
        print() #for formatting
        x = 0   #used in loop iterations
        term = ' '.join(sys.argv[3:])#search term starts at point 3
        term = term.lower()
        if len(sys.argv) == 4:  #if the length is 4 exactly
            for article in os.listdir(path):  #goes through all folders in base
                f = article.lower()
                if term in f:
                    found.append(article)
        elif len(sys.argv) > 4:
            for article in os.listdir(path):
                f = article.lower()
                if term in f:    #if term is found
                    found.append(article)
            if len(found) == 0:
                for article in os.listdir(path):
                    terms = term.split(" ")
                    f = article.lower()
                    for y in terms:
                        y = y.lower()
                        if y == "the" or y == "of" or y == "a" or y == "and" or y == "or" or y == "if" or y == "&" or y == "is" or y == "on": #ignores major key words, otherwise everything would be displayed
                            temporary = 0
                        elif y in f:
                            found.append(article)
        printFiles(found)

def printFiles(articles):
    path = base + "All/"
    if not len(articles) == 0:
        u = 0
        for x in articles:
            title = x.split(" - ", 1)[1]
            title = title.split(".pdf")[0]
            z = len(title)
            if z > u:
                u = z + 2
        header = "{0:^8} | {1:^{3}} |  {2:^}".format("ARTICLE", " TITLE", "AUTHOR", u)
        click.echo(header)
        lChar = u"\u2015"
        line = ""
        for x in range(len(header) + 7): #seems self explanatory
            if x == 9 or x == 11 + u:
                line = line + "|"
            line = line + lChar
        click.echo(line)
        for article in articles:
            num = article.split(" - ", 1)[0]
            title = article.split(" - ", 1)[1]
            title = title.split(".pdf")[0]
            f = open(path + article, 'rb')
            pdf = PdfFileReader(f)
            info = pdf.getDocumentInfo()
            author = info.author
            display = "{0:<8} |  {1:<{3}}|  {2}".format(num, title, author, u)
            click.echo(display)
