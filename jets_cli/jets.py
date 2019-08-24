import search as s, lister as l, open as o, merge as m, util, downloader as dl, rename as ren, login as log_in
import time #DEV IMPORTS
from rename import rename as r; from display import display
import click, configparser, os, sys

#import search as searcher
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

path = os.path.realpath(__file__)
path = path.replace("jets.py","")
path = path + "Articles/"
all_path = path + "All/"
author_path = path + "Author/"
merge_path = path + "Merged/"


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    util.start()
    pass

#LOGIN COMMAND

@cli.command()
@click.option('-u', 'user', required = True, nargs=1)
@click.option('-p', 'pwd', required = True, nargs=1)
def login(user, pwd):
    log_in.set_login(user, pwd)


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
        util.p("Only One Option Allowed")
    elif title == 1 or author == False:
        s.article_search(term)
    elif author == 1:
        s.auth_search(term)

#CHANGE COMMAND
@cli.command()
@click.option('-a', 'article', default=False, help="Change for specific article", count=True)
@click.option('-n', 'name', default=False, help="Change all articles with a given name", count=True)
@click.argument("term", nargs=-1, required=True)
def change(article, name, term):
    if article == 1 and name == False:
        if len(term) == 1:
            term = term[0]
            numbers = util.get_numbers(term)
            full_number = numbers[0] + "." + numbers[1] + "." + numbers[2]
            r(full_number, False, True)
        else:
            util.p("Only one argument for article")
            sys.exit()
    if name == 1 and article == False:
        term = ' '.join(term)
        ren.change(term)

#RENAME COMMAND
@cli.command()
@click.option('-t', 'title',default=False, help="Rename title", count=True)
@click.option('-b', 'both',default=False, help="Rename both title and author", count=True)
@click.argument("term", nargs=1, required=True)
def rename(title, author, both, term):
    """Rename title/author/both of article

    Usage: jets rename -t|-a|-b 1-62.1-4.articlenum"""
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
        full_number = numbers[0] + "." + numbers[1] + "." + numbers[2]
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
    dl.get_volume_url([volume_number, issue_number, article_number, force])
if __name__ == '__main__':
    util.start()
    cli()
