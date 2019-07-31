import sys
import os
base = "C:/Users/jonat/OneDrive/Documents/JETS/"
curPath = ""
curIssue = ""
curVol = ""
def main():    #Main file. going to go about this a different way this time
    length = len(sys.argv)
    if length > 2:
        arg1 = sys.argv[2]
        if int(arg1) >= 1 and int(arg1) <= 62:
            data = arg1
            startfix(arg1)
        else:
            print("Correct Usage: jets -f (1-62)")
    else:
        print("Correct Usage: jets -f (1-62)")

def startfix(data):
    global curPath
    global curIssue
    global curVol
    for vol in os.listdir(base):
        if "Vol " + data + " " in vol:
            curPath = base + vol + "/"
            for issue in os.listdir(curPath):
                curIssue = issue
                curPath = base + vol + "/" + issue #keep this way to avoid "errors"
                for article in os.listdir(curPath):
                    curPath = base + vol + "/" + issue + "/" + article
                    getName(article)

def getName(article):
    x = 0
                    
                
        
