import util, click, os, shutil, database as db

path = os.path.realpath(__file__)
path = path.replace("display.py","")
path = path + "Articles/All/"

columns, rows = shutil.get_terminal_size(fallback=(80, 24))

def display(articles):
    title_display_len = get_longest(articles) + 2
    display_header(title_display_len)
    display_articles(articles, title_display_len)

def get_longest(articles):
    u = 0
    for article in articles:
        title = article.split(" - ", 1)[1]
        title = title.split(".pdf")[0]
        z = len(title)
        if z > u:
            u = z
    col = columns - 43
    if u > col:
        u = col
    return u

def display_header(title_len):
    header = "{0:^11}|  {1:^{3}}|{2:^30}".format("ARTICLE", " TITLE", "AUTHOR", title_len)
    lines = get_lines(header, title_len)
    line, line2 = lines[0], lines[1]
    util.p(line)
    click.echo(header)
    click.echo(line2)

def get_lines(header, title_len):
    lChar = u"\u2015"
    line = ""
    line2 = ""
    for x in range(len(header)): #seems self explanatory (update: no it doesnt)
        if x == 11 or x == 13 + title_len:
            line2 = line2 + "|"
            line = line + lChar
        line = line + lChar
        line2 = line2 + lChar
    return (line, line2)

def display_articles(articles, title_len):
    title_len = int(title_len)
    max_length = columns - 43
    for article in articles:
            num = util.get_nums(article)[0]
            title = util.get_info(path + article)[0]
            author_list = db.get_author(num)
            if len(author_list) > 1:
                author = get_authors(author_list)
            else:
                author = author_list[0]
            if len(author) > 30:
                author = author[:27] + "..."
            if len(title) > max_length:
                title = title[:max_length] 
            display = "{0:^11}|  {1:<{3}}| {2:<30}".format(num, title, author, title_len)
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
            last_name = full_name[last_location]
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
