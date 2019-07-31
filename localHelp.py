import os
import time
import textwrap
import issues
from shutil import copyfile
import renamer
import sys
import re

from pathvalidate import ValidationError, validate_filename
base = "C:/Users/jonat/OneDrive/Documents/JETS/"
searching = False


def newArticleName(article):
    articleNum = articleNumberGenerator(article)
    x = article.find(")")
    curArtPrefix = article[:x + 1]
    newArticle = article.replace(curArtPrefix, articleNum)
    return newArticle
def articleNumberGenerator(article):
    issueNum = curIssue.split(" ")[1]
    articleNum = article.split(")")[0]
    articleNum = issueNum + "." + articleNum
    return articleNum
    #print(issueNum + "." + articleNum)
def authFolderCreator():
    global authList
    for auth in authList:
        print(auth)
def authListGenerator(article):
    path = base + "Authors/"
    current = curPath + article
    global authList
    auth = nameGetter(article)
    if not auth == None:
        newArt = newArticleName(article)
        if " And " in auth:
            multi = auth.split(" And ")
            for potential in multi:
                if "," in potential:
                    second = potential.split(", ")
                    for ne in second:
                        if ne.endswith(","):
                            fin = ne[:-1]
                            if fin in authList:
                                new = path + fin + "/" + newArt
                                if not os.path.exists(new):
                                    copyfile(current, new)
                            else:
                                new = path + fin + "/" + newArt
                                if not os.path.exists(path + fin):
                                    os.mkdir(path + fin)
                                if not os.path.exists(new):
                                    copyfile(current, new)
                                authList.append(fin)
                        else:
                            if ne in authList:
                                new = path + ne + "/" + newArt
                                if not os.path.exists(new):
                                    copyfile(current,new)
                            else:
                                new = path + ne + "/" + newArt
                                if not os.path.exists(path+ne):
                                    os.mkdir(path + ne)
                                if not os.path.exists(new):
                                    copyfile(current, new)
                                authList.append(ne)
                else:
                    if potential in authList:
                        new = path + potential + "/" + newArt
                        if not os.path.exists(new):
                            copyfile(current, new)
                    else:
                        new = path + potential + "/" + newArt
                        if not os.path.exists(path + potential):
                            os.mkdir(path + potential)
                        if not os.path.exists(new):
                            copyfile(current, new)
                        authList.append(potential)
        elif " With " in auth:
            multi = auth.split(" With ")
            for aut in multi:
                if aut in authList:
                    new = path + aut + "/" + newArt
                    if not os.path.exists(new):
                        copyfile(current, new)
                else:
                    new = path + aut + "/" + newArt
                    if not os.path.exists(path + aut):
                        os.mkdir(path + aut)
                    if not os.path.exists(new):
                        copyfile(current, new)
                    authList.append(aut)
        else:
            if auth in authList:
                new = path + auth + "/" + newArt
                if not os.path.exists(new):
                    copyfile(current, new)
            else:
                new = path + auth + "/" + newArt
                if not os.path.exists(path + auth):
                    os.mkdir(path + auth)
                if not os.path.exists(new):
                    copyfile(current, new)
                authList.append(auth)
def getAuthors():
    path = base + "All/"
    authList = []
    for file in os.listdir(path):
        if "(" in file:
            e = file.count("(")
            if e == 2:
                index = 0
                for t in range(2):
                    x = file.find("(", index) + 1
                    index = x
                #print(file)
            elif e == 3:
                index = 0
                for t in range(3):
                    x = file.find("(", index) + 1
                    index = x
            else:
                x = file.find("(") + 1
            y = file.find(".pdf") -1
            author = file[x:y]
            author = author.upper()
            if author[0] == " ":
                author = author.replace(" ", "", 1)
            nPath = base + "Authors/"
            if " AND " in author:
                authors = author.split(" AND ")
                for author in authors:
                    lPath = nPath + author + "/"
                    if not os.path.exists(lPath):
                        os.mkdir(lPath)
                    if not os.path.exists(lPath + file):
                        copyfile(path + file, lPath + file)
            else:
                lPath = nPath + author + "/"
                if not os.path.exists(lPath):
                    os.mkdir(lPath)
                if not os.path.exists(lPath + file):
                    copyfile(path + file, lPath + file)
    for a in os.listdir(base + "Authors/"):
        p = base + "Authors/" + a + "/"
        count = len(os.listdir(p))
        print(a + " - " + str(count))
def search(searchTerm, curDirectory):
    x = 0
    for folder in os.listdir(base):
        if "Vol " in folder:
            nPath = base + folder + "/"
            for issue in os.listdir(nPath):
                nnPath = nPath + issue + "/"
                for file in os.listdir(nnPath):
                    term = searchTerm.lower()
                    file = file.lower()
                    if term in file:
                        aNum = file.split(")")[0]
                        title = file.split(") - ")[1]
                        vNum = folder.split(" ")[1]
                        iNum = issue.split(".")[1]
                        print()
                        print(vNum + "." + iNum + "." + aNum + " " + title)
                        x = x + 1
                    else:
                        y = 0 #do nothing
    if x > 0:
        import jets
        print()
        jets_web.menu(curDirectory)
    else:
        import jets
        print()
        print("File Not Found")
        print()
        jets_web.menu(curDirectory)

curFileName = ""
curVol = ""
curIssue = ""
curPath = ""
authLists = []
authList = []
