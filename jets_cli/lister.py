##imports
import sys, os, re
from jets_cli import search
from PyPDF2 import PdfFileReader, PdfFileWriter
from shutil import copyfile
numbers = re.compile(r'(\d+)')
##global variables
path = os.path.realpath(__file__)
path = path.replace("lister.py","")
path = path + "Articles/"

def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
##functions
def listing(vNum, iNum):
    if vNum == 0 and iNum == 0:
        listAll()
    if not vNum == 0 and iNum == 0:
        listInVol(vNum)
    if not vNum == 0 and not iNum == 0:
        listInIssue(vNum, iNum)

def listAll():
    articles = []
    for article in os.listdir(path + "All/"):
        articles.append(article)
    for file in sorted(glob.glob(articles), key=numericalSort):
        print(article)

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
