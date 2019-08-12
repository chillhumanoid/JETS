import util, click, os

path = os.path.realpath(__file__)
path = path.replace("display.py","")
path = path + "Articles/All/"

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
    return u

def display_header(title_len):
    header = "{0:^11}|  {1:^{3}}|{2:^16}".format("ARTICLE", " TITLE", "AUTHOR", title_len)
    lines = get_lines(header, title_len)
    line, line2 = lines[0], lines[1]
    util.p(line)
    click.echo(header)
    click.echo(line2)

def get_lines(header, title_len):
    lChar = u"\u2015"
    line = ""
    line2 = ""
    for x in range(len(header) + 8): #seems self explanatory
        if x == 11 or x == 13 + title_len:
            line2 = line2 + "|"
            line = line + lChar
        line = line + lChar
        line2 = line2 + lChar
    return (line, line2)

def display_articles(articles, title_len):
    title_len = int(title_len)
    for article in articles:
            num = util.get_nums(article)[0]
            title = util.getInfo(path + article)[0]
            author = util.getInfo(path + article)[1]
            display = "{0:^11}|  {1:<{3}}|  {2}".format(num, title, author, title_len)
            click.echo(display)

def get_authors(author):
    a = ''
    if " And " in author:
        authors = []
        auth_split = author.split(" And ")
        for name in auth_split:
            if "," in name:
                auth_split_again = a.split(",")
                for auth in auth_split_again:
                    auth = util.sStrip()
                    if not auth == "":
                        authors.append(auth)
                    else:
                        authors.append(a)
            fullName = []
            for name in authors:
                first = name[0:1] + "."
                full_name = name.split(" ")
                full_name[0] = first
                if "Jr" in full_name or "III" in full_name:
                    last_location = len(full_name) - 2
                else:
                    last_location = len(full_name) - 1
                    last = full_name[last_location]
                    if not last_location == 1:
                        full_name = get_middle(last_location, full_name)
                    a = ' '.join(full_name)
                    fullName.append(a)
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
