import curses
from display import main
from utilities import menu as m, inputs, searcher

def menu(stdscr, title_term, author_term):
    cursor_y = 2

    stdscr.clear()
    stdscr.refresh()

    height, width = stdscr.getmaxyx()

    curses.curs_set(True)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

    title_str = "Search The JETS Archive"
    status_msg = " To search, enter a term and/or author and press enter | 'm'/esc : Back | 'q' : Quit"

    title_label = "Search By Title: "
    author_label = "Search By Author: "
    x_pos_title = len(title_label) + 2
    x_pos_author = len(author_label) + 2
    title_search = ""
    author_search = ""
    cursor_x = x_pos_title
    isError = False
    while(True):
        stdscr.clear()
        m.title(stdscr, title_str)
        m.status_bar(stdscr, status_msg)
        m.login_option(stdscr, title_label, 2, 2, cursor_y, False)
        m.login_option(stdscr, author_label, 3, 2, cursor_y, False)

        m.add_string(stdscr, title_search, 2, x_pos_title)
        m.add_string(stdscr, author_search, 3, x_pos_author)
        if isError:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(4,  (width - len("Please Enter A Term")) // 2, "Please Enter A Term")
            stdscr.attroff(curses.color_pair(2))
        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()

        k = stdscr.getch()
        if k == 27:
            main.start()
        elif k == 9:
            if cursor_y == 2:
                cursor_y = 3
                cursor_x = x_pos_author + len(author_search)
            elif cursor_y == 3:
                cursor_y = 2
                cursor_x = x_pos_title + len(title_search)
        elif k == 10:
            if cursor_y == 2:
                cursor_y = 3
                cursor_x = x_pos_author
            elif cursor_y == 3:
                if len(title_search) == 0 and len(author_search) == 0:
                    isError = True
                else:
                    if len(title_search) == 0:
                        searcher.by_author(author_search)
                    elif len(author_search) == 0:
                        searcher.by_title(title_search)
                    elif len(title_search) > 0 and len(author_search) > 0:
                        searcher.by_both(author_search, title_search)
        elif k == curses.KEY_UP or k == curses.KEY_DOWN:
            if cursor_y == 3:
                cursor_y = 2
                cursor_x = x_pos_title + len(title_search)
            elif cursor_y == 2:
                cursor_y = 3
                cursor_x = x_pos_author + len(author_search)
        elif k == curses.KEY_LEFT:
            if cursor_y == 2 and not cursor_x <= x_pos_title:
                cursor_x -= 1
            elif cursor_y == 3 and not cursor_x == x_pos_author:
                cursor_x -= 1
        elif k == curses.KEY_RIGHT:
            if cursor_y == 2 and not cursor_x >= x_pos_title + len(title_search):
                cursor_x += 1
            elif cursor_y == 3 and not cursor_x >= x_pos_author + len(author_search):
                cursor_x += 1
        elif cursor_y == 2:
            title_search = inputs.handler(title_search, k, x_pos_title, cursor_x)
            cursor_x = x_pos_title + len(title_search)
        elif cursor_y == 3:
            author_search = inputs.handler(author_search, k, x_pos_author, cursor_x)
            cursor_x = x_pos_author + len(author_search)

def start(title_term, author_term):
    curses.wrapper(menu, title_term, author_term)
