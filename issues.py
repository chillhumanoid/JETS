import requests
import urllib.request
import time
import os
import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import backend
from termcolor import colored

def getIssues(nodeURL, vFold):
    response = requests.get(nodeURL)
    z = 0
    soup = BeautifulSoup(response.text, "html.parser")
    issues_list = soup.findAll('a')
    nIssues = []
    for x in range(32, len(issues_list)-1):
        nIssues.append(issues_list[x])
    issues_list = nIssues
    if not z == 1:
        for issue in issues_list:
            if x == 1:
                iFold = getiFolder(issue, vFold)
            else:
                #print(issue)
                url = issueURL(issue)
                #print(url)
                iFold = getiFolder(issue, vFold)
                if "-" in iFold:
                    iFold = iFold.replace("-", ".")
                path = "C:/Users/jonat/OneDrive/Documents/JETS/" + vFold + "/" + iFold + "/"
                #print(path)
                getContents(url, path, iFold)
    else:
        url = issueURL(issues_list[0])
        iFold = getiFolder(issues_list[0], vFold)
        if "-" in iFold:
            iFold = iFold.replace("-", ".")
        path = "C:/Users/jonat/OneDrive/Documents/JETS/" + vFold + "/" + iFold + "/"
        getContents(url, path, iFold)
        
def issueURL(issue):
    issue = str(issue)
    x = issue.find('"') + 1
    y = issue.find('"', x)
    endURL = issue[x:y]
    #print(endURL)
    if "etsjets.org" in endURL:
        url = endURL
    else:
        url = "https://www.etsjets.org" + endURL
    return url

def getContents(url, fPath, iFold):
    #print(url)
    response = requests.get(url)
    #print(response)
    soup = BeautifulSoup(response.text, "html.parser")
    contents = soup.findAll('a')
    fCon = []
    z = 0
    x = 1
    for content in contents:
        content = str(content)
        
        if "JETS-PDFs" in content:
            print(content)
            fCon.append(content)
    if z == 0:
        for content in fCon:
            #print(content)
            fURL = getURLs(content)
            fTitle = getTitle(content, iFold, x, fPath)
            fTitle = 0
            if fTitle == 0:
                x = x + 1
            else:
                fTitle = str(x) + ") " + fTitle
                x = x + 1
                downloader(fURL, fPath, fTitle, iFold, x-1)
    else:
        url = "no"
##
#
#                    Adjust the Title
##
def getTitle(title, iFold, checker):
    os.system('color')
    #print(content)
    #x = content.find(">") + 1
    #y = content.find("<", x)
    #title = content[x:y]
    #print(title)
    check = " . . . "
    print(colored("--------------------------------------------------------------------","red"))
    print(colored(iFold + " | FILE    | " + title, "cyan"))
    print(colored("--------------------------------------------------------------------","red"))
    if check in title:
        print(colored(iFold + " | PROCESS | Adjusting Author Name     | ","yellow"), end='\r')
        time.sleep(.8)
        title = title.replace(" . . . ", " (")
        title = title + ")"
        print(colored(iFold + " | SUCCESS | Adjusted Author Name      | " + title,"green"))
    if "&amp;" in title:
        print(colored(iFold + " | PROCESS | Fixing Ampersand          | ","yellow"), end='\r')
        time.sleep(.8)
        title = title.replace("&amp;", "&")
        print(colored(iFold + " | SUCCESS | Fixed Ampersand           | " + title,"green"))
    if "<em>" in title or "<br>" in title:
        print(colored(iFold + " | PROCESS | Adjusting File Name       | ","yellow"), end='\r')
        time.sleep(.8)
        title = title.replace("<em>",  "")
        title = title.replace("<br>", "")
        title = title.replace("</em>", "")
        print(colored(iFold + " | SUCCESS | Fixed weird part          | " + title,"green"))
    if ":" in title or "?" in title or '“' in title or "/" in title or "\\" in title or '"' in title:
        print(colored(iFold + " | PROCESS | Fixing Illegal Characters | ","yellow"), end='\r')
        time.sleep(.8)
        title = title.replace(":", " -")
        title = title.replace("?", "")
        title = title.replace('“', "'")
        title = title.replace('”', "'")
        title = title.replace('"', "'")
        title = title.replace("/", " & ")
        print(colored(iFold + " | SUCCESS | Fixed Illegal Characters  | ","green"))
    print(colored(iFold + " | PROCESS | Fixing Capitalization     | ","yellow"), end='\r')
    time.sleep(.8)
    title = title.lower()
    temp = title.rsplit(" ")
        #temp[15] = temp[15].replace('\n', ' ')
        #print(temp)
    newTitle = []
    for word in temp:
        if "\n" in word:
            word = word.replace('\n', ' ')
        x = word.find("'")
        wordLen = len(word)-1
        if x > 0 and not x == wordLen:
            word = word.capitalize()
            newTitle.append(word)
        elif word == "":
            temp = 0 #fix any double spaces
        elif word[0] == "'" or word[0] == "(":
            tWord = word[1:]
            tWord = tWord.capitalize()
            word = word[0] + tWord
            newTitle.append(word)
        else:
            word = word.capitalize()
            newTitle.append(word)
    title = ' '.join(newTitle)
    print(colored(iFold + " | SUCCESS | Fixed Capitalization      | " + title,"green"))
    print(colored(iFold + " | SUCCESS | Changed Title             | " + title, "green"))
    return title

