import sys
import os
from pathvalidate import ValidationError, validate_filename
from PyPDF2 import PdfFileReader, PdfFileWriter
from shutil import copyfile

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
                            name = input("Enter New Article Title: ")
                            print("NEW NAME: " + name)
                            print("Current author: ")
                            print(author)
                            nAuth = input("Enter New Author Name: ")
                            print("OLD TITLE: " + article)
                            name = article.replace(title, name)
                            print("OLD AUTHOR: " + author)
                            print("NEW TITLE: " + name)
                            print("NEW AUTHOR: " + nAuth)
                            choice = input("Confirm change(y/n): ")
                            if choice == "y":
                                copyfile(nPath + article, nPath + name)
                                with open(nPath + name, 'rb') as f:
                                    pdf = PdfFileReader(f)
                                    writer = PdfFileWriter()
                                    writer.appendPagesFromReader(pdf)
                                    writer.addMetadata({
                                        '/Author': nAuth,
                                        '/Title': name
                                    })
                                    fout = open(curPath, 'ab')
                                    writer.write(fout)
                                    f.close()
                            else:
                                x = 1
                            
                            
                            
