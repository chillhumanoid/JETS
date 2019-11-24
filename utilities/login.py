import util, os
from bs4 import BeautifulSoup
from requests import *

path = os.path.realpath(__file__)
path = path.replace("utilities\\login.py","")


def set_login(user, pwd):
    with Session() as s:
        login_data = {"name":user, "pass":pwd, "op":"Log in", "form_build_id":"form-a0ed7b5c7437ac9afeb21b126e24633b", "form_id":"user_login_block"}
        response = s.post("https://www.etsjets.org/new_welcome?destination=node%2F1120", login_data)
        soup             = BeautifulSoup(response.content,'html.parser')
        login_check = soup.findAll("div", {"class":"messages error"})
        if(len(login_check) > 0):
            return False
        else:
            f = open(path + "login.txt", "w+")
            f.write(user + "\n")
            f.write(pwd + "\n")
            return True

def get_login():
    f = open(path + "login.txt", "r")
    lines = f.readlines()
    return lines

def check_login():
    lines = get_login()
    if not len(lines) == 0:
        return True
    else:
        return False 

def get_password():
    lines = get_login()
    pwd = lines[1]
    return pwd

def get_username():
    lines = get_login()
    username = lines[0]
    return username
