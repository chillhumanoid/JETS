import os
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

def get_size():
    total_size = 0
    for root, dirs, files in os.walk(var.download_folder):
        for file in files:
            check_path = os.path.join(var.download_folder, root,  file)
            total_size += os.path.getsize(check_path)
    return '{:.2f} GB'.format(total_size/float(1 << 30))

def get_files():
    current_path = os.getcwd()
    file = os.path.join(current_path, 'file_count.txt')
    if not os.path.exists(file):
        with open(file, 'w') as f:
            f.write('0')
        return 0
    else:
        with open(file, 'r') as f:
            value = f.readlines()[0]
        return value

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
