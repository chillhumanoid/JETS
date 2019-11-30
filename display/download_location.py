import os, curses, sys
from utilities import variables as var,downloads,  menu as m, menu_helpers as mh, files
import tkinter as tk
from tkinter import filedialog
from display import main

def key_up():
    global cursor_y
    cursor_y -= 1
    if cursor_y == 4:
        cursor_y = 7

def key_down():
    global cursor_y
    cursor_y += 1
    if cursor_y == 8:
        cursor_y = 5

def get_option(char):
    if char == ord('1'):
        root = tk.Tk()
        root.withdraw()
        new_path = filedialog.askdirectory()
        isOkay = files.change_path(new_path, var.download_folder)
    elif char == ord('2'):
        downloads.delete_all()
    elif char == ord('3'):
        main.start()

def menu(stdscr):
    current_location = var.download_folder
    global cursor_y
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
        k = 0
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
            key_up()
        elif k == curses.KEY_DOWN:
            key_down()
        elif k == 10 or k == curses.KEY_RIGHT:
            char = int.from_bytes(stdscr.instr(cursor_y, 1, 1), byteorder='little')
            get_option(char)
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
