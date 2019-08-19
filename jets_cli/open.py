import os, sys, subprocess, click, database
from display import display

path = os.path.realpath(__file__)
path = path.replace("open.py","")
all_path = path + "Articles/All/"


def open_author(author_name):
    articles = []
    if database.search_table(author_name):
        for number in database.get_full_numbers(author_name):
            for article in os.listdir(all_path):
                if article.startswith(number):
                    articles.append(article)
        display(articles)
        if click.confirm("Open All?"):
            for article in articles:
                os.startfile(all_path + article)
    else:
        print("Author Not Found")

def open_file(num):
    x = 0
    for article in os.listdir(all_path):
        if num in article:
            os.startfile(all_path + article)
            x = x + 1
    if x == 0:
        print("Article Not Found")
