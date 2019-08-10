import os, click, sys


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

def check_vol(vol):
    if not vol >= 0 and vol <= 62:
        p("Please enter 1-62 for Volume")
        sys.exit()

def check_issue(issue):
    if not issue >= 0 and vol <= 4:
        p("Please enter 1-4 for Issue")
        sys.exit()

def getNumbers(term):
    cDot = term.count(".")
    vNum = "0"
    iNum = "0"
    aNum = "0"
    if cDot >= 0:
        vNum = term.split(".")[0]
        if vNum.isdigit():
            check_vol(int(vNum))
        else:
            p("Please enter a number for volume")
            sys.exit()
    if cDot >= 1:
        iNum = term.split(".")[1]
        if iNum.isdigit():
            check_issue(int(iNum))
        else:
            p("Please enter a number for issue")
            sys.exit()
    if cDot == 2:
        aNum = term.split(".")[2]
        if not aNum.isdigit():
            p("please enter a number for article")
            sys.exit()
    return (vNum, iNum, aNum)
