import requests
import urllib.request
import time
import os
from bs4 import BeautifulSoup
import issues
def getNode():
    #since this is the first function called, lets check for directory existence
    path = "C:/Users/jonat/OneDrive/Documents/JETS"
    if not os.path.exists(path):
        os.mkdir(path)
    url = 'https://www.etsjets.org/JETS_Online_Archive' #where the archives are held
    response = requests.get(url) 
    soup = BeautifulSoup(response.text, "html.parser")
    node_list = soup.findAll('a') #gets all links
    nList = []
    for x in range(33, len(node_list)):
        nList.append(node_list[x])
    node_list = nList
    for x in range(57,58):
        nodeURLGet(node_list[x])
def shortenNode(node_list):
    nNList = []
    for x in range(33, len(node_list)-2): #first 32 links aren't needed, last 2 aren't needed
        nNList.append(node_list[x]) #append to new list
    return nNList #return new list

def printNodeList(node_list): #print the node list (dev purposes)
    for x in range(len(node_list)):
        print(node_list[x]) #breaks down per line

def volFolderMaker(node):
    node = str(node) #convert to str
    x = node.find(">") + 1 #find the first >
    y = node.find("<", x)
    if node[x] == " ":
        x = x + 1
        if node[x] == " ":
            x = x + 1
    volFold = node[x:y]
    path = "C:/Users/jonat/OneDrive/Documents/JETS/" + volFold
    if not os.path.exists(path):
        os.mkdir(path)
        print("SUCCESS - " + volFold + " folder created")
    else:
        print("IGNORED - " + volFold + " - already existed")

def volFolderGetter(node):
    node = str(node)
    x = node.find(">") + 1
    y = node.find("<", x)
    if node[x] == " ":
        x = x + 1
        if node[x] == " ":
            x = x + 1
    volFold = node[x:y]
    return volFold

def nodeURLGet(node):
    node = str(node)
    x = node.find('"') + 1
    y = node.find('"', x)
    nodeURL = "https://www.etsjets.org" + node[x:y]
    issues.getIssues(nodeURL, volFolderGetter(node))
