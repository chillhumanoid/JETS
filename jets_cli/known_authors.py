import os, sys


known_authors = ["Jerome Ficek", "Bruce Waltke", "James B. De Young", "Thomas Edward Mccomiskey", ". Robert L. Saucy", "Ronald Youngblood", 
                 "Cleon Rogers", "Robert L Saucy", "Alan Johnson", "Lewis Foster", "Phillip H. Wiebe", "William Lane Craig", "Edwin Yamauchi",
                 "Paul Frederick Feiler", "Paul Feiler", "Martin H. Woudstra", "Philip Barton Payne", "George Allen Turner", "Vern Sheridan Poythress",
                 "Gleason L. Archer", "Gordon Clark", "Wilbur B. Wallis", "Andrew Helmbold", "Vernon Grounds", "Robert Longenecker", "David Scaer", 
                 "John Warwick Montgomery", "George Eldon Ladd", "Craig Keener", "Samuel S. Schultz", "Charles Horne", "Allen A. Macrae",
                 "Robert Duncan Culver", "S. J. Schultz", "Daniel Fuller", "Clark Pinnock", "Eugene Merrill", "Aída Dina Besançon Spencer",
                 "Charles Horne", "Charles M. Home", "Bruce A Demarest", "Rovert V. Rakestraw", "Wayne Alan Detzler", "Larry L. Helyer", "Todd S Labute",
                 "Walt Russell", "Mark W. Chavalas", "Robertson Mcquilkin", "Ronald Bergey", "Gary Steven Shogren", "Ron Youngblood", "Homer Heater Jr", "David M. Howard Jr",
                 "Ernst Wendland", "Dave Mathewson", "Glen A. Scorgie", "Tim Wiarda", "Robert Yarbrough", "Joseph Hellerman", "Gregory K. Beale", "J.P. Moreland",
                 "Ken M. Campbell", "Tim Mcconnel", "Scot Mcknight With R. Boaz Johnson", "Joel Williams", "Ben L. Merkle", "Douglas Kennard", "James Alan Patterson",
                 "Herbert W. Bateman IV", "Elmer Martens", "Andreas Köstenberger", "Walter Kaiser", "David Huttar", "Bruce Ware", "Andrew Steinmann", "Robert Chisholm", 
                 "Mark Saucy", "Clint E. Arnold", "Walter C. Kaiser Jr", "Steven Cowan", "Paul Himes", "Paul House", "Paul Tanner", "Walter Schultz", "Greg Goswell", "John Frame",
                 "D.A. Carson", "Dane Ortlund", "Armin Baum", "John Walton", "Brent Sandy", "Brian Peterson", "Gary Yates", "Terrance R. Wardlaw", "Paul Maxwell", 
                 "Victor (Sung Yul) Rhee", "Klaus Issler", "Brian Neil Peterson", "Charles Cruise", "Sean Christensen", "Alexander Stewart", "Joseph Greene", 
                 "Andreas J. Kostenberger", "Michael Horton", "Brian Neil Paterson"]

