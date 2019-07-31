#import statements

import os
import sys

#global variables

base = "C:/Users/jonat/OneDrive/Documents/JETS/"

#functions

def article():    #for searching articles

    if len(sys.argv) < 4:    #If under 4, no search term given
        print()   #for formatting
        print("Please enter a search term.")

    else:
        print() #for formatting
        x = 0   #used in loop iterations
        term = sys.argv[3] #search term starts at point 3

        if len(sys.argv) == 4:  #if the length is 4 exactly

            for folder in os.listdir(base):  #goes through all folders in base

                if "Vol " in folder: #makes sure volume folder(avoids author and all folder)
                    path = base + folder + "/" #adjusts path

                    for issue in os.listdir(path): #goes through all issue folders in each volume
                        nPath = path + issue + "/" #adjusts path, this is nPath because if path, breaks loop

                        for file in os.listdir(nPath):  # checks every file in every issue folder
                            term = term.lower()   #lower for checking purposes
                            f = file.lower() #see above

                            if term in f:    #if term is found
                                aNum = file.split(")")[0] #gets the article number
                                title = file.split(") - ")[1] #gets the title
                                vNum = folder.split(" ")[1] #gets the volume number
                                iNum = issue.split(".")[1] #gets the issue number, technically could just use this for both vnum and inum
                                x = x + 1 #adds 1 to x, lets script know that an article was found (but doesn't end loop)
                                print(vNum + "." + iNum + "." + aNum + " - " + title) #display name of article

            if x == 0: #if, at end of loop, no article was found, let user know
                print()
                print("No Articles Found")
                
        elif len(sys.argv) > 4: # > 4 means more than one word in search term
            for x in range(4,len(sys.argv)):   #get each word in search term (but throw out rest of command)
                term = term + " " + sys.argv[x] #make one search term
            terms = term.split(" ") #Technically redudant, but im lazy

            for folder in os.listdir(base): #see above, it functions in practically the same way
                if "Vol " in folder:
                    path = base + folder + "/"
                    for issue in os.listdir(path):
                        nPath = path + issue + "/"
                        for file in os.listdir(nPath):
                            term = term.lower()
                            f = file.lower()
                            if term in f:
                                aNum = file.split(")")[0]
                                title = file.split(") - ")[1]
                                vNum = folder.split(" ")[1]
                                iNum = issue.split(".")[1]
                                x = x + 1
                                print(vNum + "." + iNum + "." + aNum + " - " + title)

                                #These are separated to allow for if search term was found with the full term, not to look at each individual word. If I had to guess, may never see the second part. Oh well.

            if x == 0: #if article with search term not found yet
                for folder in os.listdir(base): #try again with individual words in term, functions otherwise same as previous two, see first set of comments
                    if "Vol " in folder:
                        path = base + folder + "/"
                        for issue in os.listdir(path):
                            nPath = path + issue + "/"
                            for file in os.listdir(nPath):
                                found = []
                                f = file.lower()
                                for y in terms:   #gets each individual word in the search term
                                    y = y.lower() #lowers for checking purposes, as above
                                    if y == "the" or y == "of" or y == "a" or y == "and" or y == "or" or y == "if" or y == "&" or y == "is" or y == "on": #ignores major key words, otherwise everything would be displayed
                                        kl = 0 #does nothing, but makes the if statement work
                                    elif y in f: 
                                        aNum = file.split(")")[0]
                                        title = file.split(") - ")[1]
                                        vNum = folder.split(" ")[1]
                                        iNum = issue.split(".")[1]
                                        x = x + 1
                                        d = vNum + "." + iNum + "." + aNum + " - " + title #instead of printing out immediately, adds to function
                                        if not d in found:                                 #this allows for if the same article has two of the keywords not together(it'd have been printed already in the above)
                                            found.append(d)                                #adds any articles not already added to a found list
                                if len(found) > 0:       #makes sure that found isn't empty, if it is, no need to print
                                    for t in found:     
                                        print(t)      #print all articles that were found with search terms
 
                if x == 0: #if at this point, using either the search term as a whole or individual words, no article was found, let user know
                    print()
                    print("No articles found")
