import os
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter

base = "C:/Users/jonat/OneDrive/Documents/JETS/"

def main():
    vNum = "0"
    iNum = "0"
    if len(sys.argv) == 3:
        arg = sys.argv[2]
        if arg.count(".") == 2:
            print()
            print("Can't merge one article")
            print("Correct usage: jets -m (1-62).(1-4)")
        elif arg.count(".") == 1:
            vNum = arg.split(".")[0]
            iNum = arg.split(".")[1]
        elif arg.count(".") == 0:
            vNum = arg
        if vNum.isdigit() and iNum.isdigit():
            if int(vNum) >= 1 and int(vNum) <= 62 or int(iNum) >= 0 and int(iNum) <= 4:
                merge(vNum, iNum)
            else:
                print()
                print("volume or issue invalid")
                print("correct usage: jets -m (1-62).(1-4)")
                
        else:
            print()
            print("Make sure volume, issue and article are numbers")
            print("Correct usage: jets -m (1-62).(1-4)")
    elif len(sys.argv) == 2:
        merge("0","0")
    else:
        print()
        print("too many arguments")
        print("Correct Usage: jets -m (1-62).(1-4)")

def merge(vNum, iNum):
    for vol in os.listdir(base):
        if vol.startswith("Vol " + vNum + " ") or vNum == "0" and vol.startswith("Vol "):
            path = base + vol + "/"
            for issue in os.listdir(path):
                if os.path.isdir(path + issue):
                    if iNum == "0":
                        nPath = path + issue + "/"
                        mergeIssue(vol, issue, nPath)
                    elif vNum + "." + iNum in issue:
                        nPath = path + issue + "/"
                        mergeIssue(vol, issue, nPath)
    mergeVol(vNum, iNum)
    
def mergeVol(vNum, iNum):
    for vol in os.listdir(base):
        if vol.startswith("Vol " + vNum + " ") or vNum == "0" and vol.startswith("Vol "):
            path = base + vol + "/"
            fout = open(path + vol + ".pdf",'ab')
            writer = PdfFileWriter()
            for issue in os.listdir(path):
                if not os.path.isdir(path + issue) and not vol + ".pdf" == issue: 
                    f = open(path + issue, 'rb')
                    pdf = PdfFileReader(f)
                    for page in range(pdf.getNumPages()):
                        writer.addPage(pdf.getPage(page))
                    writer.write(fout)
                    f.close()
            fout.close()
                    
                
def mergeIssue(vol, issue, nPath):
    iPath = base + vol + "/"
    fout = open(iPath + issue + ".pdf", 'ab')
    writer = PdfFileWriter()
    for article in os.listdir(nPath):
        if not os.path.exists(nPath + article):
            f = open(nPath + article, 'rb')
            pdf = PdfFileReader(f)
            for page in range(pdf.getNumPages()):
                writer.addPage(pdf.getPage(page))
            writer.write(fout)
            f.close()
    fout.close()
        
        
