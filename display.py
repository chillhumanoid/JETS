import util, click, os, shutil, database as db
from database import get_numbers

path = os.path.realpath(__file__)
path = path.replace("display.py","")
path = path + "Articles/All/"

columns, rows = shutil.get_terminal_size(fallback=(80, 24))
columns = columns - 1

def display(article_ids):
    """Starting function of the display script

    Parameters:
    article_ids (list): the article_id's of the articles to display

    """
    title_display_len = get_longest(article_ids) + 2                                               #gets the longest title so it knows display parameters

    display_header(title_display_len)                                                             #display the header first

    display_articles(article_ids, title_display_len)                                               #continue to display the articles after

def get_longest(article_ids):
    """Gets the longest title in a list of articles

    Parameters:
    article_id (list): the article_id's of the articles to display
    """
    longest_len              = 0                                                                  #init variable
    for article_id in article_ids:                                                                #does need to be changed
        title                = db.get_title.by_article_id(article_id)
        current_len          = len(title)
        if current_len > longest_len:
            longest_len      = current_len
    max_title_length         = columns - 45
    if longest_len > max_title_length:
        longest_len          = max_title_length
    return longest_len

def display_header(title_len):
    header                   = "{0:^11}| {1:^{3}}  |{2:^26}".format("ARTICLE", " TITLE", "AUTHOR", title_len)
    lines                    = get_lines(header, title_len)
    line, line2              = lines[0], lines[1]

    util.p(line)
    click.echo(header)
    click.echo(line2)

def get_lines(header, title_len):
    lChar                    = u"\u2015"
    line                     = ""
    line2                    = ""

    for x in range(len(header) - 4): #seems self explanatory (update: no it doesnt)
        if x == 11 or x == 14 + title_len:
            line2            = line2 + "|"
            line             = line + lChar
        line                 = line + lChar
        line2                = line2 + lChar
    return (line, line2)

def display_articles(article_ids, title_len):
    title_len = int(title_len)
    max_length = columns - 46
    for article_id in article_ids:
            full_number = get_numbers.full(article_id)
            title = db.get_title.by_article_id(article_id)
            author_list = db.get_author.by_full_number(full_number)
            if len(author_list) > 1:
                author = get_authors(author_list)
            else:
                author = author_list[0]
            if len(author) > 26:
                author = author[:23] + "..."
            if len(title) > max_length:
                title = title[:max_length] + "..."
            display = "{0:^11}|  {1:<{3}} | {2:<26}".format(full_number, title, author, title_len)
            click.echo(display)

def get_authors(author_list):
    fullName = []
    for name in author_list:
        first_name = name[0:1] + "."
        full_name = name.split(" ")
        full_name[0] = first_name
        if "Jr" in full_name or "III" in full_name:
            last_location = len(full_name) - 2
        else:
            last_location = len(full_name) - 1
            if not last_location == 1:
                full_name = get_middle(last_location, full_name)
            name = ' '.join(full_name)
            fullName.append(name)
    author = ', '.join(fullName)
    return author

def get_middle(location, full_name):
    middle_location = location - 1
    middle = full_name[middle_location]
    if not len(middle) == 2:
        middle = middle[0:1] + "."
        full_name[middle_location] = middle
        if not middle_location <= 1:
            return get_middle(middle_location, full_name)
    return full_name
