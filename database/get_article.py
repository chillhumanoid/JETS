from database import executor
from utilities import variables as var
def by_volume(volume_number):
    sql = "SELECT article_id FROM articles WHERE volume_number = {} ORDER BY full_number ASC".format(volume_number)
    c = executor.select(sql)
    article_list = []
    for item in c:
        article_id = item[0]
        sql = "SELECT needs_login FROM articles WHERE article_id = {}".format(article_id)
        d = executor.select(sql)
        for it in d:
            if (it[0] == 1 and var.isLogged) or it[0] == 0:
                article_list.append(article_id)
    return article_list

def by_issue(volume_number, issue_number):
    sql = "SELECT article_id FROM articles WHERE volume_number = {} and issue_number = {} ORDER BY full_number ASC".format(volume_number, issue_number)
    c = executor.select(sql)
    article_list = []
    for item in c:
        article_id = item[0]
        sql = "SELECT needs_login FROM articles WHERE article_id = {}".format(article_id)
        d = executor.select(sql)
        for it in d:
            if (it[0] == 1 and var.isLogged) or it[0] == 0:
                article_list.append(item[0])
    return article_list
