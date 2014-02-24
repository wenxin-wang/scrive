import sys, os

configname = 'config.ini' if sys.platform == 'win32' else '.config'

def log(msg):
    """Log msg"""
    print(msg, file=sys.stderr)

def dir_empty(dir):
    """
    Check if dir is empty.
    We do not check if dir is relative.
    """
    return not os.listdir(dir)
