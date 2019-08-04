import os
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter
from shutil import copyfile

base = "C:/Users/jonat/OneDrive/Documents/Jets/"

def main():
    for vol in os.listdir(base):
        if vol.startswith("Vol "):
            path = base + vol + "/"
            for issue in os.listdir(path):
                if os.path.isdir(path + issue):
                    nPath = path + issue + "/"
                    for article in os.listdir(nPath):
                        if article.startswith("OUT "):
                        
                            nName = article.replace("OUT ", "")
                            nName = nName.replace(".pdf", "")
                            if nName.endswith(" "):
                                nName = nName.strip()
                            nName = nName + ".pdf"
                            print(nName)
                            start = issue.split(" ")[1]
                            aNum = nName.split(") - ")[0]
                            fNum = start + "." + aNum
                            os.replace(nPath + article, nPath + nName)
                            location = nPath + nName
                            f = open(location, 'rb')
                            pdf = PdfFileReader(f)
                            info = pdf.getDocumentInfo()
                            author = info.author
                            f.close()
                            fixAllAuthor(fNum, location, author)
                        else:
                            if ").pdf" in article:
                                os.remove(nPath + article)
                            
def fixAllAuthor(fNum, location, author):
    path1 = base + "Authors/"
    path2 = base + "All/"
    for auth in os.listdir(path1):
        nPath1 = path1 + auth + "/"
        for article in os.listdir(nPath1):
            if article.startswith(fNum):
                os.remove(nPath1 + article)
                nnPath1 = path1 + author + "/"
                if not os.path.exists(nnPath1):
                    os.mkdir(nnPath1)
                copyfile(location, nnPath1 + article)

