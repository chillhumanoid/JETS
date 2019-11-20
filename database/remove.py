from database import executor, get_article_id, get_author, get_author_id
from database.util import quotate
from jets_cli import util, all_path


def article_by_volume(volume_number):
    """
    Allows for removal of articles by volume

    Location: dev use only?

    Parameters:
    volume_number (int)
    """
    article_id_list = get_article_id.by_volume(volume_number)
    for article_id in article_id_list:
        sql = "DELETE FROM titles WHERE article_id = %s" % article_id
        executor.execute(sql)
        delete_linker_article_id(article_id)
        author_id_list = get_author_id.by_article_id(article_id)
        for author_id in author_id_list:
            check_remaining_author(author_id, False)
        os.remove(all_path + str(article_id) + ".pdf")

def remove_article(full_number):
    article_id = get_article_id.by_full_number(full_number)
    author_name = get_author.by_full_number(full_number)[0]
    author_id = get_author_id(author_name)
    sql = "DELETE FROM titles WHERE full_number = %s" % quotate(full_number)
    executor.execute(sql)
    delete_linker_article_id(article_id)
    check_remaining_author(author_id, author_name)
    os.remove(all_path + str(article_id) + ".pdf")

def remove_author(author_name):
    author_name = util.get_possible_names(author_name)
    author_id = get_author_id.by_name(author_name)
    sql = "DELETE FROM authors WHERE author_id = %s" % author_id
    executor.execute(sql)
    sql = "DELETE FROM linker WHERE author_id = %s" % author_id
    executor.execute(sql)

def delete_linker_article_id(article_id):
    sql = "DELETE FROM linker WHERE article_id = %s" % article_id
    executor.execute(sql)

def check_remaining_author(author_id, author_name):
    if not author_name:
        author_name = get_author.by_author_id(author_id)
    sql = "SELECT * FROM linker WHERE author_id = %s" % author_id
    c = executor.execute(sql).fetchall()
    if len(c) == 0:
        remove_author(author_name)