def change_known_authors(name):
    if is_known_author(name):
        name = name.replace("Brian Neil Paterson", "Brian N. Peterson")
        name = name.replace("Michael Horton", "Michael S. Horton")
        name = name.replace("Andreas J. Kostenberger", "Andreas J. Köstenberger")
        name = name.replace("Joseph Greene", "Joseph R. Greene")
        name = name.replace("Alexander Stewart", "Alexander E. Stewart")
        name = name.replace("Sean Christensen", "Sean M. Christensen")
        name = name.replace("Charles Cruise", "Charles E. Cruise")
        name = name.replace("Brian Neil Peterson", "Brian N. Peterson")
        name = name.replace("Klaus Issler", "Klaus D. Issler")
        name = name.replace("Victor (Sung Yul) Rhee", "Victor (Sung-Yul) Rhee")
        name = name.replace("Paul Maxwell", "Paul C. Maxwell")
        name = name.replace("Terrance R. Wardlaw", "Terrance R. Wardlaw Jr")
        name = name.replace("Gary Yates", "Gary E. Yates")
        name = name.replace("Brian Peterson", "Brian N. Peterson")
        name = name.replace("Brent Sandy", "D. Brent Sandy")
        name = name.replace("John Walton", "John H. Walton")
        name = name.replace("Armin Baum", "Armin D. Baum")
        name = name.replace("Dane Ortlund", "Dane C. Ortlund")
        name = name.replace("D.A. Carson", "D. A. Carson")
        name = name.replace("John Frame", "John M. Frame")
        name = name.replace("Greg Goswell", "Gregory Goswell")
        name = name.replace("Walter Schultz", "Walter J. Schultz")
        name = name.replace("Paul Tanner", "J. Paul Tanner")
        name = name.replace("Paul House", "Paul R. House")
        name = name.replace("Paul Himes", "Paul A. Himes")
        name = name.replace("Steven Cowan", "Steven B. Cowan")
        name = name.replace("Walter C. Kaiser Jr","Walter C. Kaiser, Jr")
        name = name.replace("Clint E. Arnold", "Clinton E. Arnold")
        name = name.replace("Mark Saucy", "Mark R. Saucy")
        name = name.replace("Robert Chisholm", "Robert B. Chisholm Jr")
        name = name.replace("Andrew Steinmann", "Andrew E. Steinmann")
        name = name.replace("Bruce Ware", "Bruce A. Ware")
        name = name.replace("David Huttar", "David K. Huttar")
        name = name.replace("Walter Kaiser", "Walter C. Kaiser, Jr")
        name = name.replace("Andreas Köstenberger", "Andreas J. Köstenberger")
        name = name.replace("Elmer Martens", "Elmer A. Martens")
        name = name.replace("Herbert W. Bateman IV", "Herbert W. Bateman, IV")
        name = name.replace("James Alan Patterson", "James A. Patterson")
        name = name.replace("Douglas Kennard", "Douglas W. Kennard")
        name = name.replace("Ben L. Merkle", "Benjamin L. Merkle")
        name = name.replace("Joel Williams", "Joel F. Williams")
        name = name.replace("Scot Mcknight With R. Boaz Johnson", "Scot Mcknight And R. Boaz Johnson")
        name = name.replace("Tim Mcconnel", "Timothy I. Mcconnel")
        name = name.replace("Ken M. Campbell", "K. M. Campbell")
        name = name.replace("J.P. Moreland", "J. P. Moreland")
        name = name.replace("Gregory K. Beale", "G. K. Beale")
        name = name.replace("Joseph Hellerman", "Joseph H. Hellerman")
        name = name.replace("Robert Yarbrough", "Robert W. Yarbrough")
        name = name.replace("Tim Wiarda", "Timothy Wiarda")
        name = name.replace("Glen A. Scorgie", "Glen G. Scorgie")
        name = name.replace("Dave Mathewson", "Dave L. Mathewson")
        name = name.replace("Ernst Wendland", "Ernst R. Wendland")
        name = name.replace("David M. Howard Jr", "David M. Howard, Jr")
        name = name.replace("Homer Heater Jr", "Homer Heater, Jr")
        name = name.replace("Ron Youngblood", "Ronald F. Youngblood")
        name = name.replace("Gary Steven Shogren", "Gary S. Shogren")
        name = name.replace("Ronald Bergey", "Ronald L. Bergey")
        name = name.replace("Robertson Mcquilkin", "J. Robertson Mcquilkin")
        name = name.replace("Mark W. Chavalas", "Mark W. Chávalas")
        name = name.replace("Walt Russell", "Walter Bo Russell, II")
        name = name.replace("Todd S Labute", "Todd S. Labute")
        name = name.replace("Larry L. Helyer", "Larry R. Helyer")
        name = name.replace("Wayne Alan Detzler", "Wayne A. Detzler")
        name = name.replace("Rovert V. Rakestraw", "Robert V. Rakestraw")
        name = name.replace("Bruce A Demarest", "Bruce A. Demarest")
        name = name.replace("Aída Dina Besançon Spencer", "Aída Besançon Spencer")
        name = name.replace("Eugene Merrill", "Eugene H. Merrill")
        name = name.replace("Clark Pinnock", "Clark H. Pinnock")
        name = name.replace("Daniel Fuller", "Daniel P. Fuller")
        name = name.replace("S. J. Schultz", "Samuel J. Schultz")
        name = name.replace("Robert Duncan Culver", "Robert D. Culver")
        name = name.replace("Allen A. Macrae", "Allan A. Macrae")
        name = name.replace("Jerome Ficek", "Jerome L. Ficek")
        name = name.replace("Craig Keener", "Craig S. Keener")
        name = name.replace("Samuel S. Schultz", "Samuel J. Schultz")
        name = name.replace("Charles Horne", "Charles M. Horne")
        name = name.replace("Charles M. Home", "Charles M. Horne")
        name = name.replace("George Eldon Ladd", "George E. Ladd")
        name = name.replace("John Warwick Montgomery", "John W. Montgomery")
        name = name.replace("Richard Longenecker", "Richard N. Longenecker")
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
        name = name.replace("Bruce Waltke", "Bruce K. Waltke")
        name = name.replace(". Robert L. Saucy", "Robert L. Saucy")
        name = name.replace("Thomas Edward Mccomiskey", "Thomas E. Mccomiskey")
        name = name.replace("James B. De Young", "James B. Deyoung")
    return name

def is_known_author(name):
    for author in known_authors:
        if author in name:
            return True
    return False