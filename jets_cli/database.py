import sqlite3, os, click, util, sys, time
path = os.path.realpath(__file__)
path = path.replace("database.py","")
path = path + "Articles/"
all_path = path + "/All"
def sql_executor(sql):
    """
    Executes SQL code

    Instead of executing in each function, executes in this base function

    Parameters:
    sql (string): SQL query to be executed

    Returns:
    c (sql query) : whatever was in the query, gets returned to the function that called it
    """
    conn = sqlite3.connect(path + "author.db")
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    return c



def create_database():
    """
    Creates database on first run

    If the database doesn't exist, or the tables don't exist, it creates the tables needed for authors and titles. 

    Created tables: \n
    authors : holds the author ids and the author names \n
    titles : holds the article info and connects to the authors table
    """
    sql = """CREATE TABLE IF NOT EXISTS authors (
        author_id integer PRIMARY KEY,
        author_name text NOT NULL
    );"""
    sql_executor(sql)
    sql = """CREATE TABLE IF NOT EXISTS titles (
        article_id integer PRIMARY KEY,
        full_number text NOT NULL,
        volume_number int,
        issue_number int,
        article_number int,
        article_title text NOT NULL
    );"""
    sql_executor(sql)
    sql = """CREATE TABLE IF NOT EXISTS linker (
        article_id integer NOT NULL, 
        author_id integer NOT NULL,
        FOREIGN KEY (article_id) REFERENCES titles(article_id),
        FOREIGN KEY (author_id) REFERENCES authors(author_id)
    );"""
    sql_executor(sql)
    


def get_all_article_ids():
    """
    Get all the article IDs

    Returns:
    article_id_list (list): list of the article ids
    """
    sql = "SELECT article_id FROM titles"
    c = sql_executor(sql)
    article_id_list = []
    for x in c:
        article_id_list.append(x[0])
    return article_id_list



def get_all_titles():
    """
    Get all the titles

    Returns:
    titles (list): a list of all the titles in the table
    """
    titles = []
    sql = "SELECT article_title FROM titles"
    c = sql_executor(sql)
    for x in c:
        titles.append(x[0])
    return titles



def get_all_names(): 
    """
    Get all the author names

    Locations: rename.get_old_name()

    Returns:
    names (list): a list of all the author names
    """ 
    names = []
    sql = "SELECT author_name FROM authors"
    c = sql_executor(sql)
    for x in c:
        names.append(x[0])
    return names

    """
    Search the articles table for a specific article

    Parameters:
    full_number (string): if the full_number is in the table, gets information

    Returns:
    True  : the article number was found, item in table
    False : article number was not found, item not in table
    """
    c = sql_executor(sql)
    data = c.fetchall()
    if len(data) == 0:
        return = False
    else:
    """
    Search the author table for a specific author

    Parameters:
    author_name (string): the author name to search

    Returns:
    True  : the author was found, item in table
    False : author was not found, item not in table
    """ 
    c = sql_executor(sql)
    data = c.fetchall()
    if len(data) == 0:
        return False
    else:
        return True

def sort_articles(new_number, existing_numbers):
    numbers = existing_numbers.split(";")
    new_numbers = new_number.split(";")
    
    replace_position = -1

    """
    Rename the author in the author database

    Locations: rename.change(), rename.rename()

    If the new author name already exists(unlikely), remove the old author, get the new id, and set the author_id in the titles database on the correct id
            
    Parameters:
    author_id (integer)
    new_author_name(string)
    """
            else:
    """
    Gets the author ID

    Locations: rename.change()

    Parameters:
    author_name(string)

    Returns:
    c[0][0] (int): technically is the author_id
    """
        c = sql_executor(sql).fetchall()
    """
    Adds new article to articles table

    Parameters:\n
    full_number    (string)  : Easy identifier, ##.##.## (vol.issue.article)\n
    volume_number  (int)     : Lone identifier for volume\n
    issue_number   (int)     : Lone identifier for issue\n
    article_number (int)     : Lone identifier for article\n
    article_title  (string)  : the title of the article\n
    author_id      (str)     : the ID(s) of the author(s) \n
    """
    sql_executor(sql)

    """
    Get the title based on article id
    
    Locations: display.display_articles(), rename.rename()
    
    Parameters:
    article_id (int)

    Returns:
    title (string)
    """
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

    """
    Gets the author based on full number

    Locations: util.get_info()

    Parameters:
    full_number (string)

    Returns:
    author_list (list)
    """
    c = sql_executor(sql).fetchall()
    author_list = []
    for lis in c:
        author_list.append(lis[0])
    return author_list

def print_table():
    conn = sqlite3.connect(path + "author.db")
    c = conn.cursor()
    for row in c.execute('SELECT * FROM authors ORDER BY name ASC'):
        click.echo(row)
    conn.close()

    """
    Gets the full number based on article id

    Current locations: display.display_articles()

    Parameters:
    article_id (int)

    Returns:
    full_number (string)
    """
    """
    gets article_ids based on author name

    Parameters:
    author_name (string)

    Returns: 
    article_id_list (list)
    """
def remove_article(full_number):
    article_id = get_article_id(full_number)
    sql = "DELETE FROM titles WHERE full_number = %s" %(quotate(full_number))
    sql_executor(sql)
    sql = "DELETE FROM linker WHERE article_id = %s" % article_id
    sql_executor(sql)
    os.remove(all_path + str(article_id) + ".pdf")


    """
    Updates title if changed

    Locations: rename.rename()

    Parameters:
    article_id (int)   : identifier for article
    new_title (string) : The new title to set
    """
    sql_executor(sql)
    
def quotify(string):
    if "'" in string:
        string = '"' + string + '"'
    else:
        string = "'" + string + "'"
    return string