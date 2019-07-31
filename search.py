import os
import sys

base = "C:/Users/jonat/OneDrive/Documents/JETS/"

def article(): #for searching articles
    if len(sys.argv) < 4:
        print()
        print("Please enter a search term.")
    else:
        print()
        x = 0
        term = sys.argv[3]
        if len(sys.argv) > 4:
            for x in range(4,len(sys.argv)):
                term = term + " " + sys.argv[x]
        for folder in os.listdir(base):
            if "Vol " in folder:
                path = base + folder + "/"
                for issue in os.listdir(path):
                    nPath = path + issue + "/"
                    for file in os.listdir(nPath):
                        term = term.lower()
                        f = file.lower()
                        if term in f:
                            aNum = file.split(")")[0]
                            title = file.split(") - ")[1]
                            vNum = folder.split(" ")[1]
                            iNum = issue.split(".")[1]
                            x = x + 1
                            print(vNum + "." + iNum + "." + aNum + " - " + title)
        if x == 0:
            print()
            print("No Articles Found")
                        
