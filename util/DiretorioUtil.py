import os


def create_dir(pasta):
    if not os.path.isdir(pasta):
        os.mkdir(pasta)


def find_unique_file(path):
    try:
        return os.listdir(path)[0]
    except:
        return ''


def remove_file(path):
    try:
        os.remove(path)
        return True
    except:
        return False
