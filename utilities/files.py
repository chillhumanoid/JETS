import os
from utilities import downloads
def isSame(old, new):
    return old == new

def change_path(new, old):
    if not new == "":
        file_path = os.path.join(new, 'JETS')
        file_path = file_path.replace("/", "\\")
    if not isSame(old, file_path):
        os.rename(old, file_path)
        downloads.set_location(file_path)
