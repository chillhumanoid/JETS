import requests, urllib.request, time, os, sys, click, util
from bs4 import BeautifulSoup
from pathvalidate import ValidationError, validate_filename
from PyPDF2 import PdfFileReader, PdfFileWriter; from shutil import copyfile, move
from pynput.keyboard import Key, Listener

bUrl = "https://www.etsjets.org"
url = "https://www.etsjets.org/JETS_Online_Archive"

path = os.path.realpath(__file__)
path = path.replace("downloader.py","")
path = path + "/Articles/"
all_path = path + "All/"
author_path = path + "Authors/"

def start(data):
    get_vol_url(data)

def get_vol_url(data):
    vol_num = data[0]
    if vol_num == '0':
        check = "Vol "
    else:
        check = " " + vol_num + " "
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    link_list = soup.findAll('a')
    for link in link_list:
        link = str(link)
        if check in link:
            link_start = link.find('"') + 1
            link_end = link.find('"', link_start)
            urlAppend = link[link_start:link_end]
            vol_url = bUrl + urlAppend
            get_issue_url(data, vol_url)

def get_issue_url(data, vol_url):
    issue_num_orig = data[1]
    issue_num = data[1]
    vol_num = data[0]
    response = requests.get(vol_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    link_list = soup.findAll('a')
    i = 0
    for link in link_list:
        link = str(link)
        if " " + vol_num + "." in link and "Go to" not in link:
            i = i + 1
            link_start = link.find('"') + 1
            link_end = link.find('"', link_start)
            url_append = link[link_start:link_end]
            issue_url = bUrl + url_append
            if issue_num == '0' or "." + issue_num in link:
                data[1] = str(i)
                get_article_url(data, issue_url)
                data[1] = issue_num_orig

def get_article_url(data, issue_url):
    article_num_orig = data[2]
    article_num = data[2]
    response = requests.get(issue_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    link_list = soup.findAll('a')
    z = 0
    for link in link_list:
        link = str(link)
        if ".pdf" in link and "Purchase Articles" not in link and "Purchase Back Issue(s)" not in link:
            z = z + 1
            if str(z) == article_num or article_num == '0':
                if "<em>" in link:
                    link = link.replace("<em>", "")
                    link = link.replace("</em>", "")
                title_start = link.find('>') + 1
                title_end = link.find('<', title_start)
                link_start = link.find('"') + 1
                link_end = link.find('"', link_start)
                article_url = link[link_start:link_end]
                article_url = bUrl + article_url
                title = link[title_start:title_end]
                if "http://www.etsjets.org/" in article_url:
                    article_url = article_url.replace("http://www.etsjets.org", "")
                if "https://www.etsjets.org/" in article_url:
                    article_url = article_url.replace("https://www.etsjets.org", "")
                article_url = bUrl + article_url
                data[2] = str(z)
                get_title_and_author(data, title, article_url)
                data[2] = article_num_orig

def get_title_and_author(data, title, article_url):
    orig_title = title
    print(orig_title)
    count = title.count(". . .")
    if not count == 0:
        author = title.split(". . .")[count]
        if not count == 1:
            title = title.split(". . .")[0:count-1]
        else:
            title = title.split(". . .")[0]
        title = ''.join(title)
    else:
        author = "JETS"

    title = fix_title(title)
    author = fix_author(author)
    try:
        validate_filename(author)
        validate_filename(title)
    except ValidationError as e:
        click.echo()
        click.echo("{}\n".format(e), file=sys.stderr)
        sys.exit()
    full_num = util.check_digit(data[0]) + "." + util.check_digit(data[1]) + "." + util.check_digit(data[2])
    full_name =  full_num + " - " + title + ".pdf"
    download(title, full_name, author, article_url, data, full_num)
def fix_author(author):
    if ", Jr" in author:
        author = author.replace(", Jr", " Jr")
    author = util.string_strip(author)
    return author
def fix_title(title):
    title = title.replace('\n', ' ')
    title = title.replace(": ", " - ")
    title = title.replace(":", "_")
    title = title.replace("’", "'")
    title = title.replace("“", "'")
    title = title.replace("”", "'")
    title = title.replace('"', "'")
    title = title.replace("/", "-")
    title = util.string_strip(title)
    title = title.replace("?", ' - ')
    title = title.title()
    title = title.replace("Iii", "III")
    title = title.replace("Iv", "IV")
    title = title.replace("Ot", "OT")
    title = title.replace("Nt", "NT")
    title = title.replace("'S", "'s")
    title = title.replace("&Amp;", "And")
    return title


def download(title, full_name, author, article_url, data, full_num):
    force = data[3]
    if os.path.exists(all_path + full_name) and force == False:
        util.p(full_name)
        click.echo("This File Already Exists")
    else:
        util.p(full_num)
        click.echo("Title: " + title)
        click.echo("Author: " + author)
        if click.confirm("Download File?"):
            if "&amp;" in article_url:
                article_url = article_url.replace("&amp;", "&")
            r = requests.get(article_url, stream=True)
            with open(all_path + "temp.pdf", 'wb') as file:
                file.write(r.content)
            util.write_info(all_path + "temp.pdf", title, author)
            move(all_path + "temp.pdf", all_path + full_name)
            author_creator(full_name, author, force)
            time.sleep(1)
        else:
            value = click.prompt("Change (A)uthor or (T)itle or (N)either?", default="n")
            value = value.lower()
            if value == "a":
                util.p("Current Author: " + author)
                new_auth = click.prompt("New Author Name: ")
                download(title, full_name, new_auth, article_url, data, full_num)
            elif value == "t":
                util.p("Current Title: " + title)
                new_title = click.prompt("New Title: ")
                download(title, full_name, new_auth, article_url, data, full_num)


def author_creator(full_name, author, force):
    aPath = ""
    for file in os.listdir(all_path):
        if full_name == file:
            f = open(path + "All/" + file, 'rb')
            pdf = PdfFileReader(f)
            info = pdf.getDocumentInfo()
            f.close()
            authors = []
            if " and " in author:
                auths = author.split(" and ")
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
            else:
                authors.append(author)
            for name in authors:
                print(name)
                full_name_split = name.split(" ")
                first = full_name_split[0]
                first_initial = first[0:1]
                if "Jr" in full_name_split or "III" in full_name_split:
                    last_location = len(full_name_split) - 2
                else:
                    last_location = len(full_name_split) - 1
                last = full_name_split[last_location]
                for author_name in os.listdir(author_path):
                    if not author_name == name:
                        author_split = author_name.split(" ")
                        author_first = author_split[0]
                        author_first_initial = author_first[0:1]
                        if author_first == first or author_first_initial == first_initial:
                            if "Jr" in author_split or "III" in author_split:
                                last_name_location = len(author_split) - 2
                            else:
                                last_name_location = len(author_split) - 1
                            author_last = author_split[last_name_location]
                            if author_last == last:
                                if click.confirm("Author Folder Possible: Articles/Authors/" + author_name):
                                    aPath = author_path + author_name
                                    break
                    else:
                        break
                if aPath == "":
                    aPath = author_path + name
                if not os.path.exists(aPath):
                    os.mkdir(aPath)
                aPath = aPath + "/" + full_name
                if os.path.exists(aPath) and not force:
                    util.p("Authors/" + name  + "/" + full_name)
                    click.echo("Already exists")
                else:
                    copyfile(all_path + full_name, aPath)
                aPath = ""
                util.p("Downloaded")
