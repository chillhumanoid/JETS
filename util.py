import os, click


path = os.path.realpath(__file__)
path = path.replace("util.py","")
path = path + "Articles/"

def start():
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(path + "All"):
        os.mkdir(path + "All")
    if not os.path.exists(path + "Authors/"):
        os.mkdir(path + "Authors/")
    if not os.path.exists(path + "Merged/"):
        os.mkdir(path + "Merged/")
def p(msg):
    click.echo()
    click.echo(msg)

def getNumbers(term):
    cDot = term.count(".")
    vNum = "0"
    iNum = "0"
    aNum = "0"
    if cDot >= 0:
        vNum = term.split(".")[0]
    if cDot >= 1:
        iNum = term.split(".")[1]
    if cDot == 2:
        aNum = term.split(".")[2]
    return (vNum, iNum, aNum)