def getURLs(content):
    x = content.find('"') + 1
    y = content.find('"', x)
    eURL = content[x:y]
    if "etsjets.org/" in eURL:
        fURL = eURL
    else:
        fURL = "https://www.etsjets.org" + eURL
    return fURL

def getiFolder(issue, vFold):
    issue = str(issue)
    x = issue.find(">") + 1
    y = issue.find("<", x)
    iFold = issue[x:y]
    return iFold

def makeiFolder(issue, vFold):
    issue = str(issue)
    x = issue.find(">") + 1
    y = issue.find("<", x)
    iFold = issue[x:y]
    z = iFold.find("-")
    if z > 0:
        iFold = iFold.replace("-", ".")
    path = "C:/Users/jonat/OneDrive/Documents/JETS/" + vFold + "/" + iFold
    if not os.path.exists(path):
        os.mkdir(path)
        print("SUCCESS - " + vFold + "/" + iFold + " folder created")
    else:
        print("IGNORED - " + vFold + "/" + iFold + " exists")
        
def fChecker(iFold, checker, fPath):
    for file in os.listdir(fPath):
        if checker in file:
            return True
def downloader(fURL, fPath, fTitle, iFold):
    if os.path.exists(fPath):
        print(colored(iFold + " | SKIPPED | File Already Exists", "green"))
    else:
        print(colored(iFold + " | PROCESS | Downloading File          |","yellow"), end='\r')
        r = requests.get(fURL, stream = True)
        with open(fPath, 'wb') as f:
            f.write(r.content)
        print(colored(iFold + " | SUCCESS | DOWNLOAD COMPLETE         |", "green"))
        time.sleep(1)

def urlCheck(url):
    response = requests.get(url)
    if str(response) == "<Response [200]>":
        return True
    else:
        return False
    
def test2(issue, url, z, vol, driver):
    driver.get(url)
    aList = []
    tList = []
    uList = []
    x = 0
    test = driver.find_elements_by_tag_name('a')
    for item in test:
        temp = item.get_attribute('outerHTML')
        if "JETS-PDFs" in temp:
            aList.append(temp)
            tList.append(item.get_attribute('innerHTML'))
    for item in aList:
        x = item.find('"')+1
        y = item.find('"', x)
        eURL = item[x:y]
        url = "https://www.etsjets.org/" + eURL
        uList.append(url)
    for title in tList:
        #print(title)
        x=0
    for url in uList:
        title = tList[x]
        print(issue)
        #iFold = issue.split()[1]
        iFold = issue + "." + str(x+1)
        title = getTitle(title, iFold, x+1)
        title = str(x+1) + ") " + title + ".pdf"        
        fPath = "C:/Users/jonat/OneDrive/Documents/JETS/" + vol + "/" + "JETS " + issue + "/" + title
        downloader(url, fPath, title, iFold)
        x = x + 1
def searchURL(url, vol, volN):
    driver = webdriver.Firefox()
    driver.get("https://www.etsjets.org/node/1120")
    emailElement = driver.find_element_by_id("edit-name")
    emailElement.send_keys("jthornenj")
    passElement = driver.find_element_by_id("edit-pass")
    passElement.send_keys("numxsi2W2f")
    submit = driver.find_element_by_id("edit-submit")
    submit.click()
    driver.get(url)
    aList = []
    tList = []
    g = 1
    urls = driver.find_elements_by_tag_name('a')
    for item in urls:
        temp = item.get_attribute('outerHTML')
        inner = item.get_attribute('innerHTML')
        issue = volN + "." + str(g)
        if "/node/" in temp and "JETS" in inner:
            x = temp.find('"') + 1
            y = temp.find('"', x)
            eURL = temp[x:y]
            url = "https://www.etsjets.org" + eURL
            aList.append(url)
            tList.append(inner)
        elif issue in inner:
            x = temp.find('"') + 1
            y = temp.find('"', x)
            eURL = temp[x:y]
            url = "https://www.etsjets.org" + eURL
            aList.append(url)
            tList.append(inner)
            fPath = "C:/Users/jonat/OneDrive/Documents/JETS/" + vol
            if not os.path.exists(fPath):
                os.mkdir(fPath)
            fPath = "C:/Users/jonat/OneDrive/Documents/JETS/" + vol + "/JETS " + inner + "/"
            if not os.path.exists(fPath):
                os.mkdir(fPath)
            print(inner)
            test2(inner, url, 0, vol, driver)
            g = g + 1
    os.sys.exit()
    
