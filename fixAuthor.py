import sys, os
import forceRename
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
        if "." in arg1:
            vNum = arg1.split(".")[0]
            iNum = arg1.split(".")[1]
        else:
            vNum = arg1
            iNum = 0
        if int(vNum) >= 1 and int(vNum) <= 62 and int(iNum) >= 0 and int(iNum) <= 4:
            fix(vNum, iNum)
            confirmNew(vNum, iNum)
        else:
            print("Correct Usage: jets -f (1-62).(1-4)")
    else:
        print("Correct Usage: jets -f (1-62).(1-4)")
        
def fix(vNum, iNum):
    global curPath
    global curIssue
    global curVol
    for vol in os.listdir(base):
        curVol = vol
        if "Vol " + vNum + " " in vol: #gets correct volume
            curPath = base + vol + "/"
            if iNum == 0:
                    for issue in os.listdir(curPath):
                        if os.path.isdir(curPath + issue):
                            t = issue.split(" ")[1]
                            iNum = t.split(".")[1]
                            curIssue = issue
                            curPath = base + vol + "/" + issue + "/" #keep this way to avoid "errors"
                            for article in os.listdir(curPath):
                                if not article.startswith("OUT "):
                                    author = getAuthor(article, vNum, iNum)
                                    if not author == 0:
                                        titles = getTitle(article)
                                        nTitle = titles[0]
                                        oTitle = titles[1]
                                        output = getOutput(article, oTitle, nTitle)
                                        setMetaData(nTitle, author, output, article)
            else:
                for issue in os.listdir(curPath):
                    if os.path.isdir(curPath + issue):
                        if vNum + "." + iNum in issue:
                            curIssue = issue
                            curPath = base + vol + "/" + issue + "/"
                            for article in os.listdir(curPath):
                                if not article.startswith("OUT "):
                                    author = getAuthor(article,vNum, iNum)
                                    if not author == 0:
                                        titles = getTitle(article)
                                        nTitle = titles[0]
                                        oTitle = titles[1]
                                        output = getOutput(article, oTitle, nTitle)
                                        setMetaData(nTitle, author, output, article)

    
def getAuthor(article,vNum, iNum): #gets the author name)
    x = article.find("(") + 1 #hold
    e = article.find(")")
    aNum = article[:e]
    if not x == 0:
        count = article.count("(")
        if count > 1:
            forceRename.main(vNum, iNum, aNum) #instead of trying to do this automagically
            return 0
        else:
            y = article.find(")", x + 1)

            author = article[x:y]
            author = author.strip()
            
            if author.endswith(" "):
                author.strip()
            if author.endswith("."):
                author = author[:-1]
                
            try:
                validate_filename(author)
                validate_filename(article)
            except ValidationError as e:
                print()
                print("{}\n".format(e), file=sys.stderr)
            else:
                return author
    else:
        author = "JETS"
        return author

def getTitle(article):
    count = article.count("(")
    x = article.find(") - ") + 4
    if count > 0:
        y = article.find("(")
        new = article[x:y]
    else:
        y = article.find(".pdf")
        new = article[x:y]
    z = article.find(".pdf")
    old = article[x:z]
    data = (new, old)
    return(data)

def getOutput(article, otitle, ntitle):
    output = article.replace(otitle, ntitle)
    output = "OUT " + output
    try:
        validate_filename(output)
    except ValidationError as e:
        print("{}\n".format(e), file=sys.stderr)
    return output
    
def setMetaData(title, author, output, article):
    f = open(curPath + article, 'rb')
    pdf = PdfFileReader(f)
    writer = PdfFileWriter()
    writer.appendPagesFromReader(pdf)
    writer.addMetadata({
        '/Author': author,
        '/Title': title
    })
    fout = open(curPath + output, 'ab')
    writer.write(fout)
    fout.close()
    f.close()

def confirmNew(vNum, iNum):
    for vol in os.listdir(base):
        curVol = vol
        if "Vol " + vNum + " " in vol: #gets correct volume
            path = base + vol + "/"
            if iNum == 0:
                for issue in os.listdir(path):
                    if os.path.isdir(path + issue):
                        iNum = issue.split(" ")[1]
                        iNum = iNum.split(".")[1]
                        curIssue = issue
                        nPath = base + vol + "/" + issue + "/" #keep this way to avoid "errors"
                        for article in os.listdir(nPath):
                            if article.startswith("OUT "):
                                x = article.find("T ")+2
                                y = article.find(") - ")
                                aNum = article[x:y]
                                with open(nPath + article, 'rb') as f:
                                    pdf = PdfFileReader(f)
                                    info = pdf.getDocumentInfo()
                                    author = info.author
                                    if author == None:
                                        author = ""
                                    title = info.title
                                    if title == None:
                                        title = ""
                                    print()
                                    print(str(vNum) + "." + str(iNum) + "." + str(aNum))
                                    print("AUTHOR: " + author)
                                    print("TITLE: " + title)
                                    f.close()
            else:
                for issue in os.listdir(path):
                    if os.path.isdir(path + issue):
                        if vNum + "." + iNum in issue:
                            curIssue = issue
                            nPath = base + vol + "/" + issue + "/"
                            for article in os.listdir(nPath):
                                if article.startwith("OUT "):
                                    x = article.find("T ") + 2
                                    y = article.find(") -")
                                    aNum = article[x:y]
                                    with open(nPath + article, 'rb') as f:
                                        pdf = PdfFileReader(f)
                                        info = pdf.getDocumentInfo()
                                        author = info.author
                                        if author == None:
                                            author = ""
                                        title = info.title
                                        if title == None:
                                            title = ""
                                        print()
                                        print(str(vNum) + "." + str(iNum) + "." + str(aNum))
                                        print("AUTHOR: " + author)
                                        print("TITLE: " + title)
                                        f.close()

