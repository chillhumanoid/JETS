import sys, os, time, subprocess
from pathvalidate import ValidationError, validate_filename; from PyPDF2 import PdfFileReader, PdfFileWriter; from shutil import copyfile

base = "C:/Users/jonat/OneDrive/Documents/JETS/"

def argGet(): #for when called from cmdline

    if len(sys.argv) == 3:
        args = sys.argv[2] #get the arguments after -fr or -c

        if sys.argv[2].count(".") == 2:
            vNum = args.split(".")[0] #get volume number
            if int(vNum) >= 1 and int(vNum) <= 62:
                iNum = args.split(".")[1]
                if int(iNum) >= 1 and int(iNum) <= 4:
                    aNum = args.split(".")[2]
                    if sys.argv[1] == "-fr":
                        main(vNum, iNum, aNum)
                        confirm(vNum, iNum, aNum)
                    elif sys.argv[1] == "-c":
                        confirm(vNum, iNum, aNum)
                    elif sys.argv[1] == "-fa":
                        authOnly(vNum, iNum, aNum)
                        confirm(vNum, iNum, aNum)
                else:
                    print()
                    print("Invalid issue number")
                    print("Correct Usage: jets -fr (1-62).(1-4).##")
            else:
                print()
                print("Invalid volume number")
                print("Correct Usage: jets -fr (1-62).(1-4).##")
        else:
            print()
            print("Incorrect argument")
            print("Correct Usage: jets -fr (1-62).(1-4).##")

    else:
        print()
        print("Need an argument")
        print("Correct Usage: jets -fr (1-62).(1-4).##")
        
def main(vNum, iNum, aNum): #had to adjust this because of fixAuthor
    vNum = str(vNum)
    iNum = str(iNum)
    aNum = str(aNum)

    for vol in os.listdir(base): #list everything in volume directory(root)

        if "Vol " + vNum + " " in vol: #get into the right volume folder
            path = base + vol + "/"  #set the path

            for issue in os.listdir(path): #run through the specific volume folder
                if os.path.isdir(path + issue):
                    if vNum + "." + iNum in issue: #find the right issue folder
                        nPath = path + issue +"/" #set the new path

                        for article in os.listdir(nPath): #run through the specific issue folder

                            if article.startswith(aNum + ") - "): #find the correct article
                                os.startfile(nPath + article) #open file (for readers sake)

                                title = "" #not sure if necessassy, but just in case
                                author = "" #see above

                                with open(nPath + article, 'rb') as f: #open the right article as "f"
                                    pdf = PdfFileReader(f)
                                    information = pdf.getDocumentInfo() #gets metadata
                                    title = information.title #gets the title
                                    author = information.author #gets the author
                                    f.close() #closes file

                                if not title == None: #if the file has a title
                                    title = title.strip() #get rid of any whitespace
                                else:
                                    title = "" #if it doesn't have a title set it to "" because otherwise error
                                if author == None: #if the article doesn't have an author, set it to "" because otehrwise error
                                    author = ""
                                
                                print() #blank prints always for formatting
                                print("Current title: ") 
                                print(title) #display current title
                                print()
                                name = input("Enter New Article Title: ") #gets new article title

                                print()
                                print("Current author: ") 
                                print(author) #displays current author
                                print()
                                nAuth = input("Enter New Author Name: ") #gets new author name
                                print()

                                print()
                                print("OLD TITLE: " + title) #display old title
                                print()
                                print("OLD AUTHOR: " + author) #display old author
                                print()

                                print("NEW TITLE: " + name) #display new title
                                print()
                                print("NEW AUTHOR: " + nAuth) #display new author
                                print()
                                choice = input("Confirm change(y/n): ") #confirm
                                
                                if choice == "y":
                                    nArticle = article.replace(article, aNum + ") - " + name + " .pdf")
                                    output = "OUT " + nArticle #works as a failsafe, after confirming, use jets -fo to fix outs

                                    with open(nPath + article, 'rb') as f: #open file again
                                        pdf = PdfFileReader(f)
                                        writer = PdfFileWriter() #open pdfwriter

                                        for page in range(pdf.getNumPages()): #get the pages
                                            writer.addPage(pdf.getPage(page)) #move them

                                        writer.addMetadata({ #add metadata
                                            '/Author': nAuth,
                                            '/Title': name
                                        })

                                        output = output.strip() #strip output just in case

                                        fout = open(nPath + output, 'ab') #open the output file

                                        writer.write(fout) #write the new pdf to the output

                                        fout.close()
                                        f.close()
                                else:
                                    x = 1

