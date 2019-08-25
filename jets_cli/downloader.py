import requests, urllib.request, sqlite3, known_authors, os, sys, click, util, search
import rename as ren, fileparser as parsr, database as db, login as log
from bs4 import BeautifulSoup;
from requests import Session
from pathvalidate import ValidationError, validate_filename
from PyPDF2 import PdfFileReader, PdfFileWriter; from shutil import copyfile, move

base_url     = "https://www.etsjets.org"
url          = "https://www.etsjets.org/JETS_Online_Archive"
path         = os.path.realpath(__file__)
path         = path.replace("downloader.py","")
path         = path + "/Articles/"
all_path     = path + "All/"
login_exists = util.is_login()

def get_volume_url(data):
    """
    Start of pdf downloader, needs to get volume url first

    Parameters:
    data (list) : volume_number, issue_number, article_number, force(deprecated?)

    Moves to get_issue_url with (data)
    """
    with Session() as s:
        
        if login_exists:
            login_data = {"name":log.get_username(), "pass":log.get_password(), "op":"Log in", "form_build_id":"form-a0ed7b5c7437ac9afeb21b126e24633b", "form_id":"user_login_block"}
            s.post("https://www.etsjets.org/new_welcome?destination=node%2F1120", login_data)
        
        volume_number    = data[0]
        if volume_number == '0':
            file_start   = "Vol "
        else:
            file_start   = " " + volume_number + " "
 
        response         = s.get(url)
        soup             = BeautifulSoup(response.content,'html.parser')
        link_list        = soup.findAll('a') #finds the "a" tag on url

        for link in link_list:
            
            link         = str(link)

            if file_start in link:
                
                link_start  = link.find('"') + 1
                link_end    = link.find('"', link_start)
                urlAppend   = link[link_start:link_end]
                volume_url  = base_url + urlAppend

                get_issue_url(data, volume_url)
 
def get_issue_url(data, volume_url):
    """
    Gets all issue urls in the volume

    Parameters:
    data(list) : see get_vol_url for that
    volume_url : the url that the volume is at
    """
    with Session() as s:
        
        if login_exists:
            login_data = {"name":log.get_username(), "pass":log.get_password(), "op":"Log in", "form_build_id":"form-a0ed7b5c7437ac9afeb21b126e24633b", "form_id":"user_login_block"}
            s.post("https://www.etsjets.org/new_welcome?destination=node%2F1120", login_data)
        
        issue_number_original  = data[1]
        issue_number           = data[1]
        volume_number          = data[0]
        response               = s.get(volume_url)
        soup                   = BeautifulSoup(response.text, 'html.parser')
        link_list              = soup.findAll('a')
        i                      = 0
   
        for link in link_list:

            link = str(link)
            
            if (" " + volume_number + "." in link or volume_number + "." in link or volume_number + "_" in link) and not "Go to " in link:
                
                i          = i + 1
                link_start = link.find('"') + 1
                link_end   = link.find('"', link_start)
                url_append = link[link_start:link_end]
                issue_url  = base_url + url_append
                y = 0
                if (issue_number == '0') or ("." + issue_number in link) or (volume_number + "_" + issue_number in link):

                    if issue_number == '0':
                        y = i
                        if volume_number + "_" in link:
                            location_one = link.find("_")+1
                            location_two = link.find('"', location_one)
                        elif volume_number + "-" in link:
                            location_one = link.find("-") + 1
                            location_two = link.find('"', location_one)
                        elif volume_number + "." in link:
                            location_one = link.find(".") + 1
                            location_two = link.find("<", location_one)
                        i = link[location_one:location_two]

                    data[1]    = str(i)
                    i = y
                    get_article_url(data, issue_url)

                    data[1]    = issue_number_original
 
