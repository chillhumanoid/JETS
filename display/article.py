import curses
from database import get_title, get_author, get_numbers, get_url
from display import displays, main
from utilities import variables as var

def menu(stdscr, article_id):
    x_start_pos = 1
    k           = 0
    full_number = get_numbers.full(article_id)
    stdscr.clear()
    stdscr.refresh()
    x_start_pos = 2
    x_indent = 6

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
 #menu_type, main_pos, authors_current_page, volume_number, volume_year, volume_current_page, issue_number, author_name):
    while True:
        if var.menu_type == "articles" or var.menu_type == "author_articles":
            if k == ord('m'):
                main.start()
            elif k == ord('o'):
                get_url.by_article_id(article_id)
            elif k == ord('d'):
                pass ## TODO: Downloader
            if var.menu_type == "articles":
                status_bar = " 'o' : Open | 'b'/esc : Back | 'i' : Issue Selection | 'v' : Volume Selection | 'd' : Download | 'm' : Main Menu"
                if k == ord('i'):
                    var.menu_type = "issue"
                    var.articles_y_pos = 0
                    displays.start()
                elif k == ord('v'):
                    var.menu_type = "volume"
                    var.articles_y_pos = 0
                    var.issue_y_pos = 0
                    var.issue_number = 0
                    var.volume_number = 0
                    var.volume_year = 0
                    displays.start()
                elif k == 27 or k == curses.KEY_LEFT or k == ord('b'):
                    displays.start()
            elif var.menu_type == "author_articles":
                status_bar = " 'o' : Open | 'b'/esc : Back | 'a' : Author Selection | 'd' : Download | 'm' : Main Menu"
                if k == 27 or k == ord('b') or k == curses.KEY_LEFT:
                    displays.start()
                elif k == ord("a"):
                    var.author_articles_y_pos = 0
                    var.menu_type = "authors"
                    displays.start()
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            title = get_title.by_article_id(article_id)
            authors = get_author.by_article_id(article_id)
            volume = full_number.split(".")[0]
            issue = full_number.split(".")[1]
            article = full_number.split('.')[2]
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

def start(article_id):
    curses.wrapper(menu, article_id)
