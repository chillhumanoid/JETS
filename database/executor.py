import sqlite3

path = "C:/Users/jonat/JETS/Articles/"
def execute(sql):
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
