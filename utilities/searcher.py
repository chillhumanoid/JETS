#import statements
import os, curses
from database import get_author, get_article_id
from utilities import menu as m, arith, string_handler, calculate_y
from display import search
from math import ceil

def by_author(author_term):
    name = author_term.split(" ")
    x = 0
    found_names = []
    all_authors = get_author.all()
    article_id_list = []
    for x in name:
        for author in all_authors:
            names = author.lower()
            if "ö" in names:
                names = names.replace("ö", "o")
            if x.lower() in names:
                if not author in found_names:
                    found_names.append(author)
            else:
                if author in found_names:
                    found_names.remove(author)

        for author in found_names:
            for article_id in get_article_id.by_author(author):
                article_id_list.append(article_id)
    curses.wrapper(article_display, article_id_list, author_term, "")
def by_title(title_term):
    pass
def by_both(author_term, title_term):
    pass

def article_display(stdscr, display_list, author_term, title_term):
    x_start_pos = 1
    cursor_y = 1
    cursor_x = 1
    k = 0
    current_page = 1
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    while(True):
        stdscr.clear()
        title_str = "Search Results"

        m.title(stdscr, title_str)

        rows = len(display_list)
        if not rows == 0:
            max_rows = m.get_height(stdscr) - 5
            if max_rows > rows:
                max_rows = rows
            num_pages = ceil(rows / max_rows)
            last_page_row = arith.get_last_row(rows, max_rows, num_pages)
            if num_pages == 1:
                status_msg = " esc/'b' : Back to Search | 'o' : Open File | 'd' : Download"
            elif current_page == num_pages:
                status_msg = " 'p' : Previous | esc/'b' : Back | 'o' : Open File | 'd' : Download"
            elif current_page == 1:
                status_msg = " 'n' : Next | esc/'b' : Back | 'o' : Open File | 'd' : Download"
            else:
                status_msg = " 'n' : Next | 'p' : Previous | esc/'b' : Back | 'o' : Open File | 'd' : Download"
            l_row = "Page {} of {}".format(current_page, num_pages)
            m.last_row(stdscr, l_row)

            for i in range(0, max_rows):
                y_position = i + 1
                if not (current_page == num_pages and y_position >= last_page_row -1):
                    index = arith.get_index(max_rows, num_pages, current_page, y_position, last_page_row)
                    pre_display = display_list[index]
                    width = m.get_width(stdscr)
                    display = string_handler.display_string(pre_display, width, "search")
                    m.menu_option(stdscr, display, y_position, 1, cursor_y)

            stdscr.move(cursor_y, cursor_x)
            stdscr.refresh()
            k = stdscr.getch()
            i = arith.get_index(max_rows, num_pages, current_page, cursor_y, last_page_row)
            article_id = display_list[i]
            if k == curses.KEY_UP:
                cursor_y = calculate_y.up(cursor_y, current_page, num_pages, max_rows, rows, last_page_row)
            elif k == curses.KEY_DOWN:
                cursor_y = calculate_y.down(cursor_y, current_page, num_pages, max_rows, rows, last_page_row)
            elif k == curses.KEY_LEFT and not current_page == 1:
                cursor_y = 1
                current_page -= 1
            elif k == curses.KEY_LEFT and current_page == 1:
                search.start(title_term, author_term)
            elif k == curses.KEY_RIGHT and not current_page == num_pages:
                cursor_y = 1
                current_page += 1
            elif k == 10 or k == ord('o'):
                get_url.by_article_id(article_id)
            elif k == ord('i'):
                article.start(article_id)
            elif k == 27 or k == ord('b'):
                search.start(title_term, author_term)
        else:
            mid = (m.get_height(stdscr) - 6) // 2
            width = m.get_width(stdscr)
            display_msg = "0 RESULTS FOUND. PRESS ANY KEY TO TRY AGAIN"
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(mid, (width - len(display_msg))//2, display_msg)
            stdscr.attroff(curses.color_pair(3))

            stdscr.move(cursor_y, cursor_x)
            stdscr.refresh()
            k = stdscr.getch()
            if not k == 27:
                search.start(title_term, author_term)
            else:
                search.start(title_term, author_term)

"""
FILE CURRENTLY SAVED FOR FURTHER IMPLEMENTATION SAKE


import os, click
from database import get_title
from database import get_article_id
from database import get_author
#global variables

path = os.path.realpath(__file__)
path = path.replace("search.py","")
path = path + "Articles/"
all_path = path + "All/"
author_path = path + "Authors/"
#functions

def auth_search(author):
    name             = author.split(" ")
    x                = 0
    found_names      = []
    all_authors      = get_author.all()
    article_id_list  = []
    for x in name:
        for author in all_authors:

            names      = author.lower()

            if x.lower() in names:
                if not author in found_names:

                    found_names.append(author)

            else:
                if author in found_names:

                    found_names.remove(author)

        for author in found_names:
            for article_id in get_article_id.by_author(author):
                article_id_list.append(article_id)

    #display(article_id_list)

def article_search(term):
    found            = []
    article_id_list  = []
    click.echo()
    term             = term.lower()
    full_list        = get_title.all()

    if len(term) == 1:
        for item in full_list:
            if term in item[0].lower():
                found.append(item[1])

    elif len(term) > 1:
        for item in full_list:
            if term in item[0].lower():
                found.append(item[1])
        if len(found) == 0:
            for item in full_list:

                terms         = term.split(" ")
                title_lower   = item[0].lower()
                run           = 1

                for term in terms:

                    term = term.lower()

                    if term == "the" or term == "of" or term == "a" or term == "and" or term == "or" or term == "if" or term == "&" or term == "is" or term == "on":
                        temporary = 0

                    elif term in title_lower and run == 1:
                        found.append(item[1])
                        run = run + 1

                    if term not in title_lower:
                        run = run + 1

                        if item[0] in found:
                            found.remove(item[1])
    for full_number in found:
        article_id_list.append(get_article_id.by_full_number(full_number))
    #display(article_id_list)
"""
