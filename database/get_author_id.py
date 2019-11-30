from database import executor

def by_name(author_name):
    """
    Gets the author ID

    Locations: rename.change()

    Parameters:
    author_name(string)

    Returns:
    c[0][0] (int): technically is the author_id
    """
    sql = "SELECT author_id FROM authors WHERE author_name = '{}'".format(author_name)
    c = executor.select(sql)
    return c[0][0]

def by_article_id(article_id):
    sql = "SELECT author_id FROM linker WHERE article_id = {}".format(article_id)
    c = executor.select(sql)
    author_id_list = []
    for lis in c:
        author_id_list.append(lis[0])
    return author_id_list
