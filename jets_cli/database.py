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



def search_articles_table(full_number):
    """
    Search the articles table for a specific article

    Parameters:
    full_number (string): if the full_number is in the table, gets information

    Returns:
    True  : the article number was found, item in table
    False : article number was not found, item not in table
    """
    sql = "SELECT * FROM titles WHERE full_number = %s" %quotate(full_number)
    c = sql_executor(sql)
    data = c.fetchall()
    if len(data) == 0:
        return False
    else:
        return True



def search_author_table(author_name):
    """
    Search the author table for a specific author

    Parameters:
    author_name (string): the author name to search

    Returns:
    True  : the author was found, item in table
    False : author was not found, item not in table
    """ 
    sql = "SELECT * FROM authors WHERE author_name = %s" % quotate(author_name)
    c = sql_executor(sql)
    data = c.fetchall()
    if len(data) == 0:
        return False
    else:
        return True

    

def rename_author(author_id, new_author_name):
    """
    Rename the author in the author database

    Locations: rename.change(), rename.rename()

    If the new author name already exists(unlikely), remove the old author, get the new id, and set the author_id in the titles database on the correct id
            
    Parameters:
    author_id (integer)
    new_author_name(string)
    """
    if search_author_table(new_author_name):
        new_author_id = get_author_id(new_author_name)
        sql = "UPDATE linker SET (author_id) VALUES (%s) WHERE author_id = %s" % (new_author_id, author_id)
        sql_executor(sql)
        sql = "DELETE FROM authors WHERE author_id = %s" % author_id
            else:
        sql = "UPDATE authors SET name = %s WHERE id = %s" %(quotate(new_author_name), author_id) 
        sql_executor(sql)



def get_author_id(author_name):
    """
    Gets the author ID

    Locations: rename.change()

    Parameters:
    author_name(string)

    Returns:
    c[0][0] (int): technically is the author_id
    """
    sql = "SELECT author_id FROM authors WHERE author_name = %s" % quotate(author_name)
        c = sql_executor(sql).fetchall()
    return c[0][0]



def add_to_articles_table(full_number, volume_number, issue_number, article_number, article_title, author_ids):
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
    article_exists = search_articles_table(full_number)
    if not article_exists:
        if "'" in article_title:
            article_title = article_title.replace("'", "''")
        article_title = "'" + article_title + "'"
         
        sql = "INSERT INTO titles (full_number, volume_number, issue_number, article_number, article_title) VALUES(%s, %s, %s, %s, %s)" % (quotate(full_number), volume_number, issue_number, article_number, article_title)
    sql_executor(sql)
        article_id = get_article_id(full_number)
        for author_id in author_ids:
            sql = "INSERT INTO linker (author_id, article_id) VALUES (%s, %s)" % (author_id, article_id)
            sql_executor(sql)



def add_to_author_table(author_name):
    author_exists = search_author_table(author_name)
    print(author_name)
    if not author_exists:
        sql = "INSERT INTO authors (author_name) VALUES (%s)" % (quotate(author_name)) 
        sql_executor(sql)



def get_title(article_id):
    """
    Get the title based on article id
    
    Locations: display.display_articles(), rename.rename()
    
    Parameters:
    article_id (int)

    Returns:
    title (string)
    """
    sql = "SELECT article_title FROM titles WHERE article_id = %s" % article_id
    c = sql_executor(sql).fetchall()
    return c[0][0]



def get_author(full_number):
    """
    Gets the author based on full number

    Locations: util.get_info()

    Parameters:
    full_number (string)

    Returns:
    author_list (list)
    """
    article_id = get_article_id(full_number)
    sql = "SELECT author_id FROM linker WHERE article_id = %s" % article_id
    c = sql_executor(sql).fetchall()
    author_list = []
    for lis in c:
        sql = "SELECT author_name FROM authors WHERE author_id = %s" % lis[0]
        d = sql_executor(sql).fetchall()
        name = d[0][0]
        author_list.append(name)
    return author_list



def print_author_table(): #DEV USE
    conn = sqlite3.connect(path + "author.db")
    c = conn.cursor()
    for row in c.execute('SELECT * FROM authors ORDER BY name ASC'):
        click.echo(row)
    conn.close()



def print_article_table(): #DEV USE
    conn = sqlite3.connect(path + "author.db")
    c = conn.cursor()
    for row in c.execute("SELECT * FROM titles ORDER BY full_number ASC"):
        click.echo(row)
    conn.close()



def get_full_number(article_id):
    """
    Gets the full number based on article id

    Current locations: display.display_articles()

    Parameters:
    article_id (int)

    Returns:
    full_number (string)
    """
    sql = "SELECT full_number FROM titles WHERE article_id = %s" % article_id
    c = sql_executor(sql).fetchall()
    return c[0][0]



def get_article_by_volume_number(volume_number):
    sql = "SELECT article_id FROM titles WHERE volume_number = %s ORDER BY full_number ASC" % volume_number
    c = sql_executor(sql).fetchall()
    article_list = []
    for item in c:
        article_list.append(item[0])
    return article_list



def get_article_by_issue_number(volume_number, issue_number):
    sql = "SELECT article_id FROM titles WHERE volume_number = %s and issue_number = %s ORDER BY full_number ASC" % (volume_number, issue_number)
    c = sql_executor(sql).fetchall()
    article_list = []
    for item in c:
        article_list.append(item[0])
    return article_list



def get_article_ids(author_name):
    """
    gets article_ids based on author name

    Parameters:
    author_name (string)

    Returns: 
    article_id_list (list)
    """
    author_id = get_author_id(author_name)
    sql = "SELECT article_id FROM linker WHERE author_id = %s" % author_id
    c = sql_executor(sql).fetchall()
    article_id_list = []
    for lis in c:
        article_id_list.append(lis[0])
    return article_id_list



def get_article_id(full_number):
    """
    Gets article_id based on full_number

    Locations: rename.rename(), downloader.download()

    Parameters:
    full_number (string) : Vol.issue.article (##.##.##)
    """
    sql = "SELECT article_id FROM titles WHERE full_number = %s" % quotate(full_number)
    c = sql_executor(sql).fetchall()
    return c[0][0]

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