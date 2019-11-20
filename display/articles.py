from menus import by_issue
import sys, curses, os
from utilities import get_year as get, names, open
from database import get_numbers, get_article, get_title, get_author
from math import *
from display import article

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
        if k == 27:
            break
        else:
            stdscr.clear()

            if issue_number != "All":
                title = "Volume {} ({}) - Issue {}".format(volume_number, year, issue_number)
            else:
                title = "Volume {} ({}) - All Issues".format(volume_number, year)

            height, width = stdscr.getmaxyx()

            start_x_title = int((width // 2) - (len(title) //2) - len(title) % 2)

            status_bar = "Press 'esc' to go issue selection"

            stdscr.attron(curses.color_pair(1))
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(0, start_x_title, title)
            stdscr.attroff(curses.A_BOLD)
            stdscr.attroff(curses.color_pair(1))
            if issue_number != "All":
                article_ids = get_article.by_issue(volume_number, issue_number)
            else:
                article_ids = get_article.by_volume(volume_number)

            rows = len(article_ids)
            max_rows = height - 4
            if rows > max_rows:
                num_pages = ceil(rows/max_rows)
                last_row = rows - (max_rows * (num_pages - 1)) + 2
            else:
                num_pages = 1
                last_row = rows - 1
            


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
                num_pages = ceil(rows/max_rows)
                max_pages = num_pages

                if (k == ord('n') or k == curses.KEY_RIGHT) and not current_page == max_pages:
                    cursor_y = 1
                    current_page += 1
                elif (k == ord('p') or k == curses.KEY_LEFT) and not current_page == 1:
                    cursor_y = 1
                    current_page -= 1
                elif k == curses.KEY_LEFT and current_page == 1:
                    by_issue.start(volume_number, year)

                l_row = "Page {} of {}".format(current_page, num_pages)

                if current_page == 1:
                    status_bar = " Press 'n' to go to the next page | Press 'esc' to go to issue_selection"
                    for i in range(0, max_rows - 1):
                        y_position = i + 1
                        article_id = article_ids[i]
                        number = get_numbers.full(article_id)
                        number = number.split(".")[1] + "." + number.split(".")[2]
                        title = get_title.by_article_id(article_id)
                        author = get_author.by_article_id(article_id)
                        display_author = names.get_authors(author)
                        if len(title) > 75:
                            title = title[:72] + " . . ."
                        else:
                            magic_number = 78 - len(title)
                            magic_string = " " * magic_number
                            title = title + magic_string
                        if len(display_author) > 26:
                            display_author = display_author[:23] + " . . ."
                        display_string = "{}| {} | {}".format(number, title, display_author)
                        if cursor_y == y_position:
                            stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(y_position, x_start_pos, display_string)
                        if cursor_y == y_position:
                            stdscr.attroff(curses.color_pair(3))
                elif current_page == max_pages:
                    status_bar = " Press 'p' to go to the previous page | Press 'esc' to go to issue selection"
                    for i in range(0, max_rows + 1):
                        y_position = i + 1
                        check = i + (max_rows * (current_page-1)) - 1
                        if not check > rows:
                            article_id = article_ids[i + (max_rows * (current_page-1)) - 2]
                            number = get_numbers.full(article_id)
                            number = number.split(".")[1] + "." + number.split(".")[2]
                            title = get_title.by_article_id(article_id)
                            author = get_author.by_article_id(article_id)
                            display_author = names.get_authors(author)
                            if len(title) > 75:
                                title = title[:72] + " . . ."
                            else:
                                magic_number = 78 - len(title)
                                magic_string = " " * magic_number
                                title = title + magic_string
                            if len(author) > 25:
                                author = author[:22] + " . . ."
                            display_string = "{}| {} | {}".format(number, title, display_author)
                            if cursor_y == y_position:
                                stdscr.attron(curses.color_pair(3))
                            stdscr.addstr(y_position, x_start_pos, display_string)
                            if cursor_y == y_position:
                                stdscr.attroff(curses.color_pair(3))
                else:
                    status_bar = " Press 'n' to go to the next page | Press 'p' to go to the previous page | Press 'esc' to go to issue_selection"
                    for i in range(0, max_rows -1):
                        y_position = i + 1
                        check = i + (max_rows * (current_page-1)) - 1
                        if not check > rows:
                            article_id = article_ids[i + (max_rows * (current_page-1)) - 2]
                            number = get_numbers.full(article_id)
                            number = number.split(".")[1] + "." + number.split(".")[2]
                            title = get_title.by_article_id(article_id)
                            author = get_author.by_article_id(article_id)
                            display_author = names.get_authors(author)
                            if len(title) > 75:
                                title = title[:72] + " . . ."
                            else:
                                magic_number = 78 - len(title)
                                magic_string = " " * magic_number
                                title = title + magic_string
                            if len(author) > 25:
                                author = author[:22] + " . . ."
                            display_string = "{}| {} | {}".format(number, title, display_author)
                            if cursor_y == y_position:
                                stdscr.attron(curses.color_pair(3))
                            stdscr.addstr(y_position, x_start_pos, display_string)
                            if cursor_y == y_position:
                                stdscr.attroff(curses.color_pair(3))
                i = cursor_y - 1
                if current_page == max_pages:
                    article_id = article_ids[i + (max_rows * (current_page -1)) - 2]
                elif(current_page == 1):
                    article_id = article_ids[i]
                else:
                    article_id = article_ids[i + (max_rows * (current_page -1)) - 1]
                if k == ord('o') or k == 10:
                    full_number = get_numbers.full(article_id)
                    open.open_file(full_number)
                elif k == ord('i'):
                    article.start(article_id, volume_number, year, issue_number)
            else:
                l_row = "Page {} of {}".format(current_page, num_pages)
                if k == curses.KEY_LEFT:
                    by_issue.start(volume_number, year)
                for i in range(0, rows - 1):
                    y_position = i + 1
                    article_id = article_ids[i]
                    number = get_numbers.full(article_id)
                    number = number.split(".")[1] + "." + number.split(".")[2]
                    title = get_title.by_article_id(article_id)
                    author = get_author.by_article_id(article_id)
                    display_author = names.get_authors(author)
                    if len(title) > 75:
                        title = title[:72] + " . . ."
                    else:
                        magic_number = 78 - len(title)
                        magic_string = " " * magic_number
                        title = title + magic_string
                    display_string = "{}| {} | {}".format(number, title, display_author)
                    if cursor_y == y_position:
                        stdscr.attron(curses.color_pair(3))
                    stdscr.addstr(y_position, x_start_pos, display_string)
                    if cursor_y == y_position:
                        stdscr.attroff(curses.color_pair(3))
                i = cursor_y - 1
                print(cursor_y)
                print(i)
                article_id = article_ids[i]
                if k == 10:
                    article.start(article_id, volume_number, year, issue_number)
                elif k == ord('o'):
                    full_number = get_numbers.full(article_id)
                    open.open_file(full_number)

        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, status_bar)
        stdscr.addstr(height-1, len(status_bar), " " * (width - len(status_bar) - 1))
        stdscr.attroff(curses.color_pair(3))
        stdscr.addstr(height - 3, x_start_pos, l_row)

        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()
        k = stdscr.getch()
    if k == 27:
        by_issue.start(volume_number, year)



def start(volume_number, year, issue_number):
    curses.wrapper(menu, volume_number, year, issue_number)
