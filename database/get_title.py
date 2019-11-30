from database import executor

def by_article_id(article_id):
    """
    Get the title based on article id

    Locations: display.display_articles(), rename.rename()

    Parameters:
    article_id (int)

    Returns:
    title (string)
    """
    sql = "SELECT article_title FROM articles WHERE article_id = {}".format(article_id)
    c = executor.select(sql)
    return c[0][0]

def all():
    """
    Get all the titles

    Returns:
    titles (list): a list of all the titles in the table
    """
    titles = []
    sql = "SELECT article_title, full_number FROM articles"
    c = executor.select(sql)
    for x in c:
        titles.append((x[0], x[1]))
    return titles
