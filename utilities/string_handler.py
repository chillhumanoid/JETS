from database import get_numbers, get_title, get_author
from utilities import arith, names, get_year as get
def display_string(article_id, width, menu_type):
    a_len = 26
    number = get_numbers.full(article_id)
    if not menu_type == "author_articles":
        number = number.split(".")[1] + "." + number.split(".")[2]
    title = get_title.by_article_id(article_id)
    author = get_author.by_article_id(article_id)
    author_ = names.get_authors(author)
    display_author = get_display_author(author_, a_len)
    display_title = get_display_title(title, width, a_len, menu_type)
    finString = "{} | {} | {}".format(number, display_title, display_author)
    return finString
def display_volume(display_number, number):
    return "Vol " + display_number + " (" + get.year(number) + ")"

def get_display_author(author, a_len):
    if(len(author) > a_len):
        display_author = author[:a_len - 6]
        display_author = display_author + " . . ."
        return display_author
    else:
        return author
def get_display_title(title, width, a_len, menu_type):
    title_len = arith.get_max_title_len(width, a_len, menu_type)
    if len(title) > title_len:
        title = title[:title_len-3] + " . . ."
    else:
        magic_number = title_len + (3 - len(title))
        magic_string = " " * magic_number
        title = title + magic_string
    return title
def display_number(number):
    if len(number) == 1:
        display_number = "0" + number
    else:
        display_number = number
    return display_number

def get_index_of_letter(letter, list, sort):
    letter = letter.upper()
    check = 0
    if sort == 1 or sort == 3:
        for (item, d) in enumerate(list):
            if d["last"][0] == letter:
                return item
            else:
                check = 1
    elif sort == 2 or sort == 4:
        for (item, d) in enumerate(list):
            if d["first"][0] == letter:
                return item
            else:
                check = 1
    if check == 1:
        return -1
