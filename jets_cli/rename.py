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
