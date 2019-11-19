from database import executor, get_article_id

def all():
    """
    Get all the author names

    Locations: rename.get_old_name()

    Returns:
    names (list): a list of all the author names
    """
    names = []
    sql = "SELECT author_name FROM authors"
    c = executor.execute(sql)
    for x in c:
        names.append(x[0])
    return names

def by_full_number(full_number):
    """
    Gets the author based on full number

    Locations: util.get_info()

    Parameters:
    full_number (string)

    Returns:
    author_list (list)
    """
    article_id = get_article_id.by_full_number(full_number)
    author_list = by_article_id(article_id)
    return author_list

def by_article_id(article_id):
    sql = "SELECT author_id FROM linker WHERE article_id = %s" % article_id
    c = executor.execute(sql)
    author_list = []
    for lis in c:
        name = by_author_id(lis[0])
        author_list.append(name)
    return author_list

def by_author_id(author_id):
    sql = "SELECT author_name from authors WHERE author_id = %s" % author_id
    c = executor.execute(sql).fetchall()
    return c[0][0]
