from database import executor
from utilities import variables as var
def full(article_id):
    """
    Gets the full number based on article id

    Current locations: display.display_articles()

    Parameters:
    article_id (int)

    Returns:
    full_number (string)
    """
    sql = "SELECT full_number FROM articles WHERE article_id = {}".format(article_id)
    c = executor.select(sql)
    return c[0][0]

def volumes():
    if var.isLogged:
        sql = "SELECT volume_number FROM articles"
    else:
        sql = "SELECT volume_number FROM articles WHERE needs_login = 0"
    c = executor.select(sql)
    volume_list = []
    for item in c:
        if not item[0] in volume_list:
            volume_list.append(item[0])
    return volume_list

def issues_in_volume(volume_number):
    if var.isLogged:
        sql = "SELECT issue_number FROM articles WHERE Volume_number = {}".format(volume_number)
    else:
        sql = "SELECT issue_number FROM articles WHERE volume_number = {} AND needs_login = 0".format(volume_number)
    c = executor.select(sql)
    issue_list = []
    for item in c:
        if not item[0] in issue_list:
            issue_list.append(item[0])
    return issue_list

def year (volume_number):
    sql = "SELECT year FROM volume WHERE volume_number = {}".format(volume_number)
    c = executor.select(sql)
    for item in c:
        return item[0]
