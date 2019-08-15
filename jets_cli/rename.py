import sys, os, time, subprocess, click
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
        change_name(old_name, new_name)


def change_name(old_name, new_name):
    old_author_path = author_path + old_name + "/" #get the specific path to the old author name
    new_author_path = author_path + new_name + "/"
    if not os.path.exists(new_author_path):
        os.mkdir(new_author_path)
    for article in os.listdir(old_author_path): #every file in old author directory
        title = util.get_info(old_author_path + article)[0] #get the title for given article
        util.write_info(old_author_path + article, title, new_name) #move the file
        move(old_author_path + article, new_author_path + article) #move the given file
        if len(os.listdir(old_author_path)) == 0:  #if the old author path is empty
            os.rmdir(old_author_path)  #delete that sucker
        full_num = util.get_nums(article)[0] #get the number for the given artictles
        for article in os.listdir(all_path):
            if article.startswith(full_num):
                util.write_info(all_path + article, title, new_name)

def get_old_name(name):
    found_names = []
    click.echo()
    name_split = name.split(" ")
    for x in name_split:
        for author in os.listdir(author_path):
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
                old_author_path = author_path + author + "/"
                new_author_path = author_path + new_author + "/"
                if not os.path.exists(new_author_path):
                    os.mkdir(new_author_path)
                move(old_author_path + file, new_author_path + file)
                if len(os.listdir(old_author_path)) == 0:
                    os.rmdir(old_author_path)
            else:
                process.kill()
