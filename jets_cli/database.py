import sqlite3, os, click, util
path = os.path.realpath(__file__)
path = path.replace("database.py","")
path = path + "Articles/"

def create_database():
    print(path)
    conn = sqlite3.connect(path + 'author.db')
    c = conn.cursor()
    exestatement = """CREATE TABLE IF NOT EXISTS authors (
        id integer PRIMARY KEY,
        name text NOT NULL,
        articlenums text
    );"""
    c.execute(exestatement)
    conn.close()

def search_table(author_name):
    sql = "SELECT * FROM authors WHERE name = %s" % author_name
    conn = sqlite3.connect(path + "author.db")
    c = conn.cursor()
    data = c.execute(sql).fetchall()
    if len(data) == 0:
        value = False
    else:
        value = True
    conn.close()
    return value

def sort_articles(new_number, existing_numbers):
    new_vol = new_number.split(".")[0]
    new_index = new_number.split(".")[1]
    new_article = new_number.split(".")[2]
    numbers = existing_numbers.split(";")
    replace_position = -1
    
    for index, number in enumerate(numbers):

        existing_vol = number.split(".")[0]
        existing_index = number.split(".")[1]
        existing_article = number.split(".")[2]
        print(existing_vol)
        if new_vol == existing_vol:
            if new_index == existing_index:
                if new_article == existing_article:
                    click.echo("Article Already Added")
                    replace_position = -2
                    break
                
                elif new_article > existing_article:
                    replace_position = index
                    break
            elif new_index > existing_index:
                replace_position = index
                break
        elif new_vol > existing_vol:
            replace_position = index
            break
    
    if replace_position > -2:
        if replace_position == -1:
           numbers.append(new_number)
           y = 0
        else:
            numbers.insert(replace_position, new_number)
            y = 0
    return numbers

def add_to_table(author_name, article_nums):
    author_name = "'" + author_name + "'"
    if search_table(author_name):
        full_num = sort_articles(article_nums, get_numbers(author_name))
        full_num = ";".join(full_num)
        full_num = "'" + full_num + "'"
        sql = "UPDATE authors SET articlenums = %s WHERE name = %s" % (full_num, author_name)
    else:
        article_nums = "'" + article_nums + "'"
        sql = "INSERT INTO authors(name, articlenums) VALUES (%s, %s)" % (author_name, article_nums)
    conn = sqlite3.connect(path + "author.db")
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()

def print_table():
    sql = """SELECT * FROM authors"""
    conn = sqlite3.connect(path + "author.db")
    c = conn.cursor()
    for row in c.execute('SELECT * FROM authors'):
        print(row)
    conn.close()

def remove_author(author_name):
    sql = "DELETE FROM authors WHERE name = %s" % "'" + author_name + "'"
    conn = sqlite3.connect(path + "author.db")
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()

def get_numbers(author_name):
    sql = "SELECT articlenums FROM authors WHERE name = %s" % author_name
    conn = sqlite3.connect(path + "author.db")
    c = conn.cursor()
    data = c.execute(sql).fetchall()
    data = data[0]
    full_num = data[0]
    full_num = full_num.split("'")[0]
    conn.close()
    return full_num

def get_full_numbers(author_name):
    sql = "SELECT articlenums FROM authors WHERE name = %s" % author_name
    conn = sqlite3.connect(path + "author.db")
    c = conn.cursor()
    data = c.execute(sql).fetchall()
    data = data[0]
    full_num = data[0]
    full_nums = full_num.split(";")

    conn.close()
    return full_nums
