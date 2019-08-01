import sys
import os
from pathvalidate import ValidationError, validate_filename
from PyPDF2 import PdfFileReader, PdfFileWriter
from shutil import copyfile

base = "C:/Users/jonat/OneDrive/Documents/JETS/"
curPath = ""
curIssue = ""
curVol = ""
def main():    #Main file. going to go about this a different way this time
    length = len(sys.argv)
    if length > 2:
        arg1 = sys.argv[2]
        if int(arg1) >= 1 and int(arg1) <= 62:
            data = arg1
            startfix(arg1)
        else:
            print("Correct Usage: jets -f (1-62)")
    else:
        print("Correct Usage: jets -f (1-62)")

def startfix(data):
    global curPath
    global curIssue
    global curVol
    for vol in os.listdir(base):
        curVol = vol
        if "Vol " + data + " " in vol:
            curPath = base + vol + "/"
            for issue in os.listdir(curPath):
                curIssue = issue
                curPath = base + vol + "/" + issue #keep this way to avoid "errors"
                for article in os.listdir(curPath):
                    curPath = base + vol + "/" + issue + "/" + article
                    getName(article)
                    

def getName(article):
    x = article.find("(") + 1
    if not x == 0:
        count = article.count("(")
        if count == 2 and article.count(")") == 3:
            x = article.find("(", x) + 1
        elif count == 3 and article.count(")") == 4:
            x = article.find("(", x) + 1
            x = article.find("(", x) + 1
        y = article.find(").", x)
        author = article[x:y]
        try:
            validate_filename(author)
            validate_filename(article)
        except ValidationError as e:
            print("{}\n".format(e), file=sys.stderr)
        path = base + "Authors/" + author + "/"
        pdfMetaData(article, author)
        nArt = changeArticleName(article)
        global curPath
        curPath = curPath.replace(article, nArt)
        x = nArt.find(") - ")
        aNum = nArt[:x]
        pNum = curIssue.split(" ")[1]
        fNum = pNum + "." + aNum
        if not os.path.exists(path):
            print(fNum)
        nArt = nArt.replace(aNum + ")", fNum)
        
        #copyfile(curPath, path + nArt)
    else:
        with open(curPath, 'rb') as f:
            pdf = PdfFileReader(f)
            information = pdf.getDocumentInfo()
            author = information.author
            x = article.find(") - ")
            aNum = article[:x]
            pNum = curIssue.split(" ")[1] #stands for pre-number
            fNum = pNum + "." + aNum      #Full Number
            article = article.replace(aNum + ")", fNum)
            if not author == None:
                path = base + "Authors/" + author + "/"
                if not os.path.exists(path):
                    print(fNum)
                copyfile(curPath, path + article)
            
        
def pdfMetaData(article, author):
    st = article.find(") - ") + 4
    end = article.find("(" + author)
    title = article[st:end-1]
    with open(curPath, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        writer = PdfFileWriter()
        writer.appendPagesFromReader(pdf)
        metadata = pdf.getDocumentInfo()
        writer.addMetadata({
            '/Author': author,
            '/Title': title
        })

        fout = open(curPath, 'ab')
        writer.write(fout)
        f.close()
        
def changeArticleName(article):
    count = article.count("(")
    x = article.find("(")
    if count == 2 and article.count(")") > count:
        x = article.find("(", x + 1)
    elif count == 3 and article.count(")") > count:
        x = article.find("(", x + 1)
        x = article.find("(", x + 1)
    x = x -1
    
    nArticle = article[:x] + ".pdf"
    nPath = curPath.replace(article, nArticle)
    print("Confirm change:")
    print("OLD: " + curPath)
    print("NEW: " + nPath)
    choice = input("Confirm?(Y/N): ")
    choice = choice.lower()
    if choice == 'y':
        os.rename(curPath, nPath)
        print("Name Changed")
        print()
    else:
        print()
        print("Okay")
        print()
    return nArticle
    
