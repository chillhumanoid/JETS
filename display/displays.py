import curses, sys
from utilities import arith, string_handler, get_list, calculate_y, variables as var, menu as m, menu_helpers as mh
from math import ceil
from database import get_url, get_numbers
from display import article, main

"""
testing capability to reuse menu logic
"""
def menu(stdscr):
    x_start_pos = 1
    cursor_y    = 1
    cursor_x    = 1
    k           = 0
    sort_int    = 1

    if var.menu_type == "authors":
        if not var.authors_y_pos == 0:
            cursor_y = var.authors_y_pos
        current_page = var.author_current_page

    elif var.menu_type == "volume":
        if not var.volume_y_pos == 0:
            cursor_y = var.volume_y_pos
        current_page = var.volume_current_page

    elif var.menu_type == "issue":
        if not var.issue_y_pos == 0:
            cursor_y = var.issue_y_pos
        current_page = 1

    elif var.menu_type == "articles":
        if not var.articles_y_pos == 0:
            cursor_y = var.articles_y_pos
        current_page = 1

    elif var.menu_type == "author_articles":
        if not var.author_articles_y_pos == 0:
            cursor_y = var.author_articles_y_pos
        current_page = 1

    else:
        current_page = 1

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)




    alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    while(True):
        stdscr.clear()
        title_str = mh.get_title(sort_int)
        m.title(stdscr, title_str)

        if var.menu_type == "volume":
            display_list = get_list.volume()
        elif var.menu_type == "issue":
            display_list = get_list.issue()
        elif var.menu_type == "articles":
            display_list = get_list.articles()
        elif var.menu_type == "authors":
            display_list = get_list.authors(sort_int)
        elif var.menu_type == "author_articles":
            display_list = get_list.author_articles()


        rows          = len(display_list)
        max_rows      = m.get_height(stdscr) - 5
        if max_rows > rows:
            max_rows  = rows
        num_pages     = ceil(rows / max_rows)
        last_page_row = arith.get_last_row(rows, max_rows, num_pages)

        status_msg = mh.get_status_bar(current_page, num_pages, sort_int)
        m.status_bar(stdscr, status_msg)

        l_row = "Page {} of {}".format(current_page, num_pages)
        m.last_row(stdscr, l_row)

        for i in range(0, max_rows):
            y_position = i + 1
            if not (current_page == num_pages and y_position >= last_page_row - 1):
                m.display_option(stdscr, y_position, x_start_pos, cursor_y, max_rows, num_pages, current_page, last_page_row, display_list)


        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()

        k = stdscr.getch()


        if k == curses.KEY_UP:
            cursor_y = calculate_y.up(cursor_y, current_page, num_pages, max_rows, rows, last_page_row)
        elif k == curses.KEY_DOWN:
            cursor_y = calculate_y.down(cursor_y, current_page, num_pages, max_rows, rows, last_page_row)

        elif k == curses.KEY_LEFT and not current_page == 1:
            cursor_y = 1
            current_page -= 1
        elif k == curses.KEY_LEFT and current_page == 1:
            mh.back()

        elif k == curses.KEY_RIGHT and not current_page == num_pages:
            cursor_y = 1
            current_page += 1


        elif var.menu_type == "authors":
            if k == 27:
                mh.back()

            elif k == ord('1'):
                sort_int = m.get_sort_1(sort_int)
                current_page = 1

            elif k == ord('2'):
                sort_int = m.get_sort_2(sort_int)
                current_page = 1

            elif k == 10:
                i              = arith.get_index(max_rows, num_pages, current_page, cursor_y, last_page_row)
                pre_display    = display_list[i]
                var.authors_y_pos = cursor_y
                var.author_name = pre_display["original"]
                var.author_current_page = current_page
                var.menu_type = "author_articles"
                menu(stdscr)

            else:
                letter = str(chr(k))
                if letter in alpha:
                    index = string_handler.get_index_of_letter(letter, display_list, sort_int)
                    if not index == -1:
                        page_cursor = arith.get_page_and_cursor(index, max_rows, num_pages)
                        current_page = page_cursor[0]
                        cursor_y = page_cursor[1]


        elif var.menu_type == "volume":
            if k == 27:
                mh.back()
            elif k == ord('n') and not current_page == num_pages:
                cursor_y - 1
                current_page  += 1

            elif k == ord('p'):
                if current_page == 1:
                    main.start()
                else:
                    cursor_y = 1
                    current_page -= 1

            elif k == 10:
                i = arith.get_index(max_rows, num_pages, current_page, cursor_y, last_page_row)
                volume_num = str(display_list[i])
                year = get_numbers.year(volume_num)
                if(len(volume_num) == 1):
                    volume_num = "0" + volume_num
                var.volume_y_pos = cursor_y
                var.volume_number = volume_num
                var.volume_year = year
                var.volume_current_page = current_page
                var.menu_type = "issue"
                menu(stdscr)

        elif var.menu_type == "issue":
            if k == 10:
                selected_issue = cursor_y - 1
                if selected_issue == 0:
                    selected_issue = "All"
                var.issue_number = selected_issue
                var.menu_type = "articles"
                var.issue_y_pos = cursor_y
                menu(stdscr)

            elif k == 27:
                mh.back()

        elif var.menu_type == "articles":
            i = arith.get_index(max_rows, num_pages, current_page, cursor_y, last_page_row)
            article_id = display_list[i]
            if k == 27:
                mh.back()

            elif k == 10 or k == ord('o'):
                get_url.by_article_id(article_id)

            elif k == ord('i'):
                article.start(article_id)

            elif k == ord('v'):
                var.issue_y_pos = 0
                var.articles_y_pos = 0
                var.menu_type = "volume"
                menu(stdscr)

        elif var.menu_type == "author_articles":
            i = arith.get_index(max_rows, num_pages, current_page, cursor_y, last_page_row)
            article_id = display_list[i]

            if k==27 or k == ord('a'):
                mh.back()

            elif k == 10 or k == ord('o'):
                get_url.by_article_id(article_id)

            elif k == ord('i'):
                var.author_articles_y_pos = cursor_y
                article.start(article_id)

        if var.menu_type == "volume" or var.menu_type == "issue"  or var.menu_type == "articles":
            if k == ord('m'):
                main.start()
            if k == ord('q'):
                sys.exit()


"""
menu_type = "volume", "issue", "authors", "articles
main_pos = cursor_y of main
current_page = 1 if coming from main

stdscr, menu_type, main_pos, authors_current_page, volume_number, vol_year, volume_current_page
"""
def start():
    curses.wrapper(menu)
