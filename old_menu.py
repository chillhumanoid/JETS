def menu(current):
    global curDirectory
    if current == "C:/Users/jonat/OneDrive/Documents/Jets/":
        current = "Root"
    choice = choice.lower()
    if "list" == choice:
        check = curDirectory.count("/")
        if current == "Root":
            printVol()
        if check == 7:
            printIssue(current)
        if check == 8:
            printArticles(current)
    if "select " in choice:
        check = curDirectory.count("/")
        num = choice.split(" ")[1]
        temp = num.count(".")
        if current == "Root":
            if temp == 0:
                selectVol(num)
            if temp == 1:
                selectVolAndIssue(num)
            if temp == 2:
                selectFull(num, current)
            else:
                print("INVALID")
                menu(curDirectory)
        elif check == 7:
            if temp == 0:
                selectIssue(num, current)
            elif temp == 1:
                selectIssueAndArticle(num, current)
            elif temp == 2:
                selectFull(num, current)
            else:
                print("INVALID")
                menu(current)
        elif check == 8:
            if temp == 0:
                selectArticles(num, current)
            if temp == 1:
                selectIssueAndArticle(num)
            if temp == 2:
                selectFull(num, current)
        else:
            print("WHAT")
    elif "root" == choice:
        curDirectory = base
        clear()
        menu(curDirectory)
    elif "back" == choice:
        check = curDirectory.count("/")
        if check == 7:
            curDirectory = base
            clear()
            menu(curDirectory)
        elif check == 8 and curDirectory.endswith("/"):
            temp = curDirectory.split(")/")[0]
            temp = temp + ")/"
            curDirectory = temp
            current = curDirectory.split("Vol ")[1]
            current = current[:-1]
            current = "Vol " + current
            clear()
            menu(current)
        elif curDirectory.endswith(".pdf"):
            start = curDirectory.find(")/")+2
            end = curDirectory.find("/", start)
            curDirectory = curDirectory[:end] + "/"
            current = curDirectory.split("Vol ")[1]
            current = "Vol " + current
            current = current[:-1]
            clear()
            menu(current)
    elif "search" in choice:
        arg = choice.split(" ", 2)[1]
        term = choice.split(" ")[2]
        if arg == "-a":
            authorSearch()
        if arg == "-i":
            localHelp.search(term, curDirectory)
    elif "print" in choice:
        if " - " in current:
            choice = current.split(" - ")[0]
        else:
            choice = choice.split(" ")[1]
        printHandle(choice, current)
    elif "help print" in choice:
        print("Make sure you only input volume number(xx), issue number(yy) and article number (zz)")
        print("\n xx.yy.zz")
        print("\n no leading 0's are needed")
        print("")
        clear()
        menu()
    
def printFile(path):
    os.startfile(path, "print")
def printHandle(potential, current):
    x = potential.count(".")
    if x == 2:
        nums = potential.split(".")
        vNum = nums[0]
        iNum = nums[1]
        aNum = nums[2]
        for folder in os.listdir(base):
            if "Vol " + vNum + " " in folder:
                nPath = base + folder + "/"
                for issue in os.listdir(nPath):
                    check = vNum + "." + iNum
                    check2 = issue.split(" ")[1]
                    if check in issue:
                        print(issue)
                        nnPath = nPath + issue + "/"
                        for article in os.listdir(nnPath):
                            num = article.split(")", 1)[0]
                            if aNum == num:
                                title = article.split(") - ")[1]
                                choice = input("Print " + potential + " - " + title + "? (Y/N): ")
                                choice = choice.lower()
                                if choice == "y":
                                    fPath = nnPath + article
                                    print(fPath)
                                    if os.path.exists(fPath):
                                        os.startfile(fPath, 'print')
                                    menu(current)
                                else:
                                    menu(current)
    else:
        print()
        print("Sorry, that's not the correct argument. \n\nType Help print for more info")
        print()
        menu(current)
