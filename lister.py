##imports
import sys, os, re, time
import search, util
from database import get_article_id
from database import get_article
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
        article_ids = get_article_id.all()
        display(article_ids)
    if not volume_number == "0" and issue_number == "0":
        volume_number = util.check_digit(volume_number)
        article_ids = get_article.by_volume(int(volume_number))
        display(article_ids)
    if not volume_number == "0" and not issue_number == "0":
        volume_number = util.check_digit(volume_number)
        issue_number = util.check_digit(issue_number)
        article_ids = get_article.by_issue(int(volume_number), int(issue_number))
        display(article_ids)
