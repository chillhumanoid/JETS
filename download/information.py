from download import fileparser as parsr
import util, known_authors

def get_title_from_link(link):
    title_start = link.find('>') + 1
    title_end   = link.find('<', title_start)
    title       = link[title_start:title_end]
    return title

def get_title(title):
    original_file_name = title
    count              = title.count(". . .")
    article_title      = parsr.get_raw_title(count, original_file_name)
    return article_title

def get_author_name(original_file_name):
    count = original_file_name.count(". . .")
    author_name        = parsr.get_raw_author(count, original_file_name)
    author_name        = known_authors.change_known_authors(author_name)
    return author_name

def get_full_number(data):
    return get_volume_number(data) + "." + get_issue_number(data) + "." + get_article_number(data)

def get_volume_number(data):
    return util.check_digit(data[0])

def get_issue_number(data):
    return util.check_digit(data[1])

def get_article_number(data):
    return util.check_digit(data[2])
