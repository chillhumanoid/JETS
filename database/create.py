from database import executor

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
    executor.execute(sql)
    sql = """CREATE TABLE IF NOT EXISTS titles (
        article_id integer PRIMARY KEY,
        full_number text NOT NULL,
        volume_number int,
        issue_number int,
        article_number int,
        article_title text NOT NULL
    );"""
    executor.execute(sql)
    sql = """CREATE TABLE IF NOT EXISTS linker (
        article_id integer NOT NULL,
        author_id integer NOT NULL,
        FOREIGN KEY (article_id) REFERENCES titles(article_id),
        FOREIGN KEY (author_id) REFERENCES authors(author_id)
    );"""
    executor.execute(sql)
