import curses, sys, os
from database import get_numbers
from menus import main, by_issue
from math import *
from utilities import get_year as get


def menu(stdscr):
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
            title = "JETS by Volume(Year)"

            height, width = stdscr.getmaxyx()



            start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)

            stdscr.attron(curses.color_pair(1))
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(0, start_x_title, title)
            stdscr.attroff(curses.A_BOLD)
            stdscr.attroff(curses.color_pair(1))

            volume_numbers = get_numbers.volumes()
            volume_numbers = sorted(volume_numbers)
            rows = len(volume_numbers)
            max_rows = height - 4
            last_row = rows - (max_rows * (max_pages - 1)) + 2

            if k == curses.KEY_UP:
                cursor_y -= 1
                if cursor_y == 0:
                    if current_page == max_pages:
                        cursor_y = last_row
                    else:
                        cursor_y = max_rows - 1
            elif k == curses.KEY_DOWN:
                cursor_y += 1
                if current_page == max_pages:
                    if cursor_y == last_row + 1:
                        cursor_y = 1
                else:
                    if cursor_y == max_rows:
                        cursor_y = 1
            if rows > max_rows:

                num_pages = ceil(rows / max_rows)
                max_pages = num_pages

                if (k == ord('n') or k == curses.KEY_RIGHT) and not current_page == max_pages:
                    cursor_y = 1
                    current_page += 1
                elif (k == ord('p') or k == curses.KEY_LEFT) and not current_page == 1:
                    cursor_y = 1
                    current_page -= 1
                elif k == curses.KEY_LEFT and current_page == 1:
                    main.start()
                l_row = "Page {} of {}".format(current_page, num_pages)

                if(current_page == 1):
                    status_bar = " Press 'n' to go to the next page | Press 'esc' to go to the main menu"
                    for i in range(0, max_rows - 1):
                        y_position = i + 1
                        number = str(volume_numbers[i])
                        if len(number) == 1:
                            display_number = "0" + number
                        else:
                            display_number = number
                        if cursor_y == y_position:
                            stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(y_position, x_start_pos, "Vol " + display_number + " (" + get.year(number) + ")")
                        if cursor_y == y_position:
                            stdscr.attroff(curses.color_pair(3))

                elif(current_page == max_pages):
                    status_bar = " Press 'p' to go to the previous page | Press 'esc' to go to the main menu"
                    for i in range(0, max_rows + 1):
                        y_position = i + 1
                        if not (i + (max_rows * (current_page - 1)) - 1) > rows:
                            number = str(volume_numbers[i + (max_rows * (current_page - 1)) - 2])
                            if cursor_y == y_position:
                                stdscr.attron(curses.color_pair(3))
                            stdscr.addstr(y_position, x_start_pos, "Vol " + number + " (" + get.year(number) + ")")
                            if cursor_y == y_position:
                                stdscr.attroff(curses.color_pair(3))


                else:
                    status_bar = " Press 'n' to go to the next page | Press 'p' to go the previous page | Press 'esc' to go to the main menu"
                    for i in range(0, max_rows - 1):
                        y_position = i + 1
                        number = str(volume_numbers[i + (max_rows * (current_page - 1)) - 1])
                        if cursor_y == y_position:
                            stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(y_position, x_start_pos, "Vol " + number + " (" + get.year(number) + ")")
                        if cursor_y == y_position:
                            stdscr.attroff(curses.color_pair(3))
                if k == 10:
                    i = cursor_y - 1
                    if(current_page == max_pages):
                        number = str(volume_numbers[i + (max_rows * (current_page -1)) -2])
                        year = get.year(number)
                        if len(number) == 1:
                            number = "0" + number
                        by_issue.start(number, year)
                    elif(current_page == 1):
                        number = str(volume_numbers[i])
                        year = get.year(number)
                        if len(number) == 1:
                            number = "0" + number
                        by_issue.start(number, year)
                    else:
                        number = str(volume_numbers[i + (max_rows * (current_page - 1)) -1])
                        year = get.year(number)
                        if len(str(number)) == 1:
                            number = "0" + str(number)
                        by_issue.start(number, year)



            stdscr.addstr(height-3, x_start_pos, l_row)
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(height-1, 0, status_bar)
            stdscr.addstr(height-1, len(status_bar), " " * (width - len(status_bar) - 1))
            stdscr.attroff(curses.color_pair(3))



            stdscr.move(cursor_y, cursor_x)
            stdscr.refresh()

            k = stdscr.getch()
    if k == 27:
        main.start()

def start():
    curses.wrapper(menu)
