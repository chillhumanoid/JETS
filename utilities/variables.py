from utilities import login, downloads
def init():
    global main_position
    main_position = 1
    global menu_type
    menu_type = "main"
    global volume_y_pos
    volume_y_pos = 0
    global issue_y_pos
    issue_y_pos = 0
    global articles_y_pos
    articles_y_pos = 0
    global authors_y_pos
    authors_y_pos = 0
    global author_articles_y_pos
    author_articles_y_pos = 0
    global author_current_page
    author_current_page = 0
    global author_name
    author_name = ""
    global volume_number
    volume_number = 0
    global volume_year
    volume_year = 0
    global volume_current_page
    volume_current_page = 0
    global issue_number
    issue_number = 0
    global isLogged
    #isLogged = login.check_login()
    isLogged = False
    global download_folder
    download_folder = downloads.get_location()
    global downloaded_files
    downloaded_files = downloads.get_files()
