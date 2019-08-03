import os, time, sys
from shutil import copyfile
from PyPDF2 import PdfFileReader, PdfFileWriter

base = "C:/Users/jonat/OneDrive/Documents/Jets/"

def main():
    if len(sys.argv) == 3:
        arg = sys.argv[2]
        if arg.count(".") == 2:
            vNum = arg.split(".")[0]
            iNum = arg.split(".")[1]
            aNum = arg.split(".")[2]
            if vNum.isdigit() and iNum.isdigit() and aNum.isdigit():
                if int(vNum) >= 1 and int(vNum) <= 62 and int(iNum) >= 1 and int(iNum) <= 4:
                        createFolders(vNum, iNum, aNum)
                else:
                    print()
                    print("incorrect volume or issue number")
                    print("Correct Usage: jets -ca (1-62).(1-4).##")
            else:
                print()
                print("Volume/Issue/Article needs to be a number")
                print("Correct Usage: jets -ca (1-62).(1-4).##")
        elif arg.count(".") == 1:
            vNum = arg.split(".")[0]
            iNum = arg.split(".")[1]
            if vNum.isdigit() and iNum.isdigit():
                if int(vNum) >= 1 and int(vNum) <= 62 and int(iNum) >= 1 and int(iNum) <= 4:
                        createFolders(vNum, iNum, 0)
                else:
                    print()
                    print("incorrect volume or issue number")
                    print("Correct Usage: jets -ca (1-62).(1-4)")
            else:
                print()
                print("Volume/Issue needs to be a number")
                print("Correct Usage: jets -ca (1-62).(1-4)")
        elif arg.count(".") == 0:
            vNum = arg
            if vNum.isdigit():
                if int(vNum) >= 1 and int(vNum) <= 62:
                    createFolders(vNum, 0, 0)
                else:
                    print()
                    print("incorrect volume number")
                    print("Correct Usage: jets -ca (1-62)")
            else:
                print()
                print("Volume needs to be a number")
                print("Correct Usage: jets -ca (1-62)")
        else:
            print()
            print("Incorrect Argument")
            print("Correct Usage: jets -ca (1-62).(1-4).##")
    elif len(sys.argv) == 2:
        createFolders(0,0,0)
    else:
        print()
        print("Too many arguments")
        print("Correct Usage: jets -ca (1-62).(1-4).##")
def createFolders(vNum, iNum, aNum):
    path = base + "Authors/"
    x = 0
    for vol in os.listdir(base):
        if "Vol " + vNum + " " in vol or vNum == 0:
            p = base + vol + "/"
            for issue in os.listdir(p):
                if vNum + "." + iNum in issue or iNum == 0:
                    num = issue.split(" ")[1]
                    np = p + issue + "/"
                    for article in os.listdir(np):
                        if article.startswith(aNum + ") - ") or aNum == 0:
                            aNum2 = article.split(") - ")[0]
                            fNum = num + "." + aNum2
                            nArticle = article.replace(aNum2 + ")", fNum)
                            f = open(np + article, 'rb')
                            pdf = PdfFileReader(f)
                            info = pdf.getDocumentInfo()
                            author = info.author
                            if "," in author:
                                x = author.split(",")
                                for item in x:
                                    author = item.strip()
                                    if "And " in author:
                                        author = author.replace("And ", "")
                                        nPath = path + author + "/"
                                        if not os.path.exists(nPath):
                                            os.mkdir(nPath)
                                        copyfile(np + article, nPath + nArticle)
                                    else:
                                        nPath = path + author + "/"
                                        if not os.path.exists(nPath):
                                            os.mkdir(nPath)
                                        copyfile(np + article, nPath + nArticle)
                            else:
                                nPath = path + author + "/"
                                if not os.path.exists(nPath):
                                    os.mkdir(nPath)
                                copyfile(np + article, nPath + nArticle)
                            x = x + 1
    if x == 0:
        print()
        print("No article found")
                    
