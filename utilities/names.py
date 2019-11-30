def get_authors(author_list):
    fullName = []
    for name in author_list:
        if not name == "JETS":
            first_name = name[0:1] + "."
            full_name = name.split(" ")
            full_name[0] = first_name
            if "Jr" in full_name or "III" in full_name or "Jr." in full_name or "IV" in full_name or "II" in full_name:
                last_location = len(full_name) - 2
            else:
                last_location = len(full_name) - 1
                if not last_location == 1:
                    full_name = get_middle(last_location, full_name)
            name = ' '.join(full_name)
            fullName.append(name)
        else:
            return "JETS"
    author = ', '.join(fullName)
    return author

def get_middle(location, full_name):
    middle_location = location - 1
    middle = full_name[middle_location]
    if not len(middle) == 2:
        middle = middle[0:1] + "."
        full_name[middle_location] = middle
        if not middle_location <= 1:
            return get_middle(middle_location, full_name)
    return full_name

def shorten_first(first):
    if len(first) >= 1 and len(first) <= 2:
        return first
    else:
        first = first[:1] + "."
        return first
