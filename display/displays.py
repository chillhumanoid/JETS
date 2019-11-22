import curses, sys
from utilities import get_year as get, menu_helpers, arith, sort_dict, string_handler, open
from math import ceil
from database import get_numbers, get_author, get_article, get_article_id
from menus import main
from display import article
"""
testing capability to reuse menu logic
"""
def menu(stdscr, menu_type, main_pos, authors_current_page, volume_number, volume_year, volume_current_page, issue_number, author_name):
    x_start_pos = 1
    cursor_y = 1
    cursor_x = 1
    k = 0
    if menu_type == "authors":
        current_page = authors_current_page
    elif menu_type == "volume":
        current_page = volume_current_page
    else:
        current_page = 1
    alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    sort_int = 1
    print(menu_type)
    while(True):
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        title = menu_helpers.get_title(menu_type, sort_int, volume_number, volume_year, issue_number, author_name)
        

        start_x_title = arith.title_start(title, width)

        if menu_type == "authors":
            names = get_author.all()
            if sort_int == None:
                sort_int == 1
            names_dict = sort_dict.create(names)
            display_list = sort_dict.sort(names_dict, sort_int)
        elif menu_type == "volume":
            vol = get_numbers.volumes()
            display_list = sorted(vol)
        elif menu_type == "issue":
            display_list = sorted(get_numbers.issues_in_volume(volume_number))
            display_list.insert(0, "All")
        elif menu_type == "articles":
            if issue_number == "All":
                display_list = get_article.by_volume(volume_number)
            else:
                display_list = get_article.by_issue(volume_number, issue_number)
        elif menu_type == "author_articles":
            display_list = get_article_id.by_author(author_name)

        
        rows = len(display_list)
        if menu_type == "issue" or menu_type == "author_articles":
            max_rows = rows
        else:
            max_rows = height - 5
        num_pages = ceil(rows / max_rows)
        last_row = arith.get_last_row(rows, max_rows, num_pages)
        status_bar = menu_helpers.get_status_bar(menu_type, current_page, num_pages, sort_int)

        l_row = "Page {} of {}".format(current_page, num_pages)

        stdscr.attron(curses.color_pair(1))
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(0, start_x_title, title)
        stdscr.attroff(curses.A_BOLD)
        stdscr.attroff(curses.color_pair(1))

        stdscr.addstr(height - 3, x_start_pos, l_row)
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height - 1, 0, status_bar)
        stdscr.addstr(height - 1, len(status_bar), " "  * (width - len(status_bar) - 1))
        stdscr.attroff(curses.color_pair(3))

        for i in range(0, max_rows):
            y_position = i + 1
            if (not (current_page == num_pages and y_position >= last_row - 1)) or menu_type == "issue" or menu_type == "author_articles":
                if (not (i + (max_rows * (current_page - 1)) - 1) > rows):
                    index = arith.get_index(max_rows, num_pages, current_page, y_position, last_row)
                    pre_display = display_list[index]
                    display = menu_helpers.get_display_row(menu_type, pre_display, volume_number, volume_year, width)
                    if cursor_y == y_position:
                        stdscr.attron(curses.color_pair(3))
                    stdscr.addstr(y_position, x_start_pos, display)
                    if cursor_y == y_position:
                        stdscr.attroff(curses.color_pair(3))
        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()

        k = stdscr.getch()

        
        if k == curses.KEY_UP:
            cursor_y -= 1
            if cursor_y == 0:
                if current_page == num_pages:
                    cursor_y = last_row - 2
                else:
                    cursor_y = max_rows
        
        elif k == curses.KEY_DOWN:
            cursor_y += 1
            if current_page == num_pages:
                if cursor_y == last_row - 1:
                    cursor_y = 1
            else:
                if cursor_y == max_rows + 1:
                    cursor_y = 1
        
        elif k == curses.KEY_LEFT and not current_page == 1:
            cursor_y = 1
            current_page -= 1
        elif k == curses.KEY_LEFT and current_page == 1:
            main.start(main_pos)
        elif k == curses.KEY_RIGHT and not current_page == num_pages:
            cursor_y = 1
            current_page += 1


        if menu_type == "authors":
            if k == 27:
                main.start(main_pos)

            elif k == ord('1'):
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

            elif k == 10:
                i = arith.get_index(max_rows, num_pages, current_page, cursor_y, last_row)
                pre_display = display_list[i]
                print(pre_display)
                author = sort_dict.get_name(pre_display)
                menu(stdscr, "author_articles", main_pos, current_page, 0, 0, 0, 0, author)

            else:
                letter = str(chr(k))
                if letter in alpha:
                    index = string_handler.get_index_of_letter(letter, display_list, sort_int)
                    if not index == -1:
                        page_cursor = arith.get_page_and_cursor(index, max_rows, num_pages)
                        current_page = page_cursor[0]
                        cursor_y = page_cursor[1]
        
            
        elif menu_type == "volume":
            if k == 27:
                main.start(main_pos)

            elif k == ord('n') and not current_page == num_pages:
                cursor_y - 1
                current_page  += 1

            elif k == ord('p'):
                if current_page == 1:
                    main.start(main_pos)

                else:
                    cursor_y = 1
                    current_page -= 1

            elif k == 10:
                i = arith.get_index(max_rows, num_pages, current_page, cursor_y, last_row)
                pre_display = str(display_list[i])
                year = get.year(pre_display)
                if(len(pre_display) == 1):
                    pre_display = "0" + pre_display
                menu(stdscr, "issue", main_pos, 0, pre_display, year, current_page, issue_number, "")

        elif menu_type == "issue":
            if k == 10:
                selected_issue = cursor_y - 1

                if selected_issue == 0:
                    selected_issue = "All"
                menu(stdscr, "articles", main_pos, 0, volume_number, volume_year, volume_current_page, selected_issue, "")

            elif k == 27:
                menu(stdscr, "volume", main_pos, 0, 0, 0, volume_current_page, issue_number, "")

        elif menu_type == "articles":
            i = arith.get_index(max_rows, num_pages, current_page, cursor_y, last_row)
            article_id = display_list[i]
            if k == 27:
                menu(stdscr, "issue", main_pos, 0, volume_number, volume_year, volume_current_page, issue_number, "")
            elif k == 10 or k == ord('o'):
                full_number = get_numbers.full(article_id)
                open.open_file(full_number)
            elif k == ord('i'):
                article.start(article_id, volume_number, volume_year, issue_number, volume_current_page, main_pos)
            elif k == ord('v'):
                menu(stdscr, "volume", main_pos, 0, 0, 0, volume_current_page, issue_number, "")
        elif menu_type == "author_articles":
            i = arith.get_index(max_rows, num_pages, current_page, cursor_y, last_row)
            article_id = display_list[i]
            if k==27:
                print(current_page)
                menu(stdscr, "authors", main_pos, authors_current_page, 0, 0, 0, 0, author_name)
            elif k == 10 or k == ord('o'):
                full_number = get_numbers.full(article_id)
                open.open_file(full_number)
            elif k == ord('i'):
                article.start(article_id, volume_number, volume_year, issue_number, volume_current_page, main_pos)
        if menu_type == "volume" or menu_type == "issue"  or menu_type == "articles":
            if k == ord('m'):
                main.start(main_pos)
            if k == ord('q'):
                sys.exit()


"""
menu_type = "volume", "issue", "authors", "articles
main_pos = cursor_y of main
current_page = 1 if coming from main

stdscr, menu_type, main_pos, authors_current_page, volume_number, vol_year, volume_current_page
"""
def start(menu_type, main_pos, authors_current_page, volume_number, volume_year, volume_current_page, issue_number, author_name):
    curses.wrapper(menu, menu_type, main_pos, authors_current_page, volume_number, volume_year, volume_current_page, issue_number, author_name)
