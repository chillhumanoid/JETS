import sys, os, time, subprocess, click
from pathvalidate import ValidationError, validate_filename; from shutil import copyfile, move
from util import p, getInfo, writeInfo, check_digit
path = os.path.realpath(__file__)
path = path.replace("rename.py","")
path = path + "Articles/"
fPath = path + "All/"
aPath = path + "Authors/"

def rename(vNum, iNum, aNum, id): #had to adjust this because of fixAuthor
    global aPath
    vNum = check_digit(vNum)
    iNum = check_digit(iNum)
    aNum = check_digit(aNum)
    num = vNum + "." + iNum + "." + aNum
    name = ""
    nAuth = ""
    for file in os.listdir(fPath):
        if file.startswith(num):
            acrobatPath = r'C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat\Acrobat.exe'
            i = subprocess.Popen("%s %s" % (acrobatPath, fPath + file))
            info = getInfo(fPath + file)
            title = info.title #gets the title
            author = info.author #gets the author
            if not title == None: #if the file has a title
               title = title.strip() #get rid of any whitespace
            else:
               title = "" #if it doesn't have a title set it to "" because otherwise error
            if author == None: #if the article doesn't have an author, set it to "" because otehrwise error
               author = ""
            p("Current Title: " + title)
            click.echo("Current Author: " + author)
            if id == 0 or id == 2 or id == 3:
                name = click.prompt("Enter New Article Title") #gets new article title
            if id == 0 or id == 1 or id == 3:
                nAuth = click.prompt("Enter New Author Name")
            if id == 0 or id == 2 or id == 3:
                p("Old Title - " + title) #display old title
                click.echo("New Title - " + name)
            if id == 0 or id == 1 or id == 3:
                p("Old Author - " + author) #display old author
                click.echo("New Author - " + nAuth) #display new author
            if click.confirm("Confirm title and/or author change?"): #confirm
                i.kill()
                time.sleep(.5)
                if name == "":
                    name = title
                if nAuth == "":
                    nAuth = author
                writeInfo(fPath + file, name, nAuth)
                oAPath = aPath + author + "/"
                nAPath = aPath + nAuth + "/"
                if not os.path.exists(nAPath):
                    os.mkdir(nAPath)
                move(oAPath + file, nAPath + file)
                if len(os.listdir(oAPath)) == 0:
                    os.rmdir(oAPath)
            else:
                i.kill()
