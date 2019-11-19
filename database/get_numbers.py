from database import executor

def full(article_id):
    """
    Gets the full number based on article id

    Current locations: display.display_articles()

    Parameters:
    article_id (int)

    Returns:
    full_number (string)
    """
    sql = "SELECT full_number FROM titles WHERE article_id = %s" % article_id
    c = executor.execute(sql).fetchall()
    return c[0][0]

def volumes():
    sql = "SELECT volume_number FROM titles"
    c = executor.execute(sql).fetchall()
    volume_list = []
    for item in c:
        if not item[0] in volume_list:
            volume_list.append(item[0])
    return volume_list

def issues_in_volume(volume_number):
    sql = "SELECT issue_number FROM titles WHERE volume_number = %s" % volume_number
    c = executor.execute(sql).fetchall()
    issue_list = []
    for item in c:
        if not item[0] in issue_list:
            issue_list.append(item[0])
    return issue_list
