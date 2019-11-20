import sqlite3, click
from jets_cli import path

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
    conn.close()\
