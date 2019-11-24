import curses, sys
from utilities import login
from menus import main
import time
def menu(stdscr, main_pos):
    cursor_y = 2
    k = 0

    stdscr.clear()
    stdscr.refresh()
    valid_symbols = "!@#$%^&*()_-+={}[]"

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    user_label = "Username: "
    password_label = "Password: "
    x_pos_user = len(user_label) + 2
    x_pos_pass = len(password_label) + 2
    username = ""
    password_display = ""
    password = ""
    success = ""
    isError = False
    height, width = stdscr.getmaxyx()
    cursor_x = x_pos_user

    while(True):
        stdscr.clear()
        title = "JETS Login"

        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(2,2, user_label)
        stdscr.addstr(3,2, password_label)
        stdscr.attroff(curses.color_pair(1))
        stdscr.addstr(2,x_pos_user, username)
        stdscr.addstr(3, x_pos_pass, password_display)

        if isError:
            stdscr.attron(curses.color_pair(2))
        else:
            stdscr.attron(curses.color_pair(4))
        stdscr.addstr(4, (width - len(success)) // 2, success)
        if isError:
            stdscr.attroff(curses.color_pair(2))
        else:
            stdscr.attroff(curses.color_pair(4))

        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()
        if isError == False and success == "Successfully logged in! Returning to main menu...":
            time.sleep(5)
            main.start(main_pos)
        k = stdscr.getch()

        if k == 27:
            sys.exit()
        elif k == 9:
            if cursor_y == 2:
                cursor_y = 3
                cursor_x = x_pos_pass
            elif cursor_y == 3:
                cursor_y = 2
                cursor_x = x_pos_user
        elif k == 10:
            if cursor_y == 2:
                cursor_y = 3
                cursor_x = x_pos_pass
            elif cursor_y == 3:
                if len(username) == 0:
                    success = "Please enter a username"
                    isError = True
                elif len(password) == 0:
                    success = "Please enter a password"
                    isError = True
                else:
                    isLogged = login.set_login(username, password)
                    if isLogged:
                        success = "Successfully logged in! Returning to main menu..."
                        isError = False
                    else:
                        success = "Incorrect Login"
                        isError = True
        elif k == curses.KEY_UP or k == curses.KEY_DOWN:
            if cursor_y == 3:
                cursor_y = 2
                cursor_x = x_pos_user + len(username)
            elif cursor_y == 2:
                cursor_y = 3
                cursor_x = x_pos_pass + len(password_display)
        elif k == curses.KEY_LEFT:
            if cursor_y == 2 and not cursor_x <= x_pos_user:
                cursor_x -= 1
            elif cursor_y == 3 and not cursor_x == x_pos_pass:
                cursor_x -= 1
        elif k == curses.KEY_RIGHT:
            if cursor_y == 2 and not cursor_x >= x_pos_user + len(username):
                cursor_x += 1
            elif cursor_y == 2 and not cursor_x >= x_pos_pass + len(password_display):
                cursor_x += 1
        elif cursor_y == 2:
            if k == 8:
                if not len(username) == 0:
                    if (not cursor_x == x_pos_user + len(username)) and ( not cursor_x - 1 < x_pos_user):
                        s_pos = cursor_x - x_pos_user
                        username = username[:s_pos-1] + username[s_pos:]
                    else:
                        username = username[:-1]
                    if not cursor_x - 1 < x_pos_user:
                        cursor_x -= 1
            elif str(chr(k)).isalnum() or str(chr(k)) in valid_symbols:
                if not cursor_x == x_pos_user + len(username):
                    s_pos = cursor_x - x_pos_user
                    username = username[:s_pos] + str(chr(k)) + username[s_pos:]
                else:
                    username = username + str(chr(k))
                cursor_x += 1
        elif cursor_y == 3:
            if k == 8:
                if not len(password) == 0:
                    if (not cursor_x == x_pos_pass + len(password)) and (not cursor_x - 1 < x_pos_pass):
                        s_pos = cursor_x - x_pos_pass
                        password = password[:s_pos-1] + password[s_pos:]
                    else:
                        password = password[:-1]
                    password_display = password_display[:-1]
                    if not cursor_x - 1 < x_pos_pass:
                        cursor_x -= 1
            elif str(chr(k)).isalnum() or str(chr(k)) in valid_symbols:
                if not cursor_x == x_pos_pass + len(password):
                    s_pos = cursor_x - x_pos_pass
                    password = password[:s_pos] + str(chr(k)) + password[s_pos:]
                else:
                    password = password + str(chr(k))
                password_display = password_display + "*"
                cursor_x += 1

def start(main_pos):
    curses.wrapper(menu, main_pos)
