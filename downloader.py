import requests, urllib.request, time, os, sys, click, jets
from bs4 import BeautifulSoup
from pathvalidate import ValidationError, validate_filename
from PyPDF2 import PdfFileReader, PdfFileWriter
from shutil import copyfile

bUrl = "https://www.etsjets.org"
url = "https://www.etsjets.org/JETS_Online_Archive"

path = os.path.realpath(__file__)
path = path.replace("downloader.py","")
path = path + "Articles/"

def downloading(vNum, iNum, aNum, force):
    if vNum == '0':
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
        if not iNum == '0':
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
        if aNum == '0':
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
    fName = num + " - " +title + ".pdf"
    download(title, fName, author, aUrl, force)


def download(title, fName, author, aUrl, force):
    dPath = path + "All/"
    if os.path.exists(dPath + fName) and force == False:
        jets.p(fName)
        click.echo("This File Already Exists")
    else:
        jets.p(title + " | " + author)
        r = requests.get(aUrl, stream=True)
        with open(dPath + "temp.pdf", 'wb') as f:
            f.write(r.content)
        with open(dPath + "temp.pdf", 'rb') as f: #open file again
            pdf = PdfFileReader(f)
            writer = PdfFileWriter() #open pdfwriter

            for page in range(pdf.getNumPages()): #get the pages
                writer.addPage(pdf.getPage(page)) #move them

            writer.addMetadata({ #add metadata
                '/Author': author,
                '/Title': title
            })

            fout = open(dPath + fName, 'ab') #open the output file
            writer.write(fout) #write the new pdf to the output
            fout.close()
        f.close()
        os.remove(dPath + "temp.pdf")
        authCreator(fName, author, force)
        time.sleep(1)

def authCreator(fName, author, force):
    for file in os.listdir(path + "All/"):
        if fName == file:
            f = open(path + "All/" + file, 'rb')
            pdf = PdfFileReader(f)
            info = pdf.getDocumentInfo()
            author = info.author
            f.close()
            if " And " in author:
                authors = []
                auths = author.split(" And ")
                for a in auths:
                    if "," in a:
                        authos = a.split(",")
                        for auth in authos:
                            auth = auth.strip()
                            if not auth == "":
                                authors.append(auth)
                    else:
                        a = a.strip()
                        a = a.strip() #just in case
                        authors.append(a)
                for n in authors:
                    aPath = path  +  "Authors/" + n
                    if not os.path.exists(aPath):
                        os.mkdir(aPath)
                    aPath = aPath + "/" + fName
                    if os.path.exists(aPath) and force == False:
                        jets.p("Authors/" + n  + "/" + fName)
                        click.echo("Already exists")
                    else:
                        copyfile(path + "All/" + fName, aPath)
                jets.p("Downloaded")
            else:
                aPath = path + "Authors/" + author
                if not os.path.exists(aPath):
                    os.mkdir(aPath)
                aPath = aPath + "/" + fName
                if os.path.exists(aPath) and force == False:
                    jets.p("Authors/" + author +  "/" + fName)
                    click.echo("Already Exists")
                else:
                    copyfile(path + "All/" + fName, aPath)
                    jets.p("Downloaded")