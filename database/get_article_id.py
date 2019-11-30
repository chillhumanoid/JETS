from database import executor, get_author_id
"""
def all():

    Get all the article IDs

    Returns:
    article_id_list (list): list of the article ids

    sql = "SELECT article_id FROM articles ORDER BY full_number ASC"
    c = executor.select(sql)
    article_id_list = []
    for x in c:
        article_id_list.append(x[0])
    return article_id_list
    """

def by_author(author_name):
    """
    gets article_ids based on author name

    Parameters:
    author_name (string)

    Returns:
    article_id_list (list)
    """
    author_id = get_author_id.by_name(author_name)
    sql = "SELECT article_id FROM linker WHERE author_id = {}".format(author_id)
    c = executor.select(sql)
    article_id_list = []
    for lis in c:
        article_id_list.append(lis[0])
    return article_id_list

def by_full_number(full_number):
    """
    Gets article_id based on full_number

    Locations: rename.rename(), downloader.download()

    Parameters:
    full_number (string) : Vol.issue.article (##.##.##)
    """
    sql = "SELECT article_id FROM articles WHERE full_number = '{}'".format(full_number)
    c = executor.select(sql)
    if len(c) == 0:
        return False
    else:
        return c[0][0]

def by_volume(volume_number):
    """
    Gets article_id based on volume number

    Locations: remove_article.by_article_id

    Parameters:
    volume_number (integer)
    """
    sql = "SELECT article_id FROM articles WHERE volume_number = {}".format(volume_number)
    c = executor.select(sql)
    article_id_list = []
    for lis in c:
        article_id_list.append(lis[0])
    return article_id_list
