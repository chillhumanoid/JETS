def handler(text, k, x_pos_max, cursor_x):
    valid_symbols = "!@#$%^&*()'\"_-+={} :[]"
    char = str(chr(k))
    if k == 8 and not len(text) == 0:
        text = backspace(text, x_pos_max, cursor_x)
    elif char.isalnum() or char in valid_symbols:
        text = add_char(cursor_x, text, x_pos_max, char)
    return text

def backspace(text, x_pos_max, cursor_x):
    if not (cursor_x == x_pos_max + len(text)) and (not cursor_x - 1 < x_pos_max):
        s_pos = cursor_x - x_pos_max
        text = text[:s_pos - 1] + text[s_pos:]
    else:
        text = text[:-1]
    return text

def add_char(cursor_x, text, x_pos_max, char):
    if not cursor_x == x_pos_max + len(text):
        s_pos = cursor_x - x_pos_max
        text = text[:s_pos] + char + text[s_pos:]
    else:
        text = text + char
    return text
