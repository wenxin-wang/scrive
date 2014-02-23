import sys

configname = 'config.ini' if sys.platform == 'win32' else '.config'

def log(msg):
    """Log msg"""
    print(msg, file=sys.stderr)
