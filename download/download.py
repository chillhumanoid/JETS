from download import information, fileparser as parsr
from database import get_author, add_to_table, get_author_id, search, get_article_id
import util
from util import p
from requests import Session
import requests, urllib.request, sqlite3, click

def article(data, title, article_url, author_name=False):

    """
    Downloads the file

    Parameters:
    article_title  (string)\n
    author_name    (string)\n
    article_url    (string)\n
    data           (list)\n
    full_number    (string)\n
    volume_number  (int)\n
    issue_number   (int)\n
    article_number (int)\n
    """
    p(article_url)

    full_number = information.get_full_number(data)
    volume_number = information.get_volume_number(data)
    issue_number = information.get_issue_number(data)
    article_number = information.get_article_number(data)

    article_title = information.get_title(title)
    if not author_name:
        author_name = information.get_author_name(title)

    article_exists = search.articles_table(full_number)

    if article_exists:
        util.p(article_title)
        click.echo("This File Already Exists")
    else:
        util.p(full_number)
        click.echo("Title: " + article_title)
        click.echo("Author: " + author_name)
        if click.confirm("Download File?"):
            author_ids = author_database_worker(author_name)
            article_id = get_article_id.by_full_number(full_number)

            add_to_table.articles(full_number, int(volume_number), int(issue_number), int(article_number), article_title, author_ids)

            if "&amp;" in article_url:
                article_url = article_url.replace("&amp;", "&")
            r = requests.get(article_url, stream=True)

            with open(all_path + str(article_id) + ".pdf", 'wb') as file:
                file.write(r.content)
        else:
            value = click.prompt("Change (A)uthor or (T)itle or (N)either?", default="n")
            value = value.lower()
            if value == "a":
                util.p("Current Author: " + author_name)
                new_author = click.prompt("New Author Name: ")
                download(data, title, article_url, new_author)
            elif value == "t":
                util.p("Current Title: " + article_title)
                new_title = click.prompt("New Title: ")
                download(data, new_title, article_url)

def author_database_worker(author):
    """
    Adds the authors to the author table if not already there, and gets there ID after

    Parameters:
    author (string)

    Returns:
    author_ids (list)
    """
    authors = parsr.get_authors(author)
    author_ids = []
    for name in authors:
        author_name = util.get_possible_names(name)
        if author_name == None:
            author_name = name
        add_to_table.author(author_name)
        author_ids.append(get_author_id.by_name(author_name))
    return author_ids
