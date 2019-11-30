import curses, sys
from display import displays, login_screen as login, download_location as dl
from utilities import variables as var, menu as m
def main_menu(stdscr):
    cursor_y = var.main_position
    cursor_x = 1
    k = 0

    curses.curs_set(0)

    stdscr.clear()
    stdscr.refresh()

    height, width = stdscr.getmaxyx()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    title_str = "Journal of the Evangelical Theological Society Application"
    status_msg = "Written by Jonathan Thorne | © 2019 | Press 'esc' to quit"
    option_1 = "1. View by Volume/Year"
    option_2 = "2. View by Author"
    option_3 = "3. View by Topic (NOT DONE)"
    option_4 = "4. Search (NOT DONE)"
    option_5 = "5. Downloads (WIP)"
    option_6 = "6. Login"
    option_6_b = "Logged in to etsjets.org"

    while(True):
        stdscr.clear()

        m.title(stdscr, title_str)

        m.status_bar(stdscr, status_msg)

        m.menu_option(stdscr, option_1, 1, 1, cursor_y)
        m.menu_option(stdscr, option_2, 2, 1, cursor_y)
        m.menu_option(stdscr, option_3, 3, 1, cursor_y)
        m.menu_option(stdscr, option_4, 4, 1, cursor_y)
        m.menu_option(stdscr, option_5, 5, 1, cursor_y)

        if var.isLogged == False:
            m.menu_option(stdscr, option_6, 6, 1, cursor_y)
        else:
            m.menu_option(stdscr, option_6_b, 7, 1, cursor_y)

        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()
        k = stdscr.getch()
        if k == 27 or k == ord('q'):
            sys.exit()
        elif k == curses.KEY_UP:
            cursor_y -= 1
            if cursor_y == 4: #COMMENT THIS OUT LATER
                cursor_y = 2 #DITTO
            elif cursor_y == 0 and var.isLogged == False:
                cursor_y = 6
            elif cursor_y == 0 and var.isLogged == True:
                cursor_y = 5 # CHANGE THIS
            var.main_position = cursor_y
        elif k == curses.KEY_DOWN:
            cursor_y += 1
            if cursor_y > 6 and var.isLogged == False:
                cursor_y = 1
            elif cursor_y > 3 and var.isLogged == True: #CHANGE THIS
                cursor_y = 5
            elif cursor_y == 3 and var.isLogged == False: # COMMENT THIS OUT
                cursor_y = 5 #COMMENT THIS OUT
            var.main_position = cursor_y
        elif k == 10 or k == curses.KEY_RIGHT:
            char = int.from_bytes(stdscr.instr(cursor_y, 1, 1), byteorder='little')
            if char == ord('1'):
                var.menu_type = "volume"
                var.volume_current_page = 1
                displays.start()
            elif char == ord('2'):
                var.menu_type = "authors"
                var.author_current_page = 1
                displays.start()
            elif char == ord('5'):
                dl.start()
            elif char == ord('6'):
                login.start(cursor_y)
        elif k == 260:
            start()



def start():
    curses.wrapper(main_menu)
