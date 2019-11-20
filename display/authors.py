from menus import main
import sys, curses, os
from database import get_author
from utilities import arith, sort_dict


def menu(stdscr, current_page, sort_int):
    #SORT INT: 1 - by last a-z 2 - by last z-a 3 - by first a-z 4 - by first z-a
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
    while (True):
        if k == 27:
            main.start()
        else:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            if sort_int == 1:
                title = "JETS Author Listing - Sorted by Last  (A-Z)"
                status_bar = " esc : Main Menu | arrow keys : Navigation | '(a-z) : go to that alpha | 1: Sort by First | 2: Sort (Z-A) '"
            elif sort_int == 2:
                title = "JETS Author Listing - Sorted by Last  (Z-A)"
                status_bar = " esc : Main Menu | arrow keys : Navigation | '(a-z) : go to that alpha | 1: Sort by First | 2: Sort (A-Z) '"
            elif sort_int == 3:
                title = "JETS Author Listing - Sorted by First (A-Z)"
                status_bar = " esc : Main Menu | arrow keys : Navigation | '(a-z) : go to that alpha | 1: Sort by Last  | 2: Sort (Z-A) '"
            elif sort_int == 4:
                title = "JETS Author Listing - Sorted by First (Z-A)"
                status_bar = " esc : Main Menu | arrow keys : Navigation | '(a-z) : go to that alpha | 1: Sort by Last | 2: Sort (A-Z) '"
            start_x_title = arith.title_start(title, width)
            stdscr.attron(curses.color_pair(1))
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(0, start_x_title, title)
            stdscr.attroff(curses.A_BOLD)
            stdscr.attroff(curses.color_pair(1))


            author_names = get_author.all()
            author_names_dict = sort_dict.create(author_names)
            author_list = sort_dict.sort(author_names_dict, sort_int)

            rows = len(author_names)

            max_rows = height - 4
            num_pages = arith.get_page_num(rows, max_rows)
            last_row = arith.get_last_row(rows, max_rows, num_pages)




            l_row = "Page {} of {}".format(current_page, num_pages)

            stdscr.addstr(height-3, x_start_pos, l_row)
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(height-1, 0, status_bar)
            stdscr.addstr(height-1, len(status_bar), " " * (width - len(status_bar) - 1))
            stdscr.attroff(curses.color_pair(3))


            for i in range(0, max_rows - 1):
                y_position = i + 1
                index = arith.get_index(max_rows, num_pages, current_page, y_position, False)
                if not (current_page == num_pages and y_position >= last_row):
                    dict = author_list[index]
                    first = dict["first"]
                    middle = dict["middle"]
                    post = dict["post"]
                    last = dict["last"]
                    author = first + middle + last + post
                    if cursor_y == y_position:
                        stdscr.attron(curses.color_pair(3))
                    stdscr.addstr(y_position, x_start_pos, author)
                    if cursor_y == y_position:
                        stdscr.attroff(curses.color_pair(3))
            if k == 10:
                i = arith.get_index(max_rows, num_pages, current_page, cursor_y, False)
                dict = author_list[i]
                first = dict["first"]
                middle = dict["middle"]
                post = dict["post"]
                last = dict["last"]
                author = first + middle + last + post
                print(author)
                sys.exit()


            stdscr.move(cursor_y, cursor_x)
            stdscr.refresh()

            k = stdscr.getch()
            if k == ord('1'):
                current_page = 1
                if sort_int == 1:
                    sort_int = 3
                elif sort_int == 2:
                    sort_int = 4
                elif sort_int == 3:
                    sort_int = 1
                elif sort_int == 4:
                    sort_int = 2

            elif k == ord('2'):
                current_page = 1
                if sort_int == 1:
                    sort_int = 2
                elif sort_int == 2:
                    sort_int = 1
                elif sort_int == 3:
                    sort_int = 4
                elif sort_int == 4:
                    sort_int = 3
            if k == ord('d'):
                if current_page == 1:
                    current_page = 35
                elif current_page == 35:
                    current_page = 1
            elif k == ord('r'):
                current_page = 1
            if k == curses.KEY_UP:
                cursor_y -= 1
                if cursor_y == 0:
                    if current_page == num_pages:
                        cursor_y = last_row - 1
                    else:
                        cursor_y = max_rows - 1
            elif k == curses.KEY_DOWN:
                cursor_y += 1
                if current_page == num_pages:
                    if cursor_y == last_row:
                        cursor_y = 1
                else:
                    if cursor_y == max_rows:
                        cursor_y = 1
            elif k == curses.KEY_LEFT and not current_page == 1:
                cursor_y = 1
                current_page -= 1
            elif k == curses.KEY_LEFT and current_page == 1:
                main.start()
            elif (k == curses.KEY_RIGHT) and not current_page == num_pages:
                cursor_y = 1
                current_page += 1



def start(current_page, sort_int):
    curses.wrapper(menu, current_page, sort_int)
