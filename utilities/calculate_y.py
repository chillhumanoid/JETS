def up(cursor_y, current_page, num_pages, max_rows, rows, last_page_row):
    cursor_y -= 1
    if cursor_y == 0:
        if current_page == num_pages:
            if num_pages == 1:
                cursor_y = rows
            else:
                if rows == 1:
                    cursor_y = 1
                else:
                    cursor_y = last_page_row - 2
        else:
            cursor_y = max_rows
    return cursor_y
def down(cursor_y, current_page, num_pages, max_rows, rows, last_page_row):
    cursor_y += 1
    if current_page == num_pages:
        if num_pages == 1:
            if cursor_y == rows + 1:
                cursor_y = 1
        else:
            if cursor_y >= last_page_row - 1:
                cursor_y = 1
    else:
        if cursor_y >= max_rows + 1:
            cursor_y = 1
    return cursor_y
def left():
    pass
def right():
    pass
