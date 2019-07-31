import sys

def help():
    if len(sys.argv) == 2:
        print()
        print("JETS Command Line Tool Made by Jonathan Thorne")
        print("Commands: ")
        print("    -l                      Without arguments, prints all volumes")
        print("    -l -v (1-62)            prints all issues in a given volume folder")
        print("    -l -v (1-62) -i (1-4)   prints all articles in given volume/issue folder")
