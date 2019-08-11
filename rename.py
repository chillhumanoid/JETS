import sys, os, time, subprocess, click
from pathvalidate import ValidationError, validate_filename; from shutil import copyfile
from util import p, getInfo, writeInfo

path = os.path.realpath(__file__)
path = path.replace("rename.py","")
path = path + "Articles/"

def rename(vNum, iNum, aNum, id): #had to adjust this because of fixAuthor
    fPath = path + "All/"
    aPath = path + "Authors/"
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
            if id == 0 or id == 2:
                name = click.prompt("Enter New Article Title") #gets new article title
            if id == 0 or id == 1:
                nAuth = click.prompt("Enter New Author Name")
            if id == 0 or id == 2:
                p("Old Title - " + title) #display old title
                click.echo("New Title - " + name)
            if id == 0 or id == 1:
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
                aPath = aPath + nAuth + "/"
                if not os.path.exists(aPath):
                    os.mkdir(aPath)
                os.rename(oAPath + file, aPath + file)
                if len(os.listdir(oAPath)) == 0:
                    os.rmdir(oAPath)
            else:
                i.kill()


def confirm(vNum, iNum, aNum): #displays author and title of new PDF (or given pdf, see below)
    for vol in os.listdir(base):
        if "Vol " + vNum + " " in vol:
            path = base + vol + "/"
            for issue in os.listdir(path):
                if os.path.isdir(path + issue):
                    if vNum + "." + iNum in issue:
                        nPath = path + issue +"/"
                        for article in os.listdir(nPath):
                            if article.startswith("OUT " + aNum + ") - ") or article.startswith(aNum + ") - "):
                                wPath = nPath + article
                                with open(wPath, 'rb') as f:
                                    pdf = PdfFileReader(f)
                                    info = pdf.getDocumentInfo()
                                    title = info.title
                                    author = info.author
                                    f.close()
                                print()
                                print("Article " + vNum + "." + iNum + "." + aNum)
                                if author == None:
                                    author = ""
                                print("Author: " + author)
                                if title == None:
                                    title = ""
                                print("Title: " + title)

def conf(num):
    vNum = num.split(".")[0]
    iNum = num.split(".")[1]
    aNum = num.split(".")[2]
    for vol in os.listdir(base):
        if "Vol " + vNum in vol:
            path = base + vol + "/"
            for issue in os.listdir(path):
                if os.path.isdir(path + issue):
                    if vNum + "." + iNum in issue:
                        nPath = path + issue + "/"
                        for article in os.listdir(nPath):
                            if article.startswith(aNum + ") - "):
                                wPath = nPath + article
                                with open(wPath, 'rb') as f:
                                    pdf = PdfFileReader(f)
                                    info = pdf.getDocumentInfo()
                                    title = info.title
                                    author = info.author
                                    f.close()
                                if author == None:
                                    author = ""
                                    print(num)
                                print("Author: " + author)
                                if title == None:
                                    title = ""
                                    print(num)
                                print("Title: " + title)
                                print()
