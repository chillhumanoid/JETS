from menus import by_issue, main, by_volume_year
import sys, curses, os
from utilities import get_year as get, names, open, arith, string_handler
from database import get_numbers, get_article, get_title, get_author
from math import *
from display import article


def menu(stdscr, volume_number, year, issue_number, volume_current_page, main_cursor_y):
    x_start_pos = 1
    cursor_y = 1
    cursor_x = 2
    k = 0

    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    paged = False
    current_page = 1
    max_pages = 1

    while(True):
        if k == 27:
            break
        elif k == ord('q'):
            sys.exit()
        else:
            stdscr.clear()

            if issue_number != "All":
                title = "Volume {} ({}) - Issue {}".format(volume_number, year, issue_number)
                article_ids = get_article.by_issue(volume_number, issue_number)
            else:
                title = "Volume {} ({}) - All Issues".format(volume_number, year)
                article_ids = get_article.by_volume(volume_number)

            height, width = stdscr.getmaxyx()

            start_x_title = arith.title_start(title, width)

            status_bar = " 'o' : Open | 'i' : Info | esc : Issue Selection | 'v' : Volume Selection | 'm' : Main Menu "

            stdscr.attron(curses.color_pair(1))
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(0, start_x_title, title)
            stdscr.attroff(curses.A_BOLD)
            stdscr.attroff(curses.color_pair(1))

            rows = len(article_ids)
            print("ROWS {}".format(rows))
            max_rows = height - 4
            num_pages = arith.get_page_num(rows, max_rows)
            last_row = arith.get_last_row(rows, max_rows, num_pages)
            print("LAST ROW {}".format(last_row))

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

            articles = []


            if rows > max_rows:

                if (k == ord('n') or k == curses.KEY_RIGHT) and not current_page == num_pages:
                    cursor_y = 1
                    current_page += 1
                elif (k == ord('p') or k == curses.KEY_LEFT) and not current_page == 1:
                    cursor_y = 1
                    current_page -= 1
                elif k == curses.KEY_LEFT and current_page == 1:
                    by_issue.start(volume_number, year, volume_current_page, main_cursor_y)

                l_row = "Page {} of {}".format(current_page, num_pages)

                if current_page == 1:
                    status_bar = " 'n' : Next Page | 'o' : Open | 'i' : Info | esc : Issue Selection | 'v' : Volume Selection | 'm' : Main Menu "
                    for i in range(0, max_rows - 1):
                        y_position = i + 1
                        article_id = article_ids[i]
                        display_string = string_handler.display_string(article_id, width)
                        if cursor_y == y_position:
                            stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(y_position, x_start_pos, display_string)
                        if cursor_y == y_position:
                            stdscr.attroff(curses.color_pair(3))
                elif current_page == num_pages:
                    status_bar = " 'p' : Previous Page | 'o' : Open | 'i' : Info | esc : Issue Selection | 'v': Volume Selection | 'm' : Main Menu "
                    for i in range(0, max_rows + 1):
                        y_position = i + 1
                        check = i + (max_rows * (current_page-1)) - 1
                        if not check > rows:
                            index = arith.get_index(max_rows, num_pages, current_page, y_position, False)
                            article_id = article_ids[index]
                            display_string = string_handler.display_string(article_id, width)
                            if cursor_y == y_position:
                                stdscr.attron(curses.color_pair(3))
                            stdscr.addstr(y_position, x_start_pos, display_string)
                            if cursor_y == y_position:
                                stdscr.attroff(curses.color_pair(3))
                else:
                    status_bar = " 'n' : Next Page | 'p' : Previous Page | 'o' :  Open | 'i' : Info | esc : Issue Selection | 'v' : Volume Selection | 'm' : Main Menu "
                    for i in range(0, max_rows -1):
                        y_position = i + 1
                        check = i + (max_rows * (current_page-1)) - 1
                        if not check > rows:
                            index = arith.get_index(max_rows, num_pages, current_page, y_position, False)
                            article_id = article_ids[index]
                            display_string = string_handler.display_string(article_id, width)
                            if cursor_y == y_position:
                                stdscr.attron(curses.color_pair(3))
                            stdscr.addstr(y_position, x_start_pos, display_string)
                            if cursor_y == y_position:
                                stdscr.attroff(curses.color_pair(3))
            else:
                l_row = "Page {} of {}".format(current_page, num_pages)
                if k == curses.KEY_LEFT:
                    by_issue.start(volume_number, year)
                for i in range(0, rows - 1):
                    y_position = i + 1
                    article_id = article_ids[i]
                    display_string = string_handler.display_string(article_id, width)
                    if cursor_y == y_position:
                        stdscr.attron(curses.color_pair(3))
                    stdscr.addstr(y_position, x_start_pos, display_string)
                    if cursor_y == y_position:
                        stdscr.attroff(curses.color_pair(3))
            i = arith.get_index(max_rows, num_pages, current_page, cursor_y, False)
            article_id = article_ids[i]
            if k == ord('o') or k == 10:
                full_number = get_numbers.full(article_id)
                open.open_file(full_number)
            elif k == ord('i'):
                article.start(article_id, volume_number, year, issue_number, volume_current_page, main_cursor_y)
            elif k == ord('m'):
                main.start(main_cursor_y)
            elif k == ord('v'):
                by_volume_year.start(volume_current_page, main_cursor_y)
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, status_bar)
        stdscr.addstr(height-1, len(status_bar), " " * (width - len(status_bar) - 1))
        stdscr.attroff(curses.color_pair(3))
        stdscr.addstr(height - 3, x_start_pos, l_row)

        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()
        k = stdscr.getch()
    if k == 27:
        by_issue.start(volume_number, year, volume_current_page, main_cursor_y)



def start(volume_number, year, issue_number, volume_current_page, main_cursor_y):
    curses.wrapper(menu, volume_number, year, issue_number, volume_current_page, main_cursor_y)
