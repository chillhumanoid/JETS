import click
import os, sys

path = os.path.realpath(__file__)
path = path.replace("download\\util.py","")
article_path = path + "Articles/"

def is_login():
    click.echo(article_path + "login.txt")
    if os.path.exists(article_path + "login.txt"):
        with open(article_path + "login.txt", "r") as f:
            data = f.readlines()
            if data[0] == "":
                click.echo("No Username")
                return False
            elif data[1] == "":
                click.echo("no pwd")
                return False
            else:
                click.echo("login found")
                return True
    else:
        click.echo("login not found")
        return False

def fix_link(link):
    if "<em>" in link:
        link = link.replace("<em>", "")
        link = link.replace("</em>", "")
    if "<br/>" in link:
        link = link.replace("<br/>", "")
    if "\n" in link:
        link = link.replace("\n", "")
    return link
