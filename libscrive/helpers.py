import sys, os

configname = 'config.ini' if sys.platform == 'win32' else '.config'
filelistname = 'filelist.ini' if sys.platform == 'win32' else '.filelist'

def log(msg):
    """Log msg"""
    print(msg)

def err(msg):
    """Log err"""
    print(msg, file=sys.stderr)

def dir_empty(dir):
    """
    Check if dir is empty.
    We do not check if dir is relative.
    """
    return not os.listdir(dir)

def columnate(items, prefix):
    if not items:
        return ""
    _return = prefix
    for item in items:
        _return += "%s  " % item
    return _return

def cmd_filename(subcmd_name):
    return subcmd_name + '.py'

def file_cmdname(filename):
    name, ext = os.path.splitext(filename)
    if not ext or ext == '.py':
        return name
    else:
        return None
