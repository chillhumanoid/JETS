from operator import itemgetter
"""
splits author names into first and last
creates dictionary from the list
"""
def create(list):
    dict_list = []
    for name in list:
        full_name = name.split(" ")
        first = full_name[0]
        middle = " "
        postfix = ""
        if "Jr" in full_name or "III" in full_name or "II" in full_name or "IV" in full_name or "Jr." in full_name:
            last_location = len(full_name) - 2
            postfix = full_name[len(full_name) - 1]
            postfix = " " + postfix
        else:
            last_location = len(full_name) - 1
        last = full_name[last_location]
        if not last_location == 1:
            middle_full = get_middle(last_location, full_name, [])
            middle = ' '.join(middle_full)
            middle = " " + middle + " "
        name_dict = {"first":first, "middle":middle, "last":last, "post":postfix}
        dict_list.append(name_dict)
    return dict_list

def sort(list, num):
    if num == 1:
        return sorted(list, key=itemgetter('last'))
    elif num == 2:
        return sorted(list, key=itemgetter('last'), reverse = True)
    elif num == 3:
        return sorted(list, key=itemgetter('first'))
    elif num == 4:
        return sorted(list, key=itemgetter('first'), reverse = True)

def get_middle(location, full_name, middle_full):
    middle_end = location - 1
    middle = full_name[middle_end]
    if not len(middle) == 2:
        middle = middle[0:1] + "."
        full_name[middle_end] = middle
        middle_full.append(middle)
        if not middle_end <= 1:
            return get_middle(middle_end, full_name, middle_full)
    else:
        middle_full.append(middle)
    return middle_full

def get_name(dict):
    first = dict["first"]
    middle = dict["middle"]
    post = dict["post"]
    last = dict["last"]
    author = first + middle + last + post
    return author

def get_all_names(list):
    names = []
    for dict in list:
        names.append(get_name(dict))
    return names
