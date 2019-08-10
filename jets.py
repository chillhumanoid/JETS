import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

def p(msg):
    click.echo()
    click.echo(msg)

@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    pass


#This is the search command

@cli.command()
@click.option('-t','title', default=False, help="Search by title")
@click.option('-a','author', default=False, help="Search by author")
@click.argument('term', nargs=-1)
def search(title, author, term):
    """Search by title or author

    Usage: jets search -t|-a TERM"""
    if len(term) == 0:
        term = ""
    else:
        term = ' '.join(term)
    if (author and title) or title == '-a' or author == '-t':
        p("Only One Option Allowed")
    elif title:
        term = title + " " + term
        p("Title: " + term)
    elif author:
        term = author + " " + term
        p("Author: " + term)
    else:
        p("Title: " + term)

#this is the rename command

@cli.command()
@click.option('-t', 'title',default=False, help="Rename title")
@click.option('-a', 'author',default=False, help="Rename author")
@click.option('-b', 'both',default=False, help="Rename both title and author")
@click.argument('term', nargs=-1)
def rename(title, author, both, term):
    """Rename title/author/both of article

    Usage: jets rename -t|-a|-b 1-62.1-4.articlenum"""
    if len(term) == 0:
        term = ""
    else:
        term = ' '.join(term)
    if (title and both) or (title and author) or (both and author) or (title and author and both):
        p("Only One Option Allowed")
    elif title == '-a' or title == '-b' or author == '-t' or author == '-b' or both == '-a' or both == '-t':
        p("Only One Option Allowed")
    elif title:
        p("Rename Title Only")
    elif author:
        p("Rename Author Only")
    elif both:
        p("Rename Title & Author")
    else:
        p("Rename Title & Author")

#this is the list Command
@cli.command()
@click.argument("term", nargs=1, required=False)
def list(term):
    """List all articles, or articles in a given volume or index

    Usage: jets list (optional) 1-62.1-4"""
    if term == None:
        p("List All")
    else:
        p("List Some")

@cli.command()
@click.argument("term", nargs=1, required=True)
def fixauth(term):
    """Fix author names in a given folder (Defunct?)"""
    p("Fix Author")

@cli.command()
@click.argument("term", nargs=1, required=True)
def info(term):
    """Show title and author for a given article

    Usage: jets info 1-62.1-4.articlenum"""
    p("Show info")

@cli.command()
@click.option("-a", 'author', default=False, help="Search by author name")
@click.argument("term", nargs=1, required=False)
def open(term, author):
    """Open the given article, or all articles by given author

    Usage: jets open 1-62.1-4.articlenum
         OR     jets open -a author"""
    if author:
        if not term == None:
            author = author + " " + term
        p("Open all by " + author)
    elif term == None:
        p("Please enter an article number")
    else:
        p("Open " + term)

@cli.command()
@click.argument("term", nargs=1, required=True)
def merge(term):
    """Merge a full volume or a given issue.

    Merging volumes does also merge issues.

    Usage: jets merge 1-62.1-4"""


    p("Merge")
#init
if __name__ == '__main__':
    cli()
