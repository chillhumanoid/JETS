import curses, sys
from display import displays, login_screen as login
from download import get_url
from utilities import login as log, variables as var
from utilities.menu import title, add_string, menu_option, status_bar, get_height, get_width
def main_menu(stdscr):
    cursor_y = var.main_position
    cursor_x = 1
    k = 0

    curses.curs_set(0)

    stdscr.clear()
    stdscr.refresh()

    isLogged = log.check_login()
    height, width = stdscr.getmaxyx()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    title_str = "Journal of the Evangelical Theological Society Application"
    status_msg = "Written by Jonathan Thorne | © 2019 | Press 'esc' to quit"
    option_1 = "1. View by Volume/Year"
    option_2 = "2. View by Author"
    option_3 = "3. View by Topic (Not Done Yet)"
    option_4 = "4. Check for New Articles"
    option_5 = "5. Login"
    option_5_b = "Logged in to etsjets.org"

    while(True):
        stdscr.clear()

        title(stdscr, title_str)

        status_bar(stdscr, status_msg)

        menu_option(stdscr, option_1, 1, 1, cursor_y)
        menu_option(stdscr, option_2, 2, 1, cursor_y)
        menu_option(stdscr, option_3, 3, 1, cursor_y)
        menu_option(stdscr, option_4, 4, 1, cursor_y)

        if isLogged == False:
            menu_option(stdscr, option_5, 5, 1, cursor_y)
        else:
            menu_option(stdscr, option_5_b, 6, 1, cursor_y)

        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()
        k = stdscr.getch()
        if k == 27 or k == ord('q'):
            sys.exit()
        elif k == curses.KEY_UP:
            cursor_y -= 1
            if cursor_y == 0 and isLogged == False:
                cursor_y = 5
            elif cursor_y == 0 and isLogged == True:
                cursor_y = 4
        elif k == curses.KEY_DOWN:
            cursor_y += 1
            if cursor_y == 6 and isLogged == False:
                cursor_y = 1
            elif cursor_y == 5 and isLogged == True:
                cursor_y = 1
        elif k == 10 or k == curses.KEY_RIGHT:
            char = int.from_bytes(stdscr.instr(cursor_y, 1, 1), byteorder='little')
            if char == ord('1'):
                var.main_position = cursor_y
                var.menu_type = "volume"
                var.volume_current_page = 1
                displays.start()
            elif char == ord('2'):
                var.main_position = cursor_y
                var.menu_type = "authors"
                var.author_current_page = 1
                displays.start()
            elif char == ord('4'):
                get_url.volume()
            elif char == ord('5'):
                login.start(cursor_y)
        elif k == 260:
            start(cursor_y)



def start():
    var.init()
    curses.wrapper(main_menu)
