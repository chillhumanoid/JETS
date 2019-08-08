##imports
import sys, os, forceRename, re, search
from PyPDF2 import PdfFileReader, PdfFileWriter
from shutil import copyfile

##global variables
base = "C:/Users/jonat/OneDrive/Documents/Jets/All"

##functions
def main():                  #start of script
    if len(sys.argv) < 3:    # if the user only entered "jets -l"
        listAll()        #list all articles
    elif len(sys.argv) == 3:   #only correct way if not just -l
        arg = sys.argv[2]
        if "." in arg:
            vNum = arg.split(".")[0]
            iNum = arg.split(".")[1]
            listInIssue(vNum, iNum)
        else:
            vNum = arg
            listInVol(vNum)
    else:
        print()
        print("Too many arguments")
        print("Correct Usage: jets -l (1-62).(1-4)")

def listAll():
    articles = []
    for article in os.listdir(base):
        articles.append(article)
    search.printFiles(articles)

def listInVol(vNum):
    if int(vNum) >= 1 and int(vNum) <= 62:
        articles = []
        for article in os.listdir(base):
            if article.startswith(vNum + "."):
                articles.append(article)
        search.printFiles(articles)
    else:
        print()
        print("Invalid Volume")
        print("Correct Usage: jets -l (1-62)")

def listInIssue(vNum, iNum):
    if int(vNum) >= 1 and int(vNum) <=62 and int(iNum) >=1 and int(iNum) <= 4:
        articles = []
        for article in os.listdir(base):
            if article.startswith(vNum + "." + iNum + "."):
                articles.append(article)
        search.printFiles(articles)
    else:
        print()
        print("invalid volume or issue")
        print("Correct Usage: jets -l (1-62).(1-4)")


def listAuth():
    authList = []
    first = []
    last = []
    num = 0
    for vol in os.listdir(base):
        if "Vol " in vol:
            path = base + vol + "/"
            for issue in os.listdir(path):
                if os.path.isdir(path + issue):
                    nPath = path + issue + "/"
                    num = issue.split(" ")[1]
                    for article in os.listdir(nPath):
                        x = article.find(") - ")
                        aNum = article[:x]
                        fNum = num + "." + aNum
                        f = open (nPath + article, 'rb')
                        pdf = PdfFileReader(f)
                        info = pdf.getDocumentInfo()
                        author = info.author
                        if author == None:
                            print(nPath + article)
                        if author.startswith("Sung-Yul)"):
                            print(fNum)
                        else:
                            if not author in authList:
                                authList.append(author)
    for author in authList:
        if "," in author:
            authList.remove(author)
            x = author.split(",")
            for item in x:
                test = item.strip()
                if "And " in test:
                    test = test.replace("And ", "")
                if not test in authList:
                    authList.append(test)
