import requests, argparse, urllib.request, click, time, win32api, win32print, subprocess, re, time, sys, os #all python wide imports
import backend, issues, lister, merger,forceRename, search, opener, fixAuthor, helpcmd, fixOut, authFolder #all jets related imports
from clear_screen import clear #specific imports
from shutil import copyfile
from bs4 import BeautifulSoup
from pathvalidate import ValidationError, validate_filename

def main():
    length = len(sys.argv)
    if length == 1:
        print()
        print("For command help, use 'jets -h'")
    else:
        com = sys.argv[1]
        com = com.lower()
        if com == "-s": #search command
            start = time.time()
            search.main()
            end = time.time()
            print()
            total = end-start
            print("Time Taken: " + str(total))
        elif com == "-l": #lists based on arguments, see lister.py
            start = time.time()
            lister.main()
            end = time.time()
            print()
            total = end-start
            print("Time Taken: " + str(total))
        elif com == "-f": #fix author command
            start = time.time()
            fixAuthor.main() #i don't remember how this works, will look
            end = time.time()
            total = end-start
            print()
            print("Time Taken: " + str(total))
        elif com == "-fr": #force rename command
            start = time.time()
            forceRename.argGet() #forces the rename of a specific file, user has to init.
            end = time.time()
            total = end - start
            print()
            print("Time Taken: " + str(total))
        elif com == "-c": #confirm that the title and author are there
            start = time.time()
            forceRename.argGet()
            end = time.time()
            total = end - start
            print()
            print("Time Taken: " + str(total))
        elif com == "-fo": #fix out
            start = time.time()
            fixOut.main()
            end = time.time()
            total = end-start
            print()
            print("Time Taken: " + str(total))

        elif com == "-ca": #create author folder
            start = time.time()
            authFolder.main()
            end = time.time()
            total = end - start
            print()
            print("Time Taken: " + str(total))
        elif com == "-o": #opener
            start = time.time()
            opener.getArgs()
            end = time.time()
            total = end - start
            print()
            print("Time Taken: " + str(total))
        elif com == "-fa":
            start = time.time()
            forceRename.argGet() #force author only rename fl coming soon
            end = time.time()
            total = end - start
            print()
            print("Time Taken: " + str(total))
        elif com == "-m": #merge
            start = time.time()
            merger.main()
            end = time.time()
            total = end - start
            print()
            print("Time Taken: " + str(total))
        elif com == "-h": #help command
            helpcmd.help()

if __name__ == '__main__':
    main()
base = "C:/Users/jonat/OneDrive/Documents/Jets/" #currently unused
curDirectory = "C:/Users/jonat/OneDrive/Documents/Jets/" #currently unused
