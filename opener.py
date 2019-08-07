import os, sys, subprocess

base = "C:/Users/jonat/OneDrive/Documents/Jets/"

def getArgs():
    num = sys.argv[2]
    if num.count(".") == 2:
        vNum = num.split(".")[0]
        iNum = num.split(".")[1]
        aNum = num.split(".")[2]
        main(vNum, iNum, aNum, num)
    else:
        mainAuth(num)
        
def main(vNum, iNum, aNum, num):
    if int(vNum) >= 1 and int(vNum) <= 62:
        if int(iNum) >= 1 and int(iNum) <= 4:
            openFile(num)
        else:
            print()
            print("Index Number out of Range")
            print("Correct Usage: jets -o (1-62).(1-4).(##) or author")
    else:
        print()
        print("Volume number out of Range")
        print("Correct Usage: jets -o (1-62).(1-4).(##)")
def mainAuth(num):
    aPaths = []
    aTitles = []
    for author in os.listdir(base + "Authors/"):
        if num in author:
            for article in os.listdir(base + "Authors/" + author):
                aTitles.append(article)
                aPaths.append(base + "Authors/" + author + "/" + article)
    if len(aTitles) > 0:
        for title in aTitles:
            print(title)
        print()
        confirm = input("Open All? (y/n): ")
        if confirm.lower() == "y":
            for path in aPaths:
                os.startfile(path)
        else:
            sys.exit()
    else:
        print("Author Not Found")
        
def openFile(num):
    path = base + "All/" 
    x = 0
    for article in os.listdir(path):
        if num in article:
            os.startfile(path + article)
            x = x + 1
    if x == 0:
        print("Article Not Found")
