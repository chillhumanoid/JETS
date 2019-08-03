import os
import sys

base = "C:/Users/jonat/OneDrive/Documents/Jets/"

def main():
    for vol in os.listdir(base):
        if vol.startswith("Vol "):
            path = base + vol + "/"
            for issue in os.listdir(path):
                nPath = path + issue + "/"
                for article in os.listdir(nPath):
                    if article.startswith("OUT "):
                        nName = article.replace("OUT ", "")
                        nName = nName.replace(".pdf", "")
                        if nName.endswith(" "):
                            nName = nName.strip()
                        nName = nName + ".pdf"
                        print(nName)
                        os.replace(nPath + article, nPath + nName)
                    else:
                        if ").pdf" in article:
                            os.remove(nPath + article)
