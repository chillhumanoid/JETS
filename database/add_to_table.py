from database import executor, search
from database.util import quotate

def articles(full_number, volume_number, issue_number, article_number, article_title, author_ids):
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
    article_exists = search.articles_table(full_number)
    if not article_exists:
        if "'" in article_title:
            article_title = article_title.replace("'", "''")
        article_title = "'" + article_title + "'"
        sql = "INSERT INTO titles (full_number, volume_number, issue_number, article_number, article_title) VALUES(%s, %s, %s, %s, %s)" % (quotate(full_number), volume_number, issue_number, article_number, article_title)
        executor.execute(sql)
        article_id = get_article_id.by_full_number(full_number)
        for author_id in author_ids:
            sql = "INSERT INTO linker (author_id, article_id) VALUES (%s, %s)" % (author_id, article_id)
            executor.execute(sql)

def author(author_name):
    author_exists = search.author_table(author_name)
    if not author_exists:
        sql = "INSERT INTO authors (author_name) VALUES (%s)" % (quotate(author_name))
        executor.execute(sql)
