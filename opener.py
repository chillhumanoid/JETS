import os, sys

base = "C:/Users/jonat/OneDrive/Documents/Jets/"

def getArgs():
    num = sys.argv[2]
    if num.count(".") == 2:
        vNum = num.split(".")[0]
        iNum = num.split(".")[1]
        aNum = num.split(".")[2]
        main(vNum, iNum, aNum)
    else:
        print()
        print("Insufficent arguments")
        print("Correct Usage: jets -o (1-62).(1-4).(##)")
def main(vNum, iNum, aNum):
    if int(vNum) >= 1 and int(vNum) <= 62:
        if int(iNum) >= 1 and int(iNum) <= 4:
            openFile(vNum, iNum, aNum)
        else:
            print()
            print("Index Number out of Range")
            print("Correct Usage: jets -o (1-62).(1-4).(##)")
    else:
        print()
        print("Volume number out of Range")
        print("Correct Usage: jets -o (1-62).(1-4).(##)")

def openFile(vNum, iNum, aNum):
    for vol in os.listdir(base):
        if "Vol " + vNum + " " in vol:
            path = base + vol + "/"
            for issue in os.listdir(path):
                if " " + vNum + "." + iNum in issue:
                    nPath = path + issue + "/"
                    for article in os.listdir(nPath):
                        if article.startswith(aNum + ") - "):
                            os.startfile(nPath + article)
