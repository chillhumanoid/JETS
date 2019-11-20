import curses, sys, os
from database import get_title, get_author, get_numbers
from display import articles
from utilities import open
from menus import main, by_issue, by_volume_year
def menu(stdscr, article_id, volume_number, year, issue_number, volume_current_page):
    curses.curs_set(0)

    k = 0

    stdscr.clear()
    stdscr.refresh()
    x_start_pos = 2
    x_indent = 6

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while True:
        if k == 27 or k == curses.KEY_LEFT or k == ord('b'):
            articles.start(volume_number, year, issue_number, volume_current_page)
        elif k == ord('m'):
            main.start()
        elif k == ord('i'):
            by_issue.start(volume_number, year, issue_number, volume_current_page)
        elif k == ord('v'):
            by_volume_year.start(volume_current_page)
        else:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            status_bar = "'o' : Open | 'b'/esc : Article Selection | 'i' : Issue Selection | 'v' : Volume Selection | 'm' : Main Menu"
            title = get_title.by_article_id(article_id)
            authors = get_author.by_article_id(article_id)
            full_number = get_numbers.full(article_id)
            volume = full_number.split(".")[0]
            issue = full_number.split(".")[1]
            article = full_number.split('.')[2]
            if k == ord('o'):
                open.open_file(full_number)
            stdscr.attron(curses.color_pair(1))
            first_line = "Article {} from Volume {} Issue {}".format(article, volume, issue)
            stdscr.addstr(0, x_start_pos, first_line)
            stdscr.attroff(curses.color_pair(1))

            second_line = "Title: "
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(2, x_start_pos, second_line)
            stdscr.attroff(curses.color_pair(1))

            stdscr.addstr(3, x_indent, title)

            third_line = "Authors:"
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(5, x_start_pos, third_line)
            stdscr.attroff(curses.color_pair(1))

            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(height-1, 0, status_bar)
            stdscr.addstr(height-1, len(status_bar), " " * (width - len(status_bar) - 1))
            stdscr.attroff(curses.color_pair(3))

            y_start = 6
            for name in authors:
                stdscr.addstr(y_start, x_indent, name)
                y_start += 1
            stdscr.move(0,0)
            stdscr.refresh()
            k = stdscr.getch()

def start(article_id, volume_number, year, issue_number, volume_current_page):
    curses.wrapper(menu, article_id, volume_number, year, issue_number, volume_current_page)
