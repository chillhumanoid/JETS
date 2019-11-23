from utilities import sort_dict, string_handler
"""
gets the title for the menu based on menu_type (authors, ) and sort_int(1-4 or 1 if not sortable)
"""
def get_title(menu_type, sort_int, volume_number, year, issue_number, author_name):
    if menu_type == "authors":
        if sort_int == 1:
            return  "JETS Author Listing - Sorted by Last (A-Z)"
        elif sort_int == 2:
            return "JETS Author Listing - Sorted by Last (Z-A)"
        elif sort_int == 3:
            return "JETS Author Listing - Sorted by First (A-Z)"
        elif sort_int == 4:
            return "JETS Author Listing - Sorted by First (Z-A)"
    elif menu_type == "volume":
        return "JETS by Volume (Year)"
    elif menu_type == "issue":
        return "Volume {} ({})".format(volume_number, year)
    elif menu_type == "articles":
        if issue_number == "All":
            return "Volume {} ({}) - All Issues".format(volume_number, year)
        else:
            return "Volume {} ({}) - Issue {}".format(volume_number, year, issue_number)
    elif menu_type == "author_articles":
        return "Articles by {}".format(author_name)

def get_display_row(menu_type, display, volume_number, year, width):
    if menu_type == "authors":
        return sort_dict.get_name(display)
    elif menu_type == "volume":
        display_number = string_handler.display_number(str(display))
        display = string_handler.display_volume(display_number, str(display))
        return display
    elif menu_type == "issue":
        number = str(display)
        return "Vol {} ({}) - Issue {}".format(volume_number, year, number)
    elif menu_type == "articles" or menu_type == "author_articles":
        return string_handler.display_string(display, width, menu_type)

def get_status_bar(menu_type, current_page, num_pages, sort_int):
    menuStr1 = "'m' : Main Menu"
    menuStr2 = "'m'/esc : Main Menu"
    menuStr3 = "esc : Main Menu"
    nextStr = "'n' : Next"
    prevStr = "'p' : Previous"
    openStr = "'o' : Open"
    infoStr =  "'i' : Info"
    issueStr = "esc : Issue Selection"
    volStr1 = "'v' : Volume Selection"
    volStr2 = "'p'/'v'/esc : Volume Selection"
    arrowStr = "arrow keys : Navigation"
    alphaStr = "(a-z) : Go to Letter"
    authorStr = "'a'/esc : Back to Author"
    if menu_type == "authors":
        current = "Last"
        cur2 = "Z-A"
        if sort_int == 1:
            current = "First"
            cur2 = "Z-A"
        elif sort_int == 2:
            current = "First"
            cur2 = "A-Z"
        elif sort_int == 3:
            current = "Last"
            cur2 = "Z-A"
        elif sort_int == 4:
            current = "Last"
            cur2 = "A-Z"
        return " {} | {} | {} | 1: Sort by {} | 2: Sort ({})".format(menuStr3, arrowStr, alphaStr, current, cur2)
    elif menu_type == "volume":
        if current_page == 1:
            return " {} | {}".format(nextStr, menuStr2)
        elif current_page == num_pages:
            return " {} | {}".format(prevStr, menuStr2)
        else:
            return " {} | {} | {}".format(nextStr, prevStr, menuStr2)

    elif menu_type == "issue":
        return " {} | {} ".format(volStr2, menuStr1)
    elif menu_type == "articles":
        if num_pages == 1:
            return " {} | {} | {} | {} | {}".format(openStr, infoStr, issueStr, volStr1, menuStr1)
        elif current_page == 1 and not num_pages == 1:
            return " {} | {} | {} | {} | {} | {}".format(nextStr, openStr, infoStr, issueStr, volStr1, menuStr1)
        elif current_page == num_pages and not num_pages == 1:
            return " {} | {} | {} | {} | {} | {}".format(prevStr, openStr, infoStr, issueStr, volStr1, menuStr1)
        else:
            return " {} | {} | {} | {} | {} | {} | {}".format(nextStr, prevStr, openStr, infoStr, issueStr, volStr1, menuStr1)
    elif menu_type == "author_articles":
        if num_pages == 1:
            return " {} | {} | {} | {}".format(openStr, infoStr, authorStr, menuStr1)
        if current_page == 1 and not num_pages == 1:
            return " {} | {} | {} | {} | {}".format(nextStr, openStr, infoStr, authorStr, menuStr1)
        elif current_page == num_pages:
            return " {} | {} | {} | {} | {}".format(prevStr, openStr, infoStr, authorStr, menuStr1)
        else:
            return " {} | {} | {} | {} | {} | {}".format(nextStr, prevStr, openStr, infoStr, authorStr, menuStr1)
