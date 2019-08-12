import os, click, sys, re
from PyPDF2 import PdfFileReader, PdfFileWriter
from shutil import copyfile
path = os.path.realpath(__file__)
path = path.replace("util.py","")
path = path + "Articles/"
fPath = path + "All/"
numbers = re.compile(r'(\d+)')

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


def getInfo(pdf):
    f = open(pdf, 'rb') #open the right article as "f"
    pdf = PdfFileReader(f)
    info = pdf.getDocumentInfo() #gets metadata
    f.close()
    return info

def getNum(vNum, iNum, aNum):
    vNum = check_digit(vNum)
    iNum = check_digit(iNum)
    aNum = check_digit(aNum)
    num = vNum + "." + iNum + "." + aNum
    return num

def writeInfo(pPath, name, author):
    f = open(pPath, 'rb')
    pdf = PdfFileReader(f)
    writer = PdfFileWriter()
    for page in range(pdf.getNumPages()):
        writer.addPage(pdf.getPage(page))
    writer.addMetadata({
        '/Author': author,
        '/Title': name
    })
    fout = open(path + 'temp.pdf', 'ab')
    writer.write(fout)
    fout.close()
    f.close()
    copyfile(path + "temp.pdf", pPath)
    os.remove(path + "temp.pdf")

def check_digit(num):
    if len(str(num)) == 1:
        num = "0" + str(num)
    return num

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

def get_nums(article):
    num = article.split(" - ")[0]
    a = num.split(".")
    vNum,iNum, aNum = [a[0], a[1], a[2]]
    payload = [num, vNum, iNum, aNum]
    return payload

def display_info(articles):
    u = 0
    for article in articles:
        title = article.split(" - ")[1]
        title = article.split(".pdf")[0]
        z = len(title)
        if z > u:
            u = z + 2
    header = "{0:^11}| {1:^{3}} |{2:^16}".format("ARTICLE", " TITLE", "AUTHOR", u)
    lChar = u"\u2015"
    line = ""
    line2 = ""
    for x in range(len(header) + 8): #seems self explanatory
        if x == 11 or x == 13 + u:
            line = line + "|"
            line2 = line2 + lChar
        line = line + lChar
        line2 = line2 + lChar
    p(line2)
    click.echo(header)
    click.echo(line)
    for article in articles:
        payload = get_nums(article)
        num,vNum,iNum,aNum = [payload[0], payload[1], payload[2], payload[3]]
        title = article.split(" - ")[1]
        title = title.split(".pdf")[0]
        vNum = check_digit(vNum)
        iNum = check_digit(iNum)
        aNum = check_digit(aNum)
        info = getInfo(fPath + article)
        author = info.author
        a = ''
        if " And " in author:
            authors = []
            test = []
            auths = author.split(" And ")
            for a in auths:
                if "," in a:
                    authos = a.split(",")
                    for auth in authos:
                        auth = auth.strip()
                        if not auth == "":
                            test.append(auth)
                else:
                    test.append(a)
            name = []
            for po in test:
                first = po[0:1] + "."
                temp = po.split(" ")
                temp[0] = first
                if "Jr" in temp or "III" in temp:
                    x = len(temp) - 2
                else:
                    x = len(temp)-1
                last = temp[x]
                if not x == 1:
                    x = x -1
                    middle = temp[x]
                    if not len(middle) == 2:
                        middle = middle[0:1] + "."
                        temp[x] = middle
                        if not x <= 1:
                            x = x - 1
                            nMiddle = temp[x]
                            if not len(nMiddle) == 2:
                                nMiddle = nMiddle[0:1]
                                temp[x] = nMiddle
                a = ' '.join(temp)
                name.append(a)
            author = ', '.join(name)
        display = "{0:^11}|  {1:<{3}}|  {2}".format(num, title, author, u)
        click.echo(display)
