from database import executor

def by_volume(volume_number):
    sql = "SELECT article_id FROM titles WHERE volume_number = %s ORDER BY full_number ASC" % volume_number
    c = executor.execute(sql).fetchall()
    article_list = []
    for item in c:
        article_list.append(item[0])
    return article_list

def by_issue(volume_number, issue_number):
    sql = "SELECT article_id FROM titles WHERE volume_number = %s and issue_number = %s ORDER BY full_number ASC" % (volume_number, issue_number)
    c = executor.execute(sql).fetchall()
    article_list = []
    for item in c:
        article_list.append(item[0])
    return article_list
