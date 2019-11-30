import os, curses, sys
from utilities import variables as var, downloads, menu as m, menu_helpers as mh
import tkinter as tk
from tkinter import filedialog
from display import main
def menu(stdscr):
    current_location = var.download_folder

    cursor_y = 5
    k = 0

    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    height, width = stdscr.getmaxyx()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)

    title_str = "Download Info"
    status_msg = " 'm' : Main Menu | 'q' : Quit"
    option_1 = "1. Change Directory"
    option_2 = "2. Delete All Files"
    option_3 = "3. Exit"

    while(True):
        info_1 = "Current Directory: {}".format(current_location)
        info_2 = "Downloaded Files: {}".format(downloads.get_files())
        info_3 = "Directory Size: {}".format(downloads.get_size())

        stdscr.clear()
        m.title(stdscr, title_str)
        m.status_bar(stdscr, status_msg)
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(1, 1, info_1)
        stdscr.addstr(2, 1, info_2)
        stdscr.addstr(3, 1, info_3)
        stdscr.attroff(curses.color_pair(1))

        m.menu_option(stdscr, option_1, 5, 1, cursor_y)
        m.menu_option(stdscr, option_2, 6, 1, cursor_y)
        m.menu_option(stdscr, option_3, 7, 1, cursor_y)
        stdscr.move(cursor_y, 1)
        stdscr.refresh()
        k = stdscr.getch()
        if k == curses.KEY_UP:
            cursor_y -= 1
            if cursor_y == 4:
                cursor_y = 7
        elif k == curses.KEY_DOWN:
            cursor_y += 1
            if cursor_y == 8:
                cursor_y = 5
        elif k == 10 or k == curses.KEY_RIGHT:
            char = int.from_bytes(stdscr.instr(cursor_y, 1, 1), byteorder='little')
            if char == ord('1'):
                root = tk.Tk()
                root.withdraw()
                new_path = filedialog.askdirectory()
                if not new_path == "":
                    file_path = os.path.join(new_path, 'JETS')
                    file_path = file_path.replace("/", "\\")
                    if not file_path == current_location:
                        if os.path.exists(current_location):
                            os.rename(current_location, file_path)
                            downloads.set_location(file_path)
                            current_location = var.download_folder
            elif char == ord('2'):
                downloads.delete_all()
            elif char == ord('3'):
                main.start()
        elif k == curses.KEY_LEFT or k == ord('m') or k == 27:
            main.start()
        elif k == ord('q'):
            sys.exit()
        elif k == ord('1'):
            cursor_y = 5
        elif k == ord('2'):
            cursor_y = 6
        elif k == ord('3'):
            cursor_y = 7


def start():
    curses.wrapper(menu)
