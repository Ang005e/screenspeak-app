import os, sys

def resourcePath(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = ""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def buildPath(*args: str):
    rel_path = ""
    for level in args:
        rel_path = os.path.join(rel_path, level)
    return rel_path