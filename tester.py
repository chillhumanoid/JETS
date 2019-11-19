import sqlite3
def main():
    path = "C:/Users/jonat/JETS/Articles/"
    conn = sqlite3.connect(path + "author.db")
    c = conn.cursor()
    sql = "Select * FROM titles"
    for row in c.execute(sql):
        print(row)
    conn.commit()
main()
