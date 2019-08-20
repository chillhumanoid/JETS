import sqlite3, os, click, util
path = os.path.realpath(__file__)
path = path.replace("database.py","")
path = path + "Articles/"

def sql_executor(sql):
    conn = sqlite3.connect(path + "author.db")
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    return c

def create_database():
    sql = """CREATE TABLE IF NOT EXISTS authors (
        id integer PRIMARY KEY,
        name text NOT NULL,
        articlenums text
    );"""
    sql_executor(sql)
    
def get_names():
    names = []
    sql = "SELECT name FROM authors"
    c = sql_executor(sql)
    for x in c:
        names.append(x[0])
    return names

def search_table(author_name):
    sql = "SELECT * FROM authors WHERE name = %s" % quotify(author_name)
    c = sql_executor(sql)
    data = c.fetchall()
    if len(data) == 0:
        value = False
    else:
        value = True
    return value

def sort_articles(new_number, existing_numbers):
    numbers = existing_numbers.split(";")
    new_numbers = new_number.split(";")
    
    replace_position = -1

    for new_number in new_numbers:
        new_volume_number           =  new_number.split(".")[0]
        new_index_number            =  new_number.split(".")[1]
        new_article_number          =  new_number.split(".")[2]

        for index, number in enumerate(numbers):
            existing_volume_number  =  number.split(".")[0]
            existing_index_number   =  number.split(".")[1]
            existing_article_number =  number.split(".")[2]

            if new_volume_number == existing_volume_number and new_index_number == existing_index_number and new_article_number == existing_article_number:
                click.echo("Article Already Added")
                replace_position = -2
            elif new_volume_number == existing_volume_number and new_index_number == existing_index_number and new_article_number > existing_article_number:
                replace_position = index
                break
            elif new_volume_number == existing_volume_number and new_index_number > existing_index_number:
                replace_position = index
                break
            elif new_volume_number > existing_volume_number:
                replace_position = index
                break
            
        if replace_position > -2:
            if replace_position == -1:
                numbers.append(new_number)
            else:
                numbers.insert(replace_position, new_number)
    return numbers

def rename_author(id, new_author_name):
    if search_table(new_author_name): #if the name already is in the table
        sql = "SELECT articlenums FROM authors WHERE id=%s" % id
        c = sql_executor(sql).fetchall()
        article_number_old = c[0][0]
        sql = "SELECT articlenums FROM authors WHERE name=%s" % quotify(new_author_name)
        c = sql_executor(sql).fetchall()
        article_numbers_new = c[0][0]
        full_number = sort_articles(article_number_old, article_numbers_new)
        full_number = ";".join(full_number)
        sql = "UPDATE authors SET articlenums = %s WHERE name = %s" %(quotify(full_number),quotify(new_author_name))
        remove_author(id)
    else:
        sql = "UPDATE authors SET name = %s WHERE id = %s" %(quotify(new_author_name), id)
    sql_executor(sql)

def get_id(author_name):
    sql = "SELECT id FROM authors WHERE name = %s" % quotify(author_name)
    c = sql_executor(sql).fetchall()
    return c[0][0]

def add_to_table(author_name, article_numbers):
    if search_table(author_name):
        full_number = sort_articles(article_numbers, get_numbers(author_name))
        full_number = ";".join(full_number)
        sql = "UPDATE authors SET articlenums = %s WHERE name = %s" % (quotify(full_number), quotify(author_name))
    else:
        sql = "INSERT INTO authors(name, articlenums) VALUES (%s, %s)" % (quotify(author_name), quotify(article_numbers))
    conn = sqlite3.connect(path + "author.db")
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()

def print_table():
    conn = sqlite3.connect(path + "author.db")
    c = conn.cursor()
    for row in c.execute('SELECT * FROM authors ORDER BY name ASC'):
        click.echo(row)
    conn.close()

def remove_author(author_name):
    if type(author_name) == int:
        sql = "DELETE FROM authors WHERE id = %s" % author_name
    else:
        sql = "DELETE FROM authors WHERE name = %s" % quotify(author_name)
    sql_executor(sql)

def get_numbers(author_name):
    sql = "SELECT articlenums FROM authors WHERE name = %s" % quotify(author_name)
    c = sql_executor(sql)
    data = c.fetchall()
    full_number = data[0][0]
    full_number = full_number.split("'")[0]
    return full_number

def get_full_numbers(author_name):
    sql = "SELECT articlenums FROM authors WHERE name = %s" % quotify(author_name)
    c = sql_executor(sql).fetchall()
    full_number = c[0][0]
    full_numbers = full_number.split(";")
    return full_numbers

def remove_article_number(author_name, article_number):
    full_numbers = get_full_numbers(author_name)
    if article_number in full_numbers:
        full_numbers.remove(article_number)
    full_numbers = ";".join(full_numbers)
    sql = "UPDATE authors SET articlenums = %s WHERE name = %s" %(quotify(full_numbers), quotify(author_name))
    sql_executor(sql)
    
def quotify(string):
    if "'" in string:
        string = '"' + string + '"'
    else:
        string = "'" + string + "'"
    return string