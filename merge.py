import os, sys, util, database as db
from PyPDF2 import PdfFileReader, PdfFileWriter

path = os.path.realpath(__file__)
path = path.replace("merge.py","")
merge_path = path + "Articles/Merged/"
all_path = path + "Articles/All/"

def merge_all():
    volume_list = db.get_all_volumes()
    for volume in volume_list:
        if volume >= 1 and volume <= 9:
            volume = "0" + str(volume)
        else:
            volume = str(volume) 
        folder = "Vol " + volume
        merge_articles(db.get_article_by_volume_number(volume), 1, folder, 0)

        issue_list = db.get_all_issues_in_volume(volume)
        for issue in issue_list:
            issue = "0" + str(issue)
            folder = "Vol " + volume
            merge_articles(db.get_article_by_issue_number(volume, issue), 2, folder, issue)


def merge(volume_number, issue_number):
    article_id_list = 0
    identifier = None
    if issue_number == "0":
        article_id_list = db.get_article_by_volume_number(volume_number)
        identifier = 1
    else:
        article_id_list = db.get_article_by_issue_number(volume_number, issue_number)
        identifier = 2
    folder = "Vol " + volume_number
    merge_articles(article_id_list, identifier, folder, issue_number)

def merge_articles(article_id_list, identifier, folder, issue_number):
    merged_path = merge_path + folder + "/"
    if not os.path.exists(merged_path):
        os.mkdir(merged_path)
    if identifier == 1:
        output = merged_path + folder + ".pdf"
    elif identifier == 2:
        output = merged_path + "Issue " + issue_number + ".pdf"
    file_out = open(output, 'ab')
    writer = PdfFileWriter()
    for article_id in article_id_list:
        article = str(article_id) + ".pdf"
        article_file = open(all_path + article, 'rb')
        print(article)
        pdf = PdfFileReader(article_file)
        for page in range(pdf.getNumPages()):
            writer.addPage(pdf.getPage(page))
        writer.write(file_out)
        article_file.close()
    file_out.close()

