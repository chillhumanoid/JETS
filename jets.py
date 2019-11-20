import search as s, lister as l, merge as m    #inside imports
import rename as ren, login as log_in, database as db, util
from rename import rename as r; from download import download as dl
import click, configparser, os, sys
from menus import main as main_menu
from download import get_url                                            #outside imports
import time

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])                      #sets help to -h or --help

path = os.path.realpath(__file__)                                                #get current path
path = path.replace("jets.py","")                                                #replace script name with nothing
path = path + "Articles/"                                                        #get the article path
all_path = path + "All/"
author_path = path + "Author/"
merge_path = path + "Merged/"


@click.group(context_settings=CONTEXT_SETTINGS)                                  #officialy sets help to use -h or --help
@click.pass_context
def cli(ctx):
    """
    Start of CLI command handler, also runs the startup script

    Parameters:
    ctx (click ctx) : The ctx of the command
    """
    pass

@cli.command()
def curses():
    main_menu.start()
#LOGIN COMMAND
@cli.command()
@click.option('-u', 'user', required = True, metavar='<user>', nargs=1, help="Username for etsjets.org")
@click.option('-p', 'pwd', required = True, metavar='<pwd>', nargs=1, help="Password for etsjets.org")
def login(user, pwd):
    """
    Usage: jets login -u username -p password
    """
    log_in.set_login(user, pwd)


#SEARCH COMMAND
@cli.command()
@click.option('-t','title', default=False, metavar="<title>", help="Search by title", count=True)
@click.option('-a','author', default=False, metavar="<author>", help="Search by author", count=True)
@click.argument('term',metavar="<search_term>", nargs=-1)
def search(title, author, term):
    """
    Search by <author> or by <title>

    Usage: jets search (-t|-a) <search_term>
    """
    term = ' '.join(term)
    if author == 1 and title == 1 or author > 1 or title > 1:
        util.p("Only One Option Allowed")
    elif title == 1 or author == False:
        s.article_search(term)
    elif author == 1:
        s.auth_search(term)


#CHANGE COMMAND
@cli.command()
@click.option('-a', 'article', default=False, help="Change for specific article", count=True)
@click.option('-n', 'name', default=False, help="Change all articles with a given name", count=True)
@click.argument("term", metavar="<article_number>", nargs=-1, required=True)
def change(article, name, term):
    """
    Changes the name of a given article or the name of the author overall, when in doubt, go overall
    """
    if article == 1 and name == False:                                           #selected if -a was used, and not -n
        if len(term) == 1:                                                       #makes sure that article only has one argument
            term = term[0]
            numbers = util.get_numbers(term)                                     #gets a list in return
            full_number = numbers[0] + "." + numbers[1] + "." + numbers[2]       #sets full_number to that list. this may be counter intuitive, but
            r(full_number, False, True)                                          #r(ename) with full number, and that we're not changing title, but article
        else:
            util.p("Only one argument for article")
            sys.exit()
    if name == 1 and article == False:
        term = ' '.join(term)                                                     #join the full name
        ren.change(term)                                                          #change the name

#RENAME COMMAND
@cli.command()
@click.option('-t', 'title',default=False, help="Rename title", count=True)
@click.option('-b', 'both',default=False, help="Rename both title and author", count=True)
@click.argument("term", nargs=1, required=True)
def rename(title, author, both, term):
    """Rename title of article"""

    numbers = util.get_numbers(term)
    full_number = numbers[0] + "." + numbers[1] + "." + numbers[2]
    change_title = False
    change_author = False
    if title == 1:
        change_title = True
    if both == 1:
        change_title = True
        change_author = True
    r(full_number, change_title, change_author)


#LIST COMMAND
@cli.command()
@click.argument("term", nargs=1, required=False)
def list(term):
    """List all articles, or articles in a given volume or index

    Usage: jets list (optional) 1-62.1-4"""
    if term == None:
        l.start("0","0")
    else:
        numbers = util.get_numbers(term) #CAN BE 0 APPENDED
        volume_number,issue_number=[numbers[0], numbers[1]]
        l.start(volume_number, issue_number)

