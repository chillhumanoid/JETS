import curses, sys
from display import displays, login_screen as login
from download import get_url
from utilities import login as log

def main_menu(stdscr, cursor_y):
    cursor_x = 1
    k = 0

    curses.curs_set(0)

    stdscr.clear()
    stdscr.refresh()
    isLogged = log.check_login()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while(True):
        if k == 27:
            break #27 is the esc key
        elif k == curses.KEY_UP:
            cursor_y -= 1
            if cursor_y == 0 and isLogged == False:
                cursor_y = 5 #hardcoded because i know how many menu items (+1)
            elif cursor_y == 0 and isLogged == True:
                cursor_y = 4
        elif k == curses.KEY_DOWN:
            cursor_y += 1
            if cursor_y == 6 and isLogged == False: #above value + 1
                cursor_y = 1
            elif cursor_y == 5 and isLogged == True:
                cursor_y = 1
        elif k == 10 or curses.KEY_RIGHT:
            char = int.from_bytes(stdscr.instr(cursor_y, 1, 1),  byteorder='little')
            if char == ord('1'):
                displays.start("volume", cursor_y, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, "")
            elif char == ord('2'):
                displays.start("authors", cursor_y, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, "")
            elif char == ord('4'):
                get_url.volume()
            elif char == ord('5') and isLogged == False:
                login.start(cursor_y)


        stdscr.clear()
        height, width = stdscr.getmaxyx()

        title = "Journal of the Evangelical Theological Society Application"
        status_bar = "Written by Jonathan Thorne | © 2019 | Press 'esc' to quit"



        option_1 = "1. View by Volume/Year"
        option_2 = "2. View by Author"
        option_3 = "3. View by Topic (Not Done Yet)"
        option_4 = "4. Check for New Articles"
        option_5 = "5. Login"
        option_5_b = "Logged in to etsjets.org"

        start_x_title = int((width // 2 ) - (len(title) // 2) - len(title) % 2)

        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, status_bar)
        stdscr.addstr(height-1, len(status_bar), " " * (width - len(status_bar) - 1))
        stdscr.attroff(curses.color_pair(3))

        stdscr.attron(curses.color_pair(1))
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(0, start_x_title, title)
        stdscr.attroff(curses.color_pair(1))
        stdscr.attroff(curses.A_BOLD)
        if cursor_y == 1:
            stdscr.attron(curses.color_pair(3))
        stdscr.addstr(1, 1, option_1)
        if cursor_y == 1:
            stdscr.attroff(curses.color_pair(3))
        if cursor_y == 2:
            stdscr.attron(curses.color_pair(3))
        stdscr.addstr(2, 1, option_2)
        if cursor_y == 2:
            stdscr.attroff(curses.color_pair(3))
        if cursor_y == 3:
            stdscr.attron(curses.color_pair(3))
        stdscr.addstr(3, 1, option_3)
        if cursor_y == 3:
            stdscr.attroff(curses.color_pair(3))
        if cursor_y == 4:
            stdscr.attron(curses.color_pair(3))
        stdscr.addstr(4, 1, option_4)
        if cursor_y == 4:
            stdscr.attroff(curses.color_pair(3))
        if isLogged == False:
            if cursor_y == 5:
                stdscr.attron(curses.color_pair(3))
            stdscr.addstr(5, 1, option_5)
            if cursor_y == 5:
                stdscr.attroff(curses.color_pair(3))
        else:
            stdscr.addstr(6, 1, option_5_b)

        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()
        k = stdscr.getch()
    sys.exit()



def start(main_pos):
    curses.wrapper(main_menu, main_pos)
