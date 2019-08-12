##imports
import sys, os, re
from jets_cli import search, util
from PyPDF2 import PdfFileReader, PdfFileWriter
from shutil import copyfile

##global variables
path = os.path.realpath(__file__)
path = path.replace("lister.py","")
path = path + "Articles/All"

##functions
def listing(vNum, iNum):
    if vNum == "0" and iNum == "0":
        listAll()
    if not vNum == "0" and iNum == "0":
        vNum = util.check_digit(vNum)
        listInVol(vNum)
    if not vNum == "0" and not iNum == "0":
        vNum = util.check_digit(vNum)
        iNum = util.check_digit(iNum)
        listInIssue(vNum, iNum)

def listAll():
    articles = []
    for article in os.listdir(path):
        articles.append(article)
    util.display_info(articles)

def listInVol(vNum):
    articles = []
    for article in os.listdir(path):
        if article.startswith(vNum + "."):
            articles.append(article)
    util.display_info(articles)

def listInIssue(vNum, iNum):
    articles = []
    for article in os.listdir(path):
        if article.startswith(vNum + "." + iNum + "."):
            articles.append(article)
    util.display_info(articles)
