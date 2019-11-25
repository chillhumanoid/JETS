from database import get_author, get_article, get_numbers, get_article_id
from utilities import sort_dict, variables as var
from menus import main

def volume():
    vol = get_numbers.volumes()
    return sorted(vol)

def issue():
    display_list = sorted(get_numbers.issues_in_volume(var.volume_number))
    display_list.insert(0, "All")
    return display_list

def articles():
    if var.issue_number == "All":
        return get_article.by_volume(var.volume_number)
    else:
        return get_article.by_issue(var.volume_number, var.issue_number)

def authors(sort_int):
    names = get_author.all()
    if sort_int == None:
        sort_int == 1
    names_dict = sort_dict.create(names)
    return sort_dict.sort(names_dict, sort_int)

def author_articles():
    return get_article_id.by_author(var.author_name)
