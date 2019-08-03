import sys

def help():
    if len(sys.argv) == 2:
        print()
        print("JETS Command Line Tool Made by Jonathan Thorne")
        print("Commands: ")
        print("      -l                    Prints all articles in all volumes")
        print("      -l (1-62)             Prints all articles in given volume")
        print("      -l (1-62).(1-4)       Prints all articles in given volume and issue")
        print("      -f (1-64)             Fixes the author info on all articles in given volume")
        print("      -f (1-64).(1-4)       Fixes the author info on all articles in given issue")
        print("      -fr (1-64).(1-4).##   Where ## is the article number, allows user to rename the file manually")
        print()
    elif len(sys.argv) == 3:
        arg = sys.argv[2]
        if arg == "-l":
            print()
            print("List Command")
            print()
            print("Description: Lists all articles, or all articles in a volume or issue")
            print()
            print("Usage:")
            print("      -l                    Prints all articles in all volumes")
            print("      -l (1-62)             Prints all articles in given volume")
            print("      -l (1-62).(1-4)       Prints all articles in given volume and issue")
        elif arg == "-s":
            print()
            print("Search Command")
            print()
            print("Description: Search by title or author")
            print()
            print("Usage:")
            print("Coming soon")
        elif arg == "-f":
            print()
            print("Fix Author Command")
            print()
            print("Description: Goes through a set volume or issue and fixes the author information")
            print("             on all the articles. May not be necessary anymore")
            print()
            print("Usage:")
            print("      -f (1-64)             Fixes the author info on all articles in given volume")
            print("      -f (1-64).(1-4)       Fixes the author info on all articles in given issue")
        elif arg == "-fr":
            print()
            print("Force Rename Command")
            print()
            print("Description: Force a title and author rename of a given article")
            print()
            print("Usage:")
            print("      -fr (1-64).(1-4).##   Where ## is the article number, allows user to rename the file manually") 
        elif arg == "-c":
            #confirm a given thing
            x = 1
        elif arg == "-fo":
            #fix out
            x = 1
        elif arg == "-ca":
            #..something author
            x = 1
        elif arg == "-o":
            #opener
            x = 1
            
