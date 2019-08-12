##imports
import sys, os, re
import search, util
from display import display
from PyPDF2 import PdfFileReader, PdfFileWriter
from shutil import copyfile

##global variables
path = os.path.realpath(__file__)
path = path.replace("lister.py","")
path = path + "Articles/All"

##functions
def start(vNum, iNum):
    if vNum == "0" and iNum == "0":
        list_all()
    if not vNum == "0" and iNum == "0":
        vNum = util.check_digit(vNum)
        list_vol(vNum)
    if not vNum == "0" and not iNum == "0":
        vNum = util.check_digit(vNum)
        iNum = util.check_digit(iNum)
        list_issue(vNum, iNum)

def list_all():
    articles = []
    for article in os.listdir(path):
        articles.append(article)
    display(articles)

def list_vol(vNum):
    articles = []
    for article in os.listdir(path):
        if article.startswith(vNum + "."):
            articles.append(article)
    display(articles)

def list_issue(vNum, iNum):
    articles = []
    for article in os.listdir(path):
        if article.startswith(vNum + "." + iNum + "."):
            articles.append(article)
    display(articles)
