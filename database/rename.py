from database import executor, get_author_id, search
from database.util import quotate

def author(author_id, new_author_name):
    """
    Rename the author in the author database

    Locations: rename.change(), rename.rename()

    If the new author name already exists(unlikely), remove the old author, get the new id, and set the author_id in the titles database on the correct id

    Parameters:
    author_id (integer)
    new_author_name(string)
    """
    if search.author_table(new_author_name):
        new_author_id = get_author_id.by_name(new_author_name)
        sql = "UPDATE linker SET (author_id) VALUES (%s) WHERE author_id = %s" % (new_author_id, author_id)
        executor.execute(sql)
        sql = "DELETE FROM authors WHERE author_id = %s" % author_id
        executor.execute(sql)
    else:
        sql = "UPDATE authors SET author_name = %s WHERE author_id = %s" % (quotate(new_author_name), author_id)
        executor.execute(sql)

def title(article_id, new_title):
    """
    Updates title if changed

    Locations: rename.rename()

    Parameters:
    article_id (int)   : identifier for article
    new_title (string) : The new title to set
    """
    sql = "UPDATE titles SET title = %s WHERE article_id = %s" % (quotate(new_title), article_id)
    executor.execute(sql)
