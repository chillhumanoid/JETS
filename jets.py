import requests, urllib.request, time, win32api, win32print, subprocess, re, sys, os #all python wide imports
import backend, issues, lister, forceRename, search, fixAuthor, helpcmd #all jets related imports
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
            if length < 3:
                print("Insufficient arguments")
            else:
                term1 = sys.argv[2]
                if term1 == "-a": #may move this to search.py
                    print("FUTURE SEARCH AUTHOR TRY AGAIN LATER")
                elif term1 == "-t":
                    search.article()
                else:
                    print("ERROR: unknown command")
        elif com == "-l": #lists based on arguments, see lister.py
            lister.main()
        elif com == "-f": #fix author command
            fixAuthor.main() #i don't remember how this works, will look
        elif com == "-fr": #force rename command
            forceRename.main1() #forces the rename of a specific file, user has to init.
        elif com == "-c": #confirm that the title and author are there
            forceRename.confirm()
        elif com == "-h": #help command
            helpcmd.help()
    

base = "C:/Users/jonat/OneDrive/Documents/Jets/" #currently unused       
curDirectory = "C:/Users/jonat/OneDrive/Documents/Jets/" #currently unused
main() #calls main()
#menu(curDirectory) remnant from old menu, see old_menu.py
