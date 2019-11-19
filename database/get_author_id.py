from database import executor
from database.util import quotate

def by_name(author_name):
    """
    Gets the author ID

    Locations: rename.change()

    Parameters:
    author_name(string)

    Returns:
    c[0][0] (int): technically is the author_id
    """
    sql = "SELECT author_id FROM authors WHERE author_name = %s" % quotate(author_name)
    c = executor.execute(sql).fetchall()
    return c[0][0]

def by_article_id(article_id):
    sql = "SELECT author_id FROM linker WHERE article_id = %s" % article_id
    c = executor.execute(sql).fetchall()
    author_id_list = []
    for lis in c:
        author_id_list.append(lis[0])
    return author_id_list
