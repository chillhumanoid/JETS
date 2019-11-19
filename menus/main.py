import curses, sys
from menus import by_volume_year

def main_menu(stdscr):
    cursor_x = 2
    cursor_y = 1
    k = 0

    curses.curs_set(0)

    stdscr.clear()
    stdscr.refresh()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while(True):
        if k == 27 or k == curses.KEY_LEFT:
            break #27 is the esc key
        elif k == curses.KEY_UP:
            cursor_y -= 1
            if cursor_y == 0:
                cursor_y = 5 #hardcoded because i know how many menu items (+1)
        elif k == curses.KEY_DOWN:
            cursor_y += 1
            if cursor_y == 6: #above value + 1
                cursor_y = 1
        elif k == 10 or curses.KEY_RIGHT:
            char = int.from_bytes(stdscr.instr(cursor_y, 1, 1),  byteorder='little')
            if char == ord('1'):
                by_volume_year.start()
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        title = "Journal of the Evangelical Theological Society Application"
        status_bar = "Written by Jonathan Thorne | © 2019 | Press 'esc' to quit"



        option_1 = "1. View by Volume/Year"
        option_2 = "2. View by Author"
        option_3 = "3. View by Topic (Not Done Yet)"
        option_4 = "4. Check for New Articles"
        option_5 = "5. Login"

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
        if cursor_y == 5:
            stdscr.attron(curses.color_pair(3))
        stdscr.addstr(5, 1, option_5)
        if cursor_y == 5:
            stdscr.attroff(curses.color_pair(3))

        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()
        k = stdscr.getch()
    sys.exit()



def start():
    curses.wrapper(main_menu)
