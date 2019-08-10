import requests, urllib.request, time, os, sys, click, jets
from bs4 import BeautifulSoup
from pathvalidate import ValidationError, validate_filename
from PyPDF2 import PdfFileReader, PdfFileWriter
from shutil import copyfile

bUrl = "https://www.etsjets.org"
url = "https://www.etsjets.org/JETS_Online_Archive"
rPath = os.path.realpath(__file__)
rPath = rPath.replace("downloader.py","")

def get_volume(vNum, iNum, aNum, force):
    if vNum == 0:
        check = "Vol "
    else:
        check = " " + vNum + " "
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    link_list = soup.findAll('a')
    for link in link_list:
        link = str(link)
        if check in link:
            x = link.find('"') + 1
            y = link.find('"', x)
            urlAppend = link[x:y]
            vUrl = bUrl + urlAppend
            get_issues(vNum, vUrl, iNum, aNum, force)

def get_issues(vNum, vUrl, iNum, aNum, force):
    response = requests.get(vUrl)
    soup = BeautifulSoup(response.text, 'html.parser')
    link_list = soup.findAll('a')
    for link in link_list:
        link = str(link)
        if not iNum == 0:
            if " " + vNum + "." + iNum in link and "Go to" not in link:
                x = link.find('"') + 1
                y = link.find('"', x)
                urlAppend = link[x:y]
                iUrl = bUrl + urlAppend
                get_article(vNum, iUrl, iNum, aNum, force)
        else:
            if " " + vNum + "." in link and "Go to" not in link:
                x = link.find('"') + 1
                y = link.find('"', x)
                d = link.find(".")+1
                e = link.find("<", d)
                nNum = link[d:e]
                urlAppend = link[x:y]
                iUrl = bUrl + urlAppend
                get_article(vNum, iUrl, nNum, aNum, force)

def get_article(vNum, iUrl, iNum, aNum, force):
    response = requests.get(iUrl)
    soup = BeautifulSoup(response.text, 'html.parser')
    link_list = soup.findAll('a')
    z = 0
    for link in link_list:
        link = str(link)
        if aNum == 0:
            if ".pdf" in link and "Purchase Articles" not in link and "Purchase Back Issue(s)" not in link:
                z = z + 1
                x = link.find('>') + 1
                y = link.find('<', x)
                a = link.find('"') + 1
                b = link.find('"', a)
                aUrl = link[a:b]
                aUrl = bUrl + aUrl
                tStart = link[x:y]
                if "http://www.etsjets.org/" in aUrl:
                    aUrl = aUrl.replace("http://www.etsjets.org", "")
                if "https://www.etsjets.org/" in link:
                    aUrl = aUrl.replace("https://www.etsjets.org", "")
                title_fixer(tStart, vNum, iNum, z, aUrl, force)
        else:
            if ".pdf" in link and "Purchase Articles" not in link and "Purchase Back Issue(s)" not in link:
                z = z + 1
                if str(z) == aNum:
                    x = link.find('>') + 1
                    y = link.find('<', x)
                    a = link.find('"') + 1
                    b = link.find('"', a)
                    aUrl = link[a:b]
                    aUrl = bUrl + aUrl
                    tStart = link[x:y]
                    if "http://www.etsjets.org/" in aUrl:
                        aUrl = aUrl.replace("http://www.etsjets.org", "")
                    if "https://www.etsjets.org/" in link:
                        aUrl = aUrl.replace("https://www.etsjets.org", "")
                    title_fixer(tStart, vNum, iNum, z, aUrl, force)