#INFO COMMAND
@cli.command()
@click.argument("term", nargs=1, required=True)
def info(term):
    """Show title and author for a given article

    Usage: jets info 1-62.1-4.articlenum"""
    numbers = util.get_numbers(term) #CAN BE 0 APPENDED
    full_number=numbers[0] + "." + numbers[1] + "." + numbers[2]
    articles = []
    for article in os.listdir(all_path):
        if article.startswith(full_number):
            articles.append(article)
    display(articles)

#REMOVE COMMAND
@cli.command("remove")
@click.argument("volume", nargs=1, required = True)
def remove(volume):
    util.check_vol(volume)
    db.remove_article_by_volume(volume)

#OPEN COMMAND
@cli.command("open")
@click.option("-a", 'author', default=False, help="Specify Author to Open", count=True)
@click.argument("term", nargs=1, required=False)
def opener(term, author):
    """Open the given article, or all articles by given author

    Usage: jets open 1-62.1-4.articlenum
         OR     jets open -a author"""
    if author == 1:
        o.open_author(term)
    elif author == False:
        numbers = util.get_numbers(term) #can be 0 appended
        volume_number = numbers[0]
        issue_number = numbers[1]
        article_number = numbers[2]
        if not volume_number == "0" and (issue_number == "0" and article_number == "0"):
            o.open_merged_file(volume_number, 0)
        if (not volume_number == "0" and not issue_number == "0") and article_number == "0":
            o.open_merged_file(volume_number, issue_number)
        if (not volume_number == "0" and not issue_number == "0" and not article_number == "0"):
            full_number = volume_number + "." + issue_number + "." + article_number

            o.open_file(full_number)
    else:
        util.p("Please enter an article number or author name")


#MERGE COMMAND
@cli.command()
@click.argument("term",nargs=1, required=True)
def merge(term):
    """Merge a full volume or a given issue.

    Merging volumes does also merge issues.

    Usage: jets merge 1-62.1-4"""
    if term.lower() == "all":
            m.merge_all()
    else:
        numbers = util.get_numbers(term) #can be 0 appended
        volume_number = numbers[0]
        issue_number = numbers[1]
        m.merge(volume_number, issue_number)

#DOWNLOAD COMMAND
@cli.command()
@click.option("-n", "new", default=False, help="Download all new/undownloaded articles", count=True)
@click.option("-v", "vol", default=0, type=int, help="Download from a specific volume")
@click.option("-i", "issue", default=0, type=int, help="Download from a specific issue")
@click.option("-a", "article", default=0, type=int, help="Download the specified article")
@click.option("-f", "force", default=False, help="Force redownload if problem with pdf", count=True)
@click.argument("term", nargs=1, required=False)
def download(new, vol, issue, article, term, force):
    """Downloads articles

       -n will download any articles not currently had
       -v will download all articles in a volume
       -i will download all articles in an issue (-v required)
       -a will download the given article in an issue (-v and -i required)

       Usage: jets -n|-v|-i|-a|1-62.1-4.articlenum"""
    if new >= 1:
        if force >= 1:
            util.p("-n can't be used with any other command")
            sys.exit()
    else:
        if vol == 0 and issue == 0 and article == 0:
            if not term == None:
                numbers = util.get_numbers(term, False) #CANT be 0 appended
                volume_number,issue_number,article_number=[numbers[0], numbers[1], numbers[2]]
        else:
            if not vol == 0 and issue == 0 and article == 0:
                util.check_vol(vol)
            if not issue == 0 and vol == 0:
                util.p("Please enter a volume number")
                sys.exit()
            if not article == 0 and issue == 0:
                util.p("Please enter an issue number")
                sys.exit()
            else:
                util.check_vol(vol)
                util.check_issue(issue)
            volume_number = str(vol)
            issue_number = str(issue)
            article_number = str(article)
    get_url.volume([volume_number, issue_number, article_number, force])

if __name__ == '__main__':
    cli()
