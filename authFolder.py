import os, time
from shutil import copyfile
from PyPDF2 import PdfFileReader, PdfFileWriter

base = "C:/Users/jonat/OneDrive/Documents/Jets/"
def main():
    path = base + "Authors/"
    for vol in os.listdir(base):
        if "Vol " in vol:
            p = base + vol + "/"
            for issue in os.listdir(p):
                num = issue.split(" ")[1]
                np = p + issue + "/"
                for article in os.listdir(np):
                    x = article.find(") - ")
                    aNum = article[:x]
                    fNum = num + "." + aNum
                    nArticle = article.replace(aNum + ")", fNum)
                    f = open(np + article, 'rb')
                    pdf = PdfFileReader(f)
                    info = pdf.getDocumentInfo()
                    author = info.author
                    if ">" in author:
                        print(fNum)
                        time.sleep(1000)
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
                    
