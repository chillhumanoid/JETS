import os, sys

known_authors = ["Jerome Ficek", "Ronald Youngblood", "Cleon Rogers", "Robert L Saucy", "Alan Johnson", "Lewis Foster", "Phillip H. Wiebe", "William Lane Craig" "Edwin Yamauchi","Paul Frederick Feiler", "Paul Feiler", "Martin H. Woudstra", "Philip Barton Payne", "George Allen Turner", "Vern Sheridan Poythress", "Gleason L. Archer", "Gordon Clark", "Wilbur B. Wallis", "Andrew Helmbold", "Vernon Grounds", "Robert Longenecker", "David Scaer", "John Warwick Montgomery", "George Eldon Ladd" "Craig Keener", "Samuel S. Schultz", "Charles Horne"]

def change_known_authors(name):
    if is_known_author(name):
        name = name.replace("Jerome Ficek", "Jerome L. Ficek")
        name = name.replace("Craig Keener", "Craig S. Keener")
        name = name.replace("Samuel S. Schultz", "Samuel J. Schultz")
        name = name.replace("Charles Horne", "Charles M. Horne")
        name = name.replace("Charles M. Home", "Charles M. Horne")
        name = name.replace("George Eldon Ladd", "George E. Ladd")
        name = name.replace("John Warwick Montgomery", "John W. Montgomery")
        name = name.replace("Robert Longenecker", "Robert N. Longenecker")
        name = name.replace("David Scaer", "David P. Scaer")
        name = name.replace("Vernon Grounds", "Vernon C. Grounds")
        name = name.replace("Andrew Helmbold", "Andrew K. Helmbold")
        name = name.replace("Wilbur B. Wallis", "Wilber B. Wallis")
        name = name.replace("Gordon Clark", "Gordon H. Clark")
        name = name.replace("Gleason L. Archer", "G. L. Archer")
        name = name.replace("Vern Sheridan Poythress", "Vern S. Poythress")
        name = name.replace("George Allen Turner", "George A. Turner")
        name = name.replace("Philip Barton Payne", "Philip B. Payne")
        name = name.replace("Martin H. Woudstra", "Marten H. Woudstra")
        name = name.replace("Edwin Yamauchi", "Edwin M. Yamauchi")
        name = name.replace("Paul Frederick Feiler", "Paul F. Feiler")
        name = name.replace("Paul Feiler", "Paul F. Feiler")
        name = name.replace("Phillip H. Wiebe", "P. H. Wiebe")
        name = name.replace("William Lane Craig", "William L. Craig")
        name = name.replace("Lewis Foster", "Lewis A. Foster")
        name = name.replace("Alan Johnson", "Alan F. Johnson")
        name = name.replace("Robert L Saucy", "Robert L. Saucy")
        name = name.replace("Cleon Rogers", "Cleon L. Rogers, Jr")
        name = name.replace("Ronald Youngblood", "Ronald F. Youngblood")
    return name

def is_known_author(name):
    if name in known_authors:
        return True
    else:
        return False