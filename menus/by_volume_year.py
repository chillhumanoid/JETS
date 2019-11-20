import curses, sys, os
from database import get_numbers
from menus import main, by_issue
from math import *
from utilities import get_year as get, arith, string_handler


def menu(stdscr, current_page, main_cursor_y):
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
    max_pages = 1
    while(True):
        if k == 27 or k == ord('m'):
            break
        elif k == ord('q'):
            sys.exit()
        else:
            stdscr.clear()
            title = "JETS by Volume(Year)"

            height, width = stdscr.getmaxyx()


            start_x_title = arith.title_start(title, width)

            stdscr.attron(curses.color_pair(1))
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(0, start_x_title, title)
            stdscr.attroff(curses.A_BOLD)
            stdscr.attroff(curses.color_pair(1))

            volume_numbers = get_numbers.volumes()
            volume_numbers = sorted(volume_numbers)
            rows = len(volume_numbers)
            max_rows = height - 4
            num_pages = ceil(rows / max_rows)
            last_row = arith.get_last_row(rows, max_rows, num_pages)

            if k == curses.KEY_UP:
                cursor_y -= 1
                if cursor_y == 0:
                    if current_page == num_pages:
                        cursor_y = last_row
                    else:
                        cursor_y = max_rows - 1
            elif k == curses.KEY_DOWN:
                cursor_y += 1
                if current_page == num_pages:
                    if cursor_y == last_row + 1:
                        cursor_y = 1
                else:
                    if cursor_y == max_rows:
                        cursor_y = 1
            if rows > max_rows:

                if (k == ord('n') or k == curses.KEY_RIGHT) and not current_page == num_pages:
                    cursor_y = 1
                    current_page += 1
                elif (k == ord('p') or k == curses.KEY_LEFT) and not current_page == 1:
                    cursor_y = 1
                    current_page -= 1
                elif (k == curses.KEY_LEFT or k == ord('p')) and current_page == 1:
                    main.start(main_cursor_y)
                l_row = "Page {} of {}".format(current_page, num_pages)

                if(current_page == 1):
                    status_bar = " 'n' : Next Page | 'm'/esc : Main Menu "
                    for i in range(0, max_rows - 1):
                        y_position = i + 1
                        number = str(volume_numbers[i])
                        display_number = string_handler.display_number(number)
                        display = string_handler.display_volume(display_number, number)
                        if cursor_y == y_position:
                            stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(y_position, x_start_pos, display)
                        if cursor_y == y_position:
                            stdscr.attroff(curses.color_pair(3))

                elif(current_page == num_pages):
                    status_bar = " 'p' : Previous Page | 'm'/esc : Main Menu "
                    for i in range(0, max_rows - 1):
                        y_position = i + 1
                        if not (i + (max_rows * (current_page - 1)) - 1) > rows:
                            index = arith.get_index(max_rows, num_pages, current_page, y_position, False)
                            number = str(volume_numbers[index])
                            display_number = string_handler.display_number(number)
                            display = string_handler.display_volume(display_number, number)
                            if cursor_y == y_position:
                                stdscr.attron(curses.color_pair(3))
                            stdscr.addstr(y_position, x_start_pos, display)
                            if cursor_y == y_position:
                                stdscr.attroff(curses.color_pair(3))

                else:
                    status_bar = " 'n' : Next Page | 'p' : Previous Page | 'm'/esc : Main Menu "
                    for i in range(0, max_rows - 1):
                        y_position = i + 1
                        index = arith.get_index(max_rows, num_pages, current_page, y_position, False)
                        number = str(volume_numbers[index])
                        display_number = string_handler.display_number(number)
                        display = string_handler.display_volume(display_number, number)
                        if cursor_y == y_position:
                            stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(y_position, x_start_pos, display)
                        if cursor_y == y_position:
                            stdscr.attroff(curses.color_pair(3))

                if k == 10:
                    i = arith.get_index(max_rows, num_pages, current_page, cursor_y - 1, True)
                    number = str(volume_numbers[i])
                    year = get.year(number)
                    if(len(number) == 1):
                        number = "0" + number
                    by_issue.start(number, year, current_page, main_cursor_y)



            stdscr.addstr(height-3, x_start_pos, l_row)
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(height-1, 0, status_bar)
            stdscr.addstr(height-1, len(status_bar), " " * (width - len(status_bar) - 1))
            stdscr.attroff(curses.color_pair(3))



            stdscr.move(cursor_y, cursor_x)
            stdscr.refresh()

            k = stdscr.getch()
    if k == 27:
        main.start(main_cursor_y)

def start(current_page, main_cursor_y):
    curses.wrapper(menu, current_page, main_cursor_y)
