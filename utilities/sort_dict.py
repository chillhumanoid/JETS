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
        if not last_location == 1 or last_location == 0:
            middle_full = get_middle(last_location, full_name, [], first)
            middle = ' '.join(middle_full)
            middle = " " + middle + " "
        name_dict = {"first":first, "middle":middle, "last":last, "post":postfix}
        dict_list.append(name_dict)
    return dict_list

def sort(lis, num):
    if num == 1:
        return sorted(lis, key=itemgetter('last'))
    elif num == 2:
        return sorted(lis, key=itemgetter('last'), reverse = True)
    elif num == 3:
        return sorted(lis, key=itemgetter('first'))
    elif num == 4:
        return sorted(lis, key=itemgetter('first'), reverse = True)

def get_middle(location, full_name, middle_full, first):
    middle_end = location - 1
    middle = full_name[middle_end]
    if not len(middle) == 2:
        if not len(first) == 2:
            middle = middle[0:1] + "."
            full_name[middle_end] = middle
            middle_full.append(middle)
            if not middle_end <= 1:
                return get_middle(middle_end, full_name, middle_full, first)
        else:
            middle_full.append(middle)
    else:
        middle_full.append(middle)
    return middle_full

def get_name(dic):
    first = dic["first"]
    middle = dic["middle"]
    post = dic["post"]
    last = dic["last"]
    author = first + middle + last + post
    return author

def get_all_names(lis):
    names = []
    for dic in lis:
        names.append(get_name(dic))
    return names
