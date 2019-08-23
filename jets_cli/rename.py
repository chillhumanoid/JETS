import sys, os, time, subprocess, click, database as db
from pathvalidate import ValidationError, validate_filename; from shutil import copyfile, move
import util
path = os.path.realpath(__file__)
path = path.replace("rename.py","")
path = path + "Articles/"
all_path = path + "All/"
author_path = path + "Authors/"

def display_title_author(title, author, new_title, new_author):
    """
    displays based on if title or author or both being changed
    
    Location: rename.change(), rename.rename()96

    Parameters:
    title      (string) : if "", title isn't changed
    author     (string) : if "", author isn't changed
    new_title  (string)
    new_author (string)
    """
    if not new_title == "":
        util.p("Old Title - " + title)           #display old title
        click.echo("New Title - " + new_title)
    if not new_author == "":
        util.p("Old Author - " + author)         #display old author
        click.echo("New Author - " + new_author) #display new author

def change(author_name):
    """
    Changes the author name

    Parameters:
    author_name (string)
    """
    old_name = get_old_name(author_name)              #just in case there is multiple options
    util.p("Selected Author: " + old_name)            #print the selected author, for verifying purposes
    new_name = click.prompt("Enter New Author Name") 
    display_title_author("", old_name, "", new_name)  #display the old and new name, again for verification purposes
    if click.confirm("Confirm author change?"):
        author_id = db.get_author_id(old_name)                #get the id of the old author name
        db.rename_author(author_id, new_name)

def get_old_name(name):
    """
    Makes sure the old name exists, asks for user input if multiple potential options

    Parameter:
    name (string) : entered name

    Returns:
    name (string) : selected actual name
    """
    found_names = []
    click.echo()
    name_split = name.split(" ")
    full_authors = db.get_all_names()
    for x in name_split:
        for author in full_authors:
            names = author.lower()
            if x.lower() in names:
                if not author in found_names:
                    found_names.append(author)
            else:
                if author in found_names:
                    found_names.remove(author)
    if len(found_names) > 0:
        click.echo("Found Possibilities: "  + str(len(found_names)))
        click.echo()
        for x, author in enumerate(found_names):
            click.echo(str(x + 1) + " - " + author)
        click.echo(str(x + 2) + " - Cancel")
        click.echo()
        value = click.prompt("Option", type = click.IntRange(1, len(found_names)+1))
        if int(value) == x+2:
            sys.exit()
        else:
            name = found_names[value -1]
            return name

def rename(full_number, change_title, change_author):
    new_title = ""
    new_author = ""
    article_id = db.get_article_id(full_number)
    file_path = all_path + str(article_id) + ".pdf"
    os.startfile(file_path)
    old_title = db.get_title(article_id)
    old_author = db.get_author(full_number)
    util.p("Current Title: " + old_title)
    util.p("Current Author: " + old_author)
    if change_title:
        new_title = click.prompt("Enter New Article Title")
    if change_author:
        new_author = click.prompt("Enter New Author Name")
    display_title_author(old_title, old_author, new_title, new_author)
    if click.confirm("Confirm title and/or author change?"):
        if not new_title == "":
            db.update_title(article_id, new_title)
        if not new_author == "":
            author_id = db.get_author_id(old_author)
            db.rename_author(author_id, new_author)