def get_article_url(data, issue_url):
    """
    Gets all article urls in the issue

    Parameters:
    data(list) : see get_vol_url for that
    issue_url : the url that the issue is at
    """
    with Session() as s:
        
        if login_exists:
            login_data = {"name":log.get_username(), "pass":log.get_password(), "op":"Log in", "form_build_id":"form-a0ed7b5c7437ac9afeb21b126e24633b", "form_id":"user_login_block"}
            s.post("https://www.etsjets.org/new_welcome?destination=node%2F1120", login_data)
        
        article_number_original = data[2]
        article_number          = data[2]
        response                = s.get(issue_url)
        soup                    = BeautifulSoup(response.text, 'html.parser')
        link_list               = soup.findAll('a')
        z                       = 0

        for link in link_list:

            link = str(link)
            
            if ".pdf" in link and "Purchase Articles" not in link and "Purchase Back Issue(s)" not in link:
                
                z = z + 1
                
                if str(z) == article_number or article_number == '0':\

                    if "<em>" in link:
                        link = link.replace("<em>", "")
                        link = link.replace("</em>", "")
                    if "<br/>" in link:
                        link = link.replace("<br/>", "")
                    if "\n" in link:
                        link = link.replace("\n", "")
                    title_start = link.find('>') + 1
                    title_end   = link.find('<', title_start)
                    link_start  = link.find('"') + 1
                    link_end    = link.find('"', link_start)
                    article_url = link[link_start:link_end]
                    article_url = base_url + article_url
                    title       = link[title_start:title_end]

                    if "http://www.etsjets.org/" in article_url:
                        article_url = article_url.replace("http://www.etsjets.org", "")
                    if "https://www.etsjets.org/" in article_url:
                        article_url = article_url.replace("https://www.etsjets.org", "")
                    
                    article_url = base_url + article_url
                    data[2]     = str(z)
                    get_title_and_author(data, title, article_url)
                    data[2]     = article_number_original

def get_title_and_author(data, title, article_url):
    """
    Gets the title and author given the data passed over

    Parameters:
    data(list) : see get_vol_url for that
    title      : the title that was grabbed from the article url above
    article_url : the url that the article is at
    """
    original_file_name = title
    count              = title.count(". . .")
    article_title      = parsr.get_raw_title(count, original_file_name)
    volume_number      = util.check_digit(data[0])
    issue_number       = util.check_digit(data[1])
    article_number     = util.check_digit(data[2])

    util.p(original_file_name)

    full_number        = volume_number + "." + issue_number + "." + article_number

    author_name        = parsr.get_raw_author(count, original_file_name)
    author_name        = known_authors.change_known_authors(author_name)

    

    download(article_title, author_name, article_url, data, full_number, volume_number, issue_number, article_number)


def download(article_title, author_name, article_url, data, full_number, volume_number, issue_number, article_number):
    """
    Downloads the file

    Parameters:
    article_title  (string)\n
    author_name    (string)\n
    article_url    (string)\n
    data           (list)\n
    full_number    (string)\n
    volume_number  (int)\n
    issue_number   (int)\n
    article_number (int)\n
    """
    article_exists = db.search_articles_table(full_number)

    if article_exists:
        util.p(article_title)
        click.echo("This File Already Exists")
    
    else:

        util.p(full_number)
        click.echo("Title: " + article_title)
        click.echo("Author: " + author_name)
        if click.confirm("Download File?"):
            
            author_ids = author_database_worker(author_name)

            db.add_to_articles_table(full_number, int(volume_number), int(issue_number), int(article_number), article_title, author_ids)

            article_id = db.get_article_id(full_number)

            if "&amp;" in article_url:
                article_url = article_url.replace("&amp;", "&")

            r = requests.get(article_url, stream=True)

            with open(all_path + str(article_id) + ".pdf", 'wb') as file:
                file.write(r.content)
            
            time.sleep(1)
        else:
            value = click.prompt("Change (A)uthor or (T)itle or (N)either?", default="n")
            value = value.lower()
            if value == "a":
                util.p("Current Author: " + author_name)
                new_author = click.prompt("New Author Name: ")
                download(article_title, new_author, article_url, data, full_number, volume_number, issue_number, article_number)
            elif value == "t":
                util.p("Current Title: " + article_title)
                new_title = click.prompt("New Title: ")
                download(new_title, author_name, article_url, data, full_number, volume_number, issue_number, article_number)


def author_database_worker(author):
    """
    Adds the authors to the author table if not already there, and gets there ID after

    Parameters:
    author (string)
    
    Returns:
    author_ids (list)
    """
    authors = parsr.get_authors(author)
    author_ids = []
    for name in authors:
        author_name = util.get_possible_names(name)
        if author_name == None:
            author_name = name
        db.add_to_author_table(author_name)
        author_ids.append(db.get_author_id(author_name))
    return author_ids