def title_fixer(title, vNum, iNum, aNum, aUrl, force):
    orig_title = title
    if ". . ." in title:
        if title.count(". . .") == 2:
            author = title.split(". . .")[2]
            title = title.split(". . .")[0:1]
            title = ' '.join(title)
        else:
            author = title.split(". . .")[1]
            title = title.split(". . .")[0]
        author = author.strip()
        title = title.strip()
    else:
        author = "JETS"
    if ": " in title:
        title = title.replace(": "," - ")
    if ":" in title:
        title = title.replace(":", "-")
    if "’" in title:
        title = title.replace("’", "'")
    if "”" in title or "“" in title:
        title = title.replace("“", "'")
        title = title.replace("”", "'")
    if '"' in title:
        title = title.replace('"', "'")
    if "/" in title:
        title = title.replace("/", "-")
    if title.endswith(" ") or title.endswith("."):
        title = title[:-1]
    if "?" in title:
        if title.endswith("?"):
            title = title[:-1]
        else:
            title = title.replace("?", ' - ')
    if author.endswith("."):
        author = author[:-1]
    if author.endswith(" "):
        author = author[:-1]
    title = title.title()
    if "'S" in title:
        title = title.replace("'S", "'s")
    if "&Amp;" in title:
        title = title.replace("&Amp;", "And")
    try:
        validate_filename(author)
    except ValidationError as e:
        jets.p("{}\n".format(e), file=sys.stderr)
    try:
        validate_filename(title)
    except ValidationError as e:
        jets.p("{}\n".format(e), file=sys.stderr)
    num = vNum + "." + str(iNum) + "." + str(aNum)
    title = num + " - " +title
    download(title, author, aUrl, force)


def download(title, author, aUrl, force):
    path = rPath + "/Articles/All/"
    fName = title + ".pdf"
    if os.path.exists(path + fName) and force == "False":
        jets.p(fName)
        click.echo("This File Already Exists")
    else:
        jets.p(title + " | " + author)
        r = requests.get(aUrl, stream=True)
        with open(path + "temp.pdf", 'wb') as f:
            f.write(r.content)
        with open(path + "temp.pdf", 'rb') as f: #open file again
            pdf = PdfFileReader(f)
            writer = PdfFileWriter() #open pdfwriter

            for page in range(pdf.getNumPages()): #get the pages
                writer.addPage(pdf.getPage(page)) #move them

            writer.addMetadata({ #add metadata
                '/Author': author,
                '/Title': title
            })

            fout = open(path + fName, 'ab') #open the output file
            writer.write(fout) #write the new pdf to the output
            fout.close()
        f.close()
        os.remove(path + "temp.pdf")
        authCreator(fName, author, force)
        time.sleep(1)

def authCreator(fName, author, force):
    for file in os.listdir(rPath + "/Articles/All"):
        if fName == file:
            f = open(rPath + "/Articles/All/" + file, 'rb')
            pdf = PdfFileReader(f)
            info = pdf.getDocumentInfo()
            author = info.author
            f.close()
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
                        x = len(temp - 2)
                    else:
                        x = len(temp - 1)
                    last = temp[x]
                    if not x == 1:
                        x = x-1
                        middle = temp[x]
                        if not len(middle) == 2:
                            middle = middle[0:1] + "."
                            temp[x] = middle
                            if not x <= 1:
                                x = x -1
                                nMiddle = temp[x]
                                if not len(nMiddle) == 2:
                                    nMiddle = nMiddle[0:1] + "."
                                    temp[x] = nMiddle
                    a = ' '.join(temp)
                    name.append(a)
                author = ", ".join(name)
                for n in name:
                    path = rPath + "/Articles/Authors/" + n
                    if not os.path.exists(path):
                        os.mkdir(path)
                    nPath = path + "/" + fName
                    if os.path.exists(nPath) and force == "False":
                        jets.p("Authors/" + n  + "/" + fName)
                        click.echo("Already exists")
                    else:
                        copyfile(rPath + "Articles/All/" + fName, nPath)
                jets.p("Downloaded")
            else:
                path = rPath + "/Articles/Authors/" + author
                if not os.path.exists(path):
                    os.mkdir(path)
                nPath = path + "/" + fName
                if os.path.exists(nPath) and force == "False":
                    jets.p("Authors/" + author +  "/" + fName)
                    click.echo("Already Exists")
                else:
                    copyfile(rPath + "Articles/All/" + fName, nPath)
                    jets.p("Downloaded")
