import sys, os, time, subprocess, click, database
from pathvalidate import ValidationError, validate_filename; from shutil import copyfile, move
import util
path = os.path.realpath(__file__)
path = path.replace("rename.py","")
path = path + "Articles/"
all_path = path + "All/"
author_path = path + "Authors/"

def prompt(title, author, new_title, new_author):
    if not new_title == "":
        util.p("Old Title - " + title) #display old title
        click.echo("New Title - " + new_title)
    if not new_author == "":
        util.p("Old Author - " + author) #display old author
        click.echo("New Author - " + new_author) #display new author

def change(name):
    old_name = get_old_name(name)
    util.p("Selected Author: " + old_name)
    new_name = click.prompt("Enter New Author Name")
    prompt("", old_name, "", new_name)
    if click.confirm("Confirm author change?"):
        id = database.get_id(old_name)
        database.rename_author(id, new_name)


def get_old_name(name):
    found_names = []
    click.echo()
    name_split = name.split(" ")
    full_authors = database.get_names()
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

def rename(full_num, change_title, change_author):
    new_title = ""
    new_author = ""
    for file in os.listdir(all_path):
        if file.startswith(full_num):
            file_path = all_path + file
            acrobat_path = r'C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat\Acrobat.exe'
            process = subprocess.Popen("%s %s" % (acrobat_path, file_path))
            info = util.get_info(file_path)
            title = info[0]
            author = info[1]
            if not title == None: #if the file has a title
               title = util.string_strip(title) #get rid of any whitespace
            else:
               title = "" #if it doesn't have a title set it to "" because otherwise error
            if author == None: #if the article doesn't have an author, set it to "" because otehrwise error
               author = ""
            util.p("Current Title: " + title)
            click.echo("Current Author: " + author)
            if change_title:
                new_title = click.prompt("Enter New Article Title") #gets new article title
            if change_author:
                new_author = click.prompt("Enter New Author Name")

            prompt(title, author, new_title, new_author)

            if click.confirm("Confirm title and/or author change?"): #confirm
                process.terminate()
                time.sleep(.5) #allow adobe to close
                if new_title == "":
                    new_title = title
                if new_author == "":
                    new_author = author

                util.write_info(all_path + file, new_title, new_author)
                database.rename_author(author, new_author)
                
            else:
                process.kill()
