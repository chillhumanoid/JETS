import os, sys
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter
path = os.path.realpath(__file__)
path = path.replace("merge.py","")
path = path + "Articles/"
fPath = path + "All/"
mPath = path + "Merged/"

def merge(vNum, iNum):
    folder = "Vol " + vNum +"/"
    if iNum == "0":
        issues = []
        for file in os.listdir(fPath):
            if file.startswith(vNum + "."):
                title = file.split(" - ", 1)[0]
                num = title.split(".")[1]
                issues.append(num)
        for iNum in issues:
            mergeIssue(vNum, iNum)
        mergeVol(vNum)
    else:
        mergeIssue(vNum, iNum)

def mergeIssue(vNum, iNum):
    vPath = mPath + "Vol " + vNum + "/"
    if not os.path.exists(vPath):
        os.mkdir(vPath)
    out = vPath + "Issue " + str(iNum) + ".pdf"
    fout = open(out, 'ab')
    writer = PdfFileWriter()
    for article in os.listdir(fPath):
        if article.startswith(vNum + "." + iNum):
            f = open(fPath + article, 'rb')
            pdf = PdfFileReader(f)
            for page in range(pdf.getNumPages()):
                writer.addPage(pdf.getPage(page))
            writer.write(fout)
            f.close()
    fout.close()

def mergeVol(vNum):
    for folders in os.listdir(mPath):
        if folders == "Vol " + vNum:
            out = mPath + folders + "/" + "Vol " + vNum + ".pdf"
            fout = open(out, 'ab')
            writer = PdfFileWriter()
            for file in os.listdir(mPath + folders):
                f = open(mPath + folders + "/" + file, 'rb')
                pdf = PdfFileReader(f)
                for page in range(pdf.getNumPages()):
                    writer.addPage(pdf.getPage(page))
                writer.write(fout)
                f.close()
            fout.close()
