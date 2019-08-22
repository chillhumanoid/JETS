import util, os

path = os.path.realpath(__file__)
path = path.replace("login.py","")


def set_login(user, pwd):
    f = open(path + "login.txt", "w+")
    f.write(user + "\n")
    f.write(pwd + "\n")

def get_login():
    f = open(path + "login.txt", "r")
    lines = f.readlines()
    return lines

def get_password():
    lines = get_login()
    pwd = lines[1]
    return pwd

def get_username():
    lines = get_login()
    username = lines[0]
    return username