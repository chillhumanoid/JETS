#this is the file for parsing title, filenumber or author name from a raw file title or the post-change file.
import util

def get_full_number(file_name):
    full_num = None #if no num, which would be error
    if " - " in file_name: #this indicates file number is on file name
        full_num = file_name.split(" - ")[0] #get the file number
    return full_num

def get_raw_author(raw_file_name, count, title):
    if count == 0:
        author = "JETS" #if no author given, author name is JETS always.
    else:
        author = title.split(". . .")[count] #get the author
        if ", Jr" in author: #replace this weird jr denoter
            author = author.replace(", Jr", " Jr")
        author = util.string_strip(author) #this keeps stripping author until no whitespace on either end
        author = author.replace("  ", " ") #get rid of double spaces.
        author = author.title()
        author = fix_titled_authors(author)
    return author

def get_raw_title(count, title):
    if not count == 0:
        if not count == 1:
            title = title.split(". . .")[:count]
        else:
            title = title.split(". . .")[0]
        title = ''.join(title)
    title = util.string_strip(title)
    title = title.title()
    title = fix_titled(title)
    return title

def get_file_name(file_name):
    file_name = file_name.replace('\n', ' ')
    file_name = file_name.replace(": ", " - ")
    file_name = file_name.replace(":", "_")
    file_name = file_name.replace("’", "'")
    file_name = file_name.replace("“", "'")
    file_name = file_name.replace("”", "'")
    file_name = file_name.replace('"', "'")
    file_name = file_name.replace("/", "-")
    file_name = util.string_strip(file_name)
    if file_name.endswith("?"):
        file_name = file_name[:-1]
    if file_name.endswith("?'"):
        file_name = file_name[:-2]
        file_name = file_name + "'"
    file_name = file_name.replace("?", ' -')
    file_name = file_name.title()
    file_name = fix_titled(file_name)
    return file_name

def get_authors(author):
    authors = []
    author = author.replace(" And ", " and ")
    if " and " in author:
        auths = author.split(" and ")
        for a in auths:
            if "," in a:
                authos = a.split(",")
                for auth in authos:
                    auth = auth.strip()
                    if not auth == "":
                        authors.append(auth)
            else:
                a = a.strip()
                a = a.strip() #just in case
                authors.append(a)
    else:
        authors.append(author)
    return authors

def fix_titled_authors(string):
    string = string.replace("Iii", "III")
    string = string.replace("Ii", "II")
    string = string.replace("Iv", "IV")
    string = string.replace("&Amp;", "And")
    string = string.replace("  ", " ")
    return string
    
def fix_titled(string):
    string = string.replace("Iii", "III")
    string = string.replace("Ii", "II")
    string = string.replace("Iv", "IV")
    string = string.replace("Ot", "OT")
    string = string.replace("Nt", "NT")
    string = string.replace("'S", "'s")
    string = string.replace("’S", "’s")
    string = string.replace("Bc", "BC")
    if string.endswith("Ad"):
        string = string[:-2]
        string = string + "AD"
    string = string.replace("Ad ", "AD ")
    string = string.replace("&Amp;", "And")
    string = string.replace("Mattter", "Matter")
    string = string.replace("  ", " ")
    return string
