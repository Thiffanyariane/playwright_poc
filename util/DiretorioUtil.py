import os


def createDir(pasta):
    if not os.path.isdir(pasta):
        os.mkdir(pasta)


def findUniqueFile(path):
    try:
        return os.listdir(path)[0]
    except Exception as ex:
        return ''


def removeFile(path):
    try:
        os.remove(path)
        return True
    except:
        return False
