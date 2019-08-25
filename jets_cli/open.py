import os, sys, subprocess, click, database as db, util
from display import display

path = os.path.realpath(__file__)
path = path.replace("open.py","")
all_path = path + "Articles/All/"


def open_author(author_name):
    """
    Open all articles by a specific author

    Parameters:
    author_name (string)
    """
    author_exists = db.search_author_table(author_name)
    if author_exists:
        article_id_list = db.get_article_ids(author_name)
        number_of_articles = str(len(article_id_list))
        if click.confirm("Are you sure you want to open all " + number_of_articles + " articles by " + author_name + "?"):
            for article_id in article_id_list:
                os.startfile(all_path + str(article_id) + ".pdf")
    else:
        util.p("Author not found")

def open_file(full_number):
    """
    Open a specific file based on the full number(volume.issue.article ##.##.##)

    Parameters:
    full_number (string)
    """
    x = 0
    article_id = db.get_article_id(full_number)
    for article in os.listdir(all_path):
        if str(article_id) + ".pdf" == article:
            os.startfile(all_path + article)
            x = x + 1
    if x == 0:
        print("Article Not Found")
