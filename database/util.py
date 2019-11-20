def quotate(string):
    if "'" in string:
        string = '"' + string + '"'
    else:
        string = "'" + string + "'"
    return string
