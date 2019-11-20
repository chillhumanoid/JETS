import os, sys, subprocess, click, database as db, util

path = os.getcwd() + "/"
path = path.replace("utilities/open.py","")
all_path = path + "Articles/All/"
merged_path = path + "Articles/Merged/"

def open_merged_file(volume_number, issue_number):
    if issue_number == 0:
        check_statement = "Vol " + str(volume_number) + ".pdf"
    else:
        check_statement = "Issue " + str(issue_number) + ".pdf"
    for directory in os.listdir(merged_path):
        if directory == "Vol " + volume_number:
            merge_path = merged_path + directory + "/"
            for merged_file in os.listdir(merge_path):
                if merged_file == check_statement:
                    os.startfile(merge_path + merged_file)

def open_author(author_name):
    """
    Open all articles by a specific author

    Parameters:
    author_name (string)
    """
    author_exists = db.search_author_table(author_name)
    if author_exists:
        article_id_list = db.get_article_ids(author_name)
        number_of_articles = str(len(article_id_list))
        if click.confirm("Are you sure you want to open all " + number_of_articles + " articles by " + author_name + "?"):
            for article_id in article_id_list:
                os.startfile(all_path + str(article_id) + ".pdf")
    else:
        util.p("Author not found")

def open_file(full_number):
    """
    Open a specific file based on the full number(volume.issue.article ##.##.##)

    Parameters:
    full_number (string)
    """
    x = 0
    article_id = db.get_article_id.by_full_number(full_number)
    for article in os.listdir(all_path):
        if str(article_id) + ".pdf" == article:
            os.startfile(all_path + article)
            x = x + 1
    if x == 0:
        print("Article Not Found")
