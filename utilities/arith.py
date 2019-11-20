from math import *


def title_start(title, width):
    start_pos = int((width // 2) - (len(title) // 2) - len(title) % 2)
    return start_pos

def get_page_num(rows, max_rows):
    if rows > max_rows:
        return ceil(rows/max_rows)
    else:
        return 1

def get_last_row(rows, max_rows, num_pages):
    if rows > max_rows:
        return (rows - (max_rows * (num_pages - 1)) + 2)
    else:
        return rows - 1

def get_max_title_len(width, a_len):
    length = width - 7 #5 spots are spaces, 2 are dividiers (|)
    length -= 5 # the volume number and issue number will always be 5 total
    length -= a_len #length for author string
    return length

def get_index(max_rows, num_pages, current_page, cursor_y, last_row):
    i = cursor_y
    if current_page == 1:
        return i - 1
    elif current_page == num_pages:
        if not i == last_row - 1:
            return (i + (max_rows * (current_page - 1)) - 1)
    else:
        return (i + (max_rows * (current_page - 1)) - 1)

def get_page_and_cursor(index_number, max_rows, num_pages):
    if index_number == 0:
        page = 1
        cursor_pos = 1
    else:
        page = ceil(index_number / max_rows)
        leftover = index_number % max_rows
        cursor_pos = (index_number % max_rows) + 1
        if leftover == 0:
            page += 1
    data = [page, cursor_pos]
    return data