def authOnly(vNum, iNum, aNum):
    for vol in os.listdir(base):
        if "Vol " +  vNum + " " in vol:
            path = base + vol + "/"
            for issue in os.listdir(path):
                if os.path.isdir(issue + path):
                    if vNum + "." + iNum in issue:
                        nPath = path + issue + "/"
                        for article in os.listdir(nPath):
                            if article.startswith(aNum + ") - "):
                                acrobatPath = r'C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat\Acrobat.exe'
                                p = subprocess.Popen("%s %s" % (acrobatPath, nPath + article))
                                os.startfile(nPath + article)
                                f = open(nPath + article, 'rb')
                                pdf = PdfFileReader(f)
                                info = pdf.getDocumentInfo()
                                title = info.title
                                author = info.author
                                writer = PdfFileWriter()
                                for page in range(pdf.getNumPages()):
                                    writer.addPage(pdf.getPage(page))

                                print("Title - " + title)
                                nAuth = input("New Author Name: ")
                                print()
                                print("Old Author - " + author)
                                print("New Author - " + nAuth)
                                choice = input("Confirm(y/n): ")
                                choice = choice.lower()
                                if choice == "y":
                                    p.kill()
                                    time.sleep(.5)
                                    writer.addMetadata({
                                        '/Author': nAuth,
                                        '/Title': title
                                    })
                                    fout = open(nPath + article, 'ab')
                                    writer.write(fout)
                                    fout.close()
                                    f.close()
                                    fNum = vNum + "." + iNum + "." + aNum
                                    aName = article.replace(aNum + ") - ", fNum + " - ")
                                    aBase1 = base + "Authors/"
                                    aBase2 = base + "All/"
                                    #the following deletes the file from the author folder
                                    if os.path.exists(aBase1 + nAuth + "/"):
                                        for file in os.listdir(aBase1 + author + "/"):
                                            if file.startswith(fNum):
                                                os.remove(aBase1 + author + "/" + file)
                                                if not os.path.exists(aBase1 + nAuth + "/"):
                                                    os.mkdir(aBase1 + nAuth + "/")
                                                copyfile(nPath + article, aBase1 + nAuth  + "/" + aName)
                                    else:
                                        if not os.path.exists(aBase1 + nAuth + "/"):
                                            os.mkdir(aBase1 + nAuth + "/")
                                        copyfile(nPath + article, aBase1 + nAuth + "/" + aName)
                                    #the following deletes the existing file from the all folder
                                    for file in os.listdir(aBase2):
                                        if file.startswith(fNum):
                                            os.remove(aBase2 + file)
                                            copyfile(nPath + article, aBase2 + aName)
                                else:
                                    p.kill()
def confirm(vNum, iNum, aNum): #displays author and title of new PDF (or given pdf, see below)
    for vol in os.listdir(base):
        if "Vol " + vNum + " " in vol:
            path = base + vol + "/"
            for issue in os.listdir(path):
                if os.path.isdir(path + issue):
                    if vNum + "." + iNum in issue:
                        nPath = path + issue +"/"
                        for article in os.listdir(nPath):
                            if article.startswith("OUT " + aNum + ") - ") or article.startswith(aNum + ") - "):
                                wPath = nPath + article
                                with open(wPath, 'rb') as f:
                                    pdf = PdfFileReader(f)
                                    info = pdf.getDocumentInfo()
                                    title = info.title
                                    author = info.author
                                    f.close()
                                print()
                                print("Article " + vNum + "." + iNum + "." + aNum)
                                if author == None:
                                    author = ""
                                print("Author: " + author)
                                if title == None:
                                    title = ""
                                print("Title: " + title)
                            
def conf(num):
    vNum = num.split(".")[0]
    iNum = num.split(".")[1]
    aNum = num.split(".")[2]
    for vol in os.listdir(base):
        if "Vol " + vNum in vol:
            path = base + vol + "/"
            for issue in os.listdir(path):
                if os.path.isdir(path + issue):
                    if vNum + "." + iNum in issue:
                        nPath = path + issue + "/"
                        for article in os.listdir(nPath):
                            if article.startswith(aNum + ") - "):
                                wPath = nPath + article
                                with open(wPath, 'rb') as f:
                                    pdf = PdfFileReader(f)
                                    info = pdf.getDocumentInfo()
                                    title = info.title
                                    author = info.author
                                    f.close()
                                if author == None:
                                    author = ""
                                    print(num)
                                print("Author: " + author)
                                if title == None:
                                    title = ""
                                    print(num)
                                print("Title: " + title)
                                print()
                            
