from bs4 import BeautifulSoup
from pathlib import Path
from requests import Session

path = Path("login.txt")

def set_login(user, pwd):
    with Session() as s:
        login_data = {"name":user, "pass":pwd, "op":"Log in", "form_build_id":"form-a0ed7b5c7437ac9afeb21b126e24633b", "form_id":"user_login_block"}
        response = s.post("https://www.etsjets.org/new_welcome?destination=node%2F1120", login_data)
        soup             = BeautifulSoup(response.content,'html.parser')
        login_check = soup.findAll("div", {"class":"messages error"})
        if(len(login_check) > 0):
            return False
        else:
            f = open(path, "w")
            f.write(user + "\n")
            f.write(pwd + "\n")
            f = open(path, "")
            return True

def get_login():
    if path.exists():
        f = open(path, "r")
        lines = f.readlines()
        return lines
    else:
        return []

def check_login():
    lines = get_login()
    if not len(lines) == 0:
        return True
    else:
        return False
