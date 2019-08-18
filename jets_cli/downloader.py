import requests, urllib.request, sqlite3, time, os, sys, click, util, rename as ren, fileparser as parsr, database
from bs4 import BeautifulSoup
from pathvalidate import ValidationError, validate_filename
from PyPDF2 import PdfFileReader, PdfFileWriter; from shutil import copyfile, move

bUrl = "https://www.etsjets.org"
url = "https://www.etsjets.org/JETS_Online_Archive"

path = os.path.realpath(__file__)
path = path.replace("downloader.py","")
path = path + "/Articles/"
all_path = path + "All/"

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
    original_file_name = title
    util.p(original_file_name)
    count = title.count(". . .")
    full_num = util.check_digit(data[0]) + "." + util.check_digit(data[1]) + "." + util.check_digit(data[2])
    full_name =  full_num + " - " + file_name + ".pdf"
    title = parsr.get_raw_title(full_name, count, original_file_name)
    file_name = parsr.get_file_name(title)
    author = parsr.get_raw_author(full_name, count, original_file_name)
    try:
        validate_filename(file_name)
    except ValidationError as e:
        click.echo()
        click.echo("{}\n".format(e), file=sys.stderr)
        sys.exit()
    finally:
        download(title, file_name, full_name, author, article_url, data, full_num)

def download(title, file_name, full_name, author, article_url, data, full_num):
    force = data[3]
    if os.path.exists(all_path + full_name) and force == False:
        util.p(full_name)
        click.echo("This File Already Exists")
    else:
        util.p(full_num)
        click.echo("File Name: " + file_name)
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
            author_database_worker  (full_name, full_num, author, force, title)
            time.sleep(1)
        else:
            value = click.prompt("Change (A)uthor or (T)itle or (N)either?", default="n")
            value = value.lower()
            if value == "a":
                util.p("Current Author: " + author)
                new_auth = click.prompt("New Author Name: ")
                download(title, file_name, full_name, new_auth, article_url, data, full_num)
            elif value == "t":
                util.p("Current Title: " + title)
                new_title = click.prompt("New Title: ")
                download(new_title,file_name, full_name, author, article_url, data, full_num)


def author_database_worker(full_name, full_num, author, force, title):
    for file in os.listdir(all_path):
        if full_name == file:
            authors = fileparser.get_authors(author)
            full_nums = database.get_full_numbers()
            for name in authors:
                author_name = util.get_possible_names(name)
                if author_name == None:
                    author_name = name
                util.write_info(all_path + full_name, title, author_name) #change author name to folder name
                aPath = aPath + "/" + full_name
                if os.path.exists(aPath) and not force:
                    util.p("Authors/" + name  + "/" + full_name)
                    click.echo("Already exists")
                else:
                    copyfile(all_path + full_name, aPath)
                aPath = ""
                util.p("Downloaded")
