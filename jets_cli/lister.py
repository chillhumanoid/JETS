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

##function
def start(volume_number, issue_number):
    if volume_number == "0" and issue_number == "0":
        article_ids = db.get_all_article_ids()
        display(article_ids)
    if not volume_number == "0" and issue_number == "0":
        volume_number = util.check_digit(volume_number)
        display([article for article in os.listdir(path) if article.startswith(volume_number + ".")])
    if not volume_number == "0" and not issue_number == "0":
        volume_number = util.check_digit(volume_number)
        issue_number = util.check_digit(issue_number)
        display([article for article in os.listdir(path) if article.startswith(volume_number + "." + issue_number + ".")])