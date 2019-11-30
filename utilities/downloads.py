import os, shutil
from utilities import variables as var

def get_location():
    current_path = os.getcwd()
    check = os.path.join(current_path, 'download_location.txt')
    if not os.path.exists(check):
        path = os.path.join(os.path.expanduser('~'), 'Documents', 'JETS')
        if not os.path.exists(path):
            os.mkdir(path)
        with open(check, 'w') as f:
            f.write(path)
        return path
    else:
        with open(check, 'r') as f:
            path = f.readlines()[0]
        return path

def delete_all():
    for root, dirs, files in os.walk(var.download_folder):
        for file in files:
            file_path = os.path.join(var.download_folder, root, file)
            os.remove(file_path)
    shutil.rmtree(var.download_folder) #just a full on delete
    os.mkdir(var.download_folder) #just a full on remake
    
def get_size():
    total_size = 0
    for root, dirs, files in os.walk(var.download_folder):
        for file in files:
            check_path = os.path.join(var.download_folder, root,  file)
            total_size += os.path.getsize(check_path)
    return '{:.2f} GB'.format(total_size/float(1 << 30))

def get_files():
    total_files = 0
    for root, dirs, files in os.walk(var.download_folder):
        total_files += len(files)
    return total_files

def add_files():
    file = os.path.join(os.getcwd(), 'file_count.txt')
    number = get_files() + 1
    with open(file, 'w') as f:
        f.write(number)

def set_location(new_location):
    var.download_folder = new_location
    check = os.path.join(os.getcwd(), 'download_location.txt')
    with open(check, 'w') as f:
        f.write(new_location)
