from jets_cli import search as searcher; from jets_cli import rename as r; from jets_cli import lister as l; from jets_cli import open as o
import click, configparser, os, sys
#import search as searcher
from jets_cli.util import p, start, getNumbers, check_vol, check_issue, check_digit, display_info as display; from jets_cli.rename import rename as r; from jets_cli.merge import merge as m
from jets_cli.downloader import start as dl
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

path = os.path.realpath(__file__)
path = path.replace("jets.py","")
path = path + "Articles/"

@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    pass

#SEARCH COMMAND
@cli.command()
@click.option('-t','title', default=False, help="Search by title", count=True)
@click.option('-a','author', default=False, help="Search by author", count=True)
@click.argument('term', nargs=-1)
def search(title, author, term):
    """Search by title or author

    Usage: jets search -t|-a TERM"""
    term = ' '.join(term)
    if author == 1 and title == 1 or author > 1 or title > 1:
        p("Only One Option Allowed")
    elif title == 1 or author == False:
        searcher.articleSearch(term)
    elif author == 1:
        searcher.authSearch(term)


#RENAME COMMAND
@cli.command()
@click.option('-t', 'title',default=False, help="Rename title", count=True)
@click.option('-a', 'author',default=False, help="Rename author", count=True)
@click.option('-b', 'both',default=False, help="Rename both title and author", count=True)
@click.argument("term", nargs=1, required=True)
def rename(title, author, both, term):
    """Rename title/author/both of article

    Usage: jets rename -t|-a|-b 1-62.1-4.articlenum"""
    num = getNumbers(term)
    vNum,iNum,aNum=[num[0], num[1], num[2]]
    id = 0
    if title == 1:
        id = id + 2
    if author == 1:
        id = id + 1
    r(vNum, iNum, aNum, id)

#LIST COMMAND
@cli.command()
@click.argument("term", nargs=1, required=False)
def list(term):
    """List all articles, or articles in a given volume or index

    Usage: jets list (optional) 1-62.1-4"""
    if term == None:
        l.listing("0","0")
    else:
        num = getNumbers(term)
        vNum,iNum=[num[0], num[1]]
        l.listing(vNum, iNum)


#INFO COMMAND
@cli.command()
@click.argument("term", nargs=1, required=True)
def info(term):
    """Show title and author for a given article

    Usage: jets info 1-62.1-4.articlenum"""
    num = getNumbers(term)
    vNum,iNum,aNum=[num[0], num[1], num[2]]
    articles = []
    for article in os.listdir(path + "All/"):
        if article.startswith(vNum + "." + iNum + "." + aNum):
            articles.append(article)
    display(articles)

#OPEN COMMAND
@cli.command("open")
@click.option("-a", 'author', default=False, help="Specify Author to Open", count=True)
@click.argument("term", nargs=1, required=False)
def opener(term, author):
    """Open the given article, or all articles by given author

    Usage: jets open 1-62.1-4.articlenum
         OR     jets open -a author"""
    if author == 1:
        o.openAuth(term)
    elif author == False:
        num = getNumbers(term)
        fNum = num[0] + "." + num[1] + "." + num[2]
        o.openFile(fNum)
    else:
        p("Please enter an article number or author name")


#MERGE COMMAND
@cli.command()
@click.argument("term",nargs=1, required=True)
def merge(term):
    """Merge a full volume or a given issue.

    Merging volumes does also merge issues.

    Usage: jets merge 1-62.1-4"""

    num = getNumbers(term)
    vNum = num[0]
    iNum = num[1]
    m(vNum, iNum)

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
    vNum = aNum = iNum = "0"
    if new >= 1:
        if force >= 1:
            p("-n can't be used with any other command")
            sys.exit()
    else:
        if vol == 0 and issue == 0 and article == 0:
            if term == None:
                p("Please enter an article number")
                sys.exit()
            else:
                num = getNumbers(term)
                vNum,iNum,aNum=[num[0], num[1], num[2]]
        else:
            if not vol == 0 and issue == 0 and article == 0:
                check_vol(vol)
            if not issue == 0 and vol == 0:
                p("Please enter a volume number")
                sys.exit()
            if not article == 0 and issue == 0:
                p("Please enter an issue number")
                sys.exit()
            else:
                check_vol(vol)
                check_issue(issue)
            vNum = str(vol)
            iNum = str(issue)
            aNum = str(article)
    dl(vNum, iNum, aNum, force)
