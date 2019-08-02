import requests, urllib.request, time, win32api, win32print, subprocess, re, sys, os #all python wide imports
import backend, issues, lister, forceRename, search, fixAuthor, helpcmd #all jets related imports
from clear_screen import clear #specific imports
from shutil import copyfile
from bs4 import BeautifulSoup
from pathvalidate import ValidationError, validate_filename


def main_test():
    global curDirectory
    length = len(sys.argv)
    if length == 1:
        print()
        print("For command help, use 'jets -h'")
    else:
        com = sys.argv[1]
        com = com.lower()
    #length = len(sys.argv)
        if com == "-s":
            if length < 3:
                print("Insufficient arguments")
            else:
                term1 = sys.argv[2]
                if term1 == "-a":
                    print("FUTURE SEARCH AUTHOR TRY AGAIN LATER")
                elif term1 == "-t":
                    search.article()
                else:
                    print("ERROR: unknown command")
        elif com == "-l":
            lister.main()
        elif com == "-f":
            fixAuthor.main()
        elif com == "-fr":
            forceRename.main()
        elif com == "-c":
            forceRename.confirm()
        elif com == "-h":
            helpcmd.help()
    

base = "C:/Users/jonat/OneDrive/Documents/Jets/"        
curDirectory = "C:/Users/jonat/OneDrive/Documents/Jets/"
main_test()
#menu(curDirectory)
