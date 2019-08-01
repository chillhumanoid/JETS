import sys
import os
from pathvalidate import ValidationError, validate_filename
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from shutil import copyfile
import time
base = "C:/Users/jonat/OneDrive/Documents/JETS/"

def main():
    args = sys.argv[2]
    vNum = args.split(".")[0]
    iNum = args.split(".")[1]
    aNum = args.split(".")[2]
    for vol in os.listdir(base):
        if "Vol " + vNum in vol:
            path = base + vol
            for issue in os.listdir(path):
                if vNum + "." + iNum in issue:
                    nPath = path +"/" + issue +"/"
                    for article in os.listdir(nPath):
                        if aNum + ") - " in article:
                            os.startfile(nPath + article)
                            print()
                            print("Current title: ")
                            title = ""
                            author = ""
                            with open(nPath + article, 'rb') as f:
                                pdf = PdfFileReader(f)
                                information = pdf.getDocumentInfo()
                                title = information.title
                                author = information.author
                                f.close()
                            title = title.strip()
                            print(title)
                            print()
                            name = input("Enter New Article Title: ")
                            print()
                            print("Current author: ")
                            print(author)
                            print()
                            nAuth = input("Enter New Author Name: ")
                            print("OLD TITLE: " + title)
                            print()
                            nArticle = article.replace(title, name) 
                            print("OLD AUTHOR: " + author)
                            print()
                            print()
                            print("NEW TITLE: " + name)
                            print()
                            print("NEW AUTHOR: " + nAuth)
                            print()
                            choice = input("Confirm change(y/n): ")
                            if choice == "y":
                                copyfile(nPath + article, nPath + nArticle)
                                with open(nPath + name, 'rb') as f:
                                    pdf = PdfFileReader(f)
                                    writer = PdfFileWriter()
                                    for page in range(pdf.numPages):
                                        pageObj = pdf.getPage(page)
                                        writer.addPage(pageObj)
                                    writer.addMetadata({
                                        '/Author': nAuth,
                                        '/Title': name
                                    })
                                    f.close()
                                    fout = open(nPath + nArticle, 'ab')
                                    writer.write(fout)
                                    fout.close()
                                    confirm()
                            else:
                                x = 1
def confirm():
    args = sys.argv[2]
    vNum = args.split(".")[0]
    iNum = args.split(".")[1]
    aNum = args.split(".")[2]
    for vol in os.listdir(base):
        if "Vol " + vNum in vol:
            path = base + vol
            for issue in os.listdir(path):
                if vNum + "." + iNum in issue:
                    nPath = path +"/" + issue +"/"
                    for article in os.listdir(nPath):
                        if aNum + ") - " in article:
                            wPath = nPath + article
                            with open(wPath, 'rb') as f:
                                pdf = PdfFileReader(f)
                                info = pdf.getDocumentInfo()
                                title = info.title
                                author = info.author
                                f.close()
                            print()
                            print("Author: " + author)
                            print("Title: " + title)
                            
