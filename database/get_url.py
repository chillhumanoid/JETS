import webbrowser
from database import executor
def by_article_id(article_id):
    sql = "SELECT article_url FROM articles WHERE article_id = {}".format(article_id)
    c = executor.select(sql)
    if len(c) > 0:
        url = c[0][0]
        webbrowser.open(url)
