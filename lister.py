##imports
import sys, os, forceRename
from PyPDF2 import PdfFileReader, PdfFileWriter
import re

##global variables
base = "C:/Users/jonat/OneDrive/Documents/Jets/"

##functions
def main():                  #start of script
    if len(sys.argv) < 3:    # if the user only entered "jets -l"
        listVolumes()        #list all volumes
    elif sys.argv[2] == "-v":   #only correct way if not just -l
        if len(sys.argv) < 4:   #if -v but no number
            print()             
            print("Correct Usage: jets -l -v (1-62)")
        else:
            num = sys.argv[3] #get number
            if len(num) == 2: #if they had a leading 0
                s = num[0:1] 
                if s == "0":
                    num = num[1:] #gets rid of leading 0
            if len(sys.argv) > 4: #if they had more than just -v 
                if sys.argv[4] == "-i": #if it's -i (only correct argument)
                    if len(sys.argv) < 6 or len(sys.argv) > 6: #if less than 6, or greater than 6
                        print()
                        print("Correct Usage: jets -l -v (1-62) -i (1-4)")  
                    else:
                        iNum = int(sys.argv[5]) #sets issue number
                        if iNum > 0 and iNum < 5: #if this issue number is between 1-4
                            num = str(num) + "." + str(iNum) #reconstruct number, may not be necessary
                            listArticles(num)  #list articles
                        else:
                            print()
                            print("Correct Usage: jets -l -v (1-62) -i (1-4)")
                else: #if not -i
                    print()
                    print("Correct Usage: jets -l -v (1-62) -i (1-4)")
            else:
                listIssues(num) #display issues if only -v argument
    elif sys.argv[2] == "-a":
        listAuth()
    else:
        print("Correct Usage: jets -l -v (1-62)")
        
def listVolumes():
    print() #blank for formatting
    for vol in os.listdir(base):
        if "Vol " in vol:  #rules out "all" and "authors"
            print(vol) #displays all volumes

def listIssues(num):
    print()
    for vol in os.listdir(base):
        if "Vol " + num + " " in vol:
            path = base + vol
            for issue in os.listdir(path):
                nPath = path + "/" + issue + "/"
                for aNum in range(len(os.listdir(nPath))+1):
                    front = issue.split(" ")[1]
                    num = front + "." + str(aNum)
                    forceRename.conf(num)
                
def listArticles(num):
    print()
    vNum = num.split(".")[0]
    iNum = num.split(".")[1]
    for vol in os.listdir(base):
        if "Vol " + vNum + " (" in vol:
            path = base + vol + "/"
            for issue in os.listdir(path):
                if " " + num in issue:
                    nPath = path + issue + "/" 
                    for aNum in range(len(os.listdir(nPath))):
                        print(aNum)


def listAuth():
    authList = []
    first = []
    last = []
    num = 0
    for vol in os.listdir(base):
        if "Vol " in vol:
            path = base + vol + "/"
            for issue in os.listdir(path):
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
    
