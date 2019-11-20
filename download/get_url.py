import requests, urllib.request, sqlite3, click
from bs4 import BeautifulSoup
from requests import Session
from download import util, download, information
from util import p
import login as log

login_exists = util.is_login()
base_url     = "https://www.etsjets.org"
url          = "https://www.etsjets.org/JETS_Online_Archive"

def volume(data):
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

                issue(data, volume_url)

def issue(data, volume_url):
    """
    Gets all issue urls in the volume

    Parameters:
    data(list) : see get_vol_url for that
    volume_url : the url that the volume is at
    """

    with Session() as s:
        p("testing")
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
                    article(data, issue_url)
                    data[1]    = issue_number_original

def article(data, issue_url):
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
                if str(z) == article_number or article_number == '0':
                    link = util.fix_link(link)
                    title = information.get_title_from_link(link)

                    link_start  = link.find('"') + 1
                    link_end    = link.find('"', link_start)
                    article_url = link[link_start:link_end]
                    article_url = base_url + article_url
                    if "http://www.etsjets.org/" in article_url:
                        article_url = article_url.replace("http://www.etsjets.org", "")
                    if "https://www.etsjets.org/" in article_url:
                        article_url = article_url.replace("https://www.etsjets.org", "")
                    article_url = base_url + article_url
                    if not article_url == "https://www.etsjets.org/files/JETS-PDFs/58/58-2/JETS_58-1_117-30_Blackburn.pdf": #currently broken
                        data[2]     = str(z)
                        download.article(data, title, article_url)
                        data[2]     = article_number_original
