import sys, curses, os
from menus import by_volume_year
from utilities import get_year as get
from database import get_numbers
from display import articles

def menu(stdscr, vol_number, year):
    cursor_y = 1
    cursor_x = 2
    k = 0
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    x_start_pos = 2
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    paged = False
    current_page = 1
    max_pages = 1

    while(True):
        if k == 27 or k == ord('b'):
            break
        else:
            stdscr.clear()

            title = "Volume {} ({})".format(vol_number, year)

            height, width = stdscr.getmaxyx()

            start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
            status_bar = "  Press 'b' to go to Volume selection menu"

            stdscr.attron(curses.color_pair(1))
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(0, start_x_title, title)
            stdscr.attroff(curses.A_BOLD)
            stdscr.attroff(curses.color_pair(1))

            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(height-1, 0, status_bar)
            stdscr.addstr(height-1, len(status_bar), " " * (width - len(status_bar) - 1))
            stdscr.attroff(curses.color_pair(3))

            issue_number = get_numbers.issues_in_volume(vol_number)
            issue_number = sorted(issue_number)

            rows = len(issue_number)
            max_rows = height - 4
            if k == curses.KEY_UP:
                cursor_y -= 1
                if cursor_y == 0:
                    cursor_y = rows
            elif k == curses.KEY_DOWN:
                cursor_y += 1
                if cursor_y == rows + 2:
                    cursor_y = 1
            string = "All"
            if cursor_y == 1:
                stdscr.attron(curses.color_pair(3))
            stdscr.addstr(1, x_start_pos, string)
            if cursor_y == 1:
                stdscr.attroff(curses.color_pair(3))
            for i in range(0, rows):
                y_position = i + 2
                number = str(issue_number[i])
                string = "Vol {} ({}) - Issue {}".format(vol_number, year, number)
                if cursor_y == y_position:
                    stdscr.attron(curses.color_pair(3))
                stdscr.addstr(y_position, x_start_pos, string)
                if cursor_y == y_position:
                    stdscr.attroff(curses.color_pair(3))
            if k == 10:
                if cursor_y == 1:
                    articles.start(vol_number, year, "All")
                else:
                    selected_issue = cursor_y - 1
                    articles.start(vol_number, year, selected_issue)
        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()

        k = stdscr.getch()

    if k == 27:
        sys.exit()
    if k == ord('b'):
        by_volume_year.start()
def start(volume_number, year):
    curses.wrapper(menu, volume_number, year)
