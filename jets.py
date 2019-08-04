import requests, urllib.request, time, win32api, win32print, subprocess, re, sys, os #all python wide imports
import backend, issues, lister, merger,forceRename, search, opener, fixAuthor, helpcmd, fixOut, authFolder #all jets related imports
from clear_screen import clear #specific imports
from shutil import copyfile
from bs4 import BeautifulSoup
from pathvalidate import ValidationError, validate_filename


def main():
    global curDirectory
    length = len(sys.argv)
    if length == 1:
        print()
        print("For command help, use 'jets -h'")
    else:
        com = sys.argv[1]
        com = com.lower()
        if com == "-s": #search command
            search.main()
        elif com == "-l": #lists based on arguments, see lister.py
            lister.main()
        elif com == "-f": #fix author command
            fixAuthor.main() #i don't remember how this works, will look
        elif com == "-fr": #force rename command
            forceRename.argGet() #forces the rename of a specific file, user has to init.
        elif com == "-c": #confirm that the title and author are there
            forceRename.argGet()
        elif com == "-fo":
            fixOut.main()
        elif com == "-ca":
            authFolder.main()
        elif com == "-o":
            opener.getArgs()
        elif com == "-fa":
            forceRename.argGet()
        elif com == "-m":
            merger.main()
        elif com == "-h": #help command
            helpcmd.help()
    

base = "C:/Users/jonat/OneDrive/Documents/Jets/" #currently unused       
curDirectory = "C:/Users/jonat/OneDrive/Documents/Jets/" #currently unused
main() #calls main()
#menu(curDirectory) remnant from old menu, see old_menu.py
