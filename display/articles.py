from menus import by_issue
import sys, curses, os
from utilities import get_year as get
from database import get_numbers, get_article, get_title
from math import *

def menu(stdscr, volume_number, year, issue_number):
    x_start_pos = 2
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
        if k == 27 or k == ord('b'):
            break
        else:
            stdscr.clear()

            if issue_number != "All":
                title = "Volume {} ({}) - Issue {}".format(volume_number, year, issue_number)
            else:
                title = "Volume {} ({}) - All Issues".format(volume_number, year)

            height, width = stdscr.getmaxyx()

            start_x_title = int((width // 2) - (len(title) //2) - len(title) % 2)

            status_bar = "Press 'b' to go issue selection"

            stdscr.attron(curses.color_pair(1))
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(0, start_x_title, title)
            stdscr.attroff(curses.A_BOLD)
            stdscr.attroff(curses.color_pair(1))

            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(height-1, 0, status_bar)
            stdscr.addstr(height-1, len(status_bar), " " * (width - len(status_bar) - 1))
            stdscr.attroff(curses.color_pair(3))

            articles = []
            if issue_number != "All":
                article_ids = get_article.by_issue(volume_number, issue_number)
            else:
                article_ids = get_article.by_volume(volume_number)
            for id in article_ids:
                title = get_title.by_article_id(id)
                articles.append(title)
            rows = len(articles)
            max_rows = height - 4
            if rows > max_rows:
                num_pages = ceil(rows/max_rows)
                max_pages = num_pages

                if k == ord('n') and not current_page == max_pages:
                    cursor_y = 1
                    current_page += 1
                elif k == ord('p') and not current_page == 1:
                    cursor_y = 1
                    current_page -= 1

                l_row = "Page {} of {}".format(current_page, num_pages)

                if current_page == 1:
                    status_bar = " Press 'n' to go to the next page | Press 'b' to go to issue_selection"
                    for i in range(0, max_rows - 1):
                        y_position = i + 1
                        article = str(articles[i])
                        display_string = "{}) {}".format(y_position, article)
                        stdscr.addstr(y_position, x_start_pos, display_string)
                elif current_page == max_pages:
                    status_bar = " Press 'p' to go to the previous page | Press 'b' to go to issue selection"
                    for i in range(0, max_rows + 1):
                        y_position = i + 1
                        if not(i + (max_rows * (current_page - 1)) - 1) > rows:
                            article = articles[i + (max_rows * (current_page - 1)) - 2]
                            display_string = "{}) {}".format(y_position, article)
                            stdscr.addstr(y_position, x_start_pos, display_string)
                else:
                    status_bar = " Press 'n' to go to the next page | Press 'p' to go to the previous page | Press 'b' to go to issue_selection"
                    for i in range(0, max_rows -1):
                        y_position = i + 1
                        article = articles[i + (max_rows * (current_page - 1)) - 1]
                        display_string = "{}) {}".format(y_position, article)
                        stdscr.addstr(y_position, x_start_pos, display_string)


        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()
        k = stdscr.getch()
    if k == 27:
        sys.exit()
    if k == ord('b'):
        by_issue.start(volume_number, year)


def start(volume_number, year, issue_number):
    curses.wrapper(menu, volume_number, year, issue_number)