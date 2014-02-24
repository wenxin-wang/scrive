# A wrapper library for git

import os, subprocess, string

class Repository:
    @staticmethod
    def get_toplevel():
        """Get the toplevel of a project"""
        subprocess.call(["git", "rev-parse", "--show-toplevel"])
    def __init__(self, path):
        self.path = path
        self.dotgit = os.path.join(self.path, '.git')
        self.gitcmd = ['git', "--git-dir={}".format(self.dotgit), "--work-tree={}".format(self.path)]
    def init(self):
        """
        Same as calling 'git init self.path'
        """
        return subprocess.call(["git", "init", self.path])
    def get_status(self):
        """
        Get current git status. If success, return:
        cached, changed, created
        """
        cached = []
        changed = []
        created = []
        s = subprocess.check_output(self.gitcmd + ['status', '--porcelain'], universal_newlines=True)
        print(s)
        for line in s.splitlines():
            print(line.split(" "))
            if line.startswith(" "):
                relname = line.split(" ")[2]
                changed.append(os.path.join(self.path, relname))
            elif line.startswith("??"):
                relname = line.split(" ")[1]
                created.append(os.path.join(self.path, relname))
            else:
                relname = line.split(" ")[1]
                cached.append(os.path.join(self.path, relname))
        return cached, changed, created
    def add_to_cache(self, files):
        """
        Read a list of files, add them to cache
        """
        for filename in files:
            print(filename)
            try:
                subprocess.check_call(self.gitcmd + ['add', filename]) != 0
            except subprocess.CalledProcessError as e:
                print(e, 'git add: {} failed'.format(filename))
    def commit(self, msg):
        """
        If there's something in cache, commit them with msg
        """
        cached, _, _ = self.get_status()
        if not cached:
            return
        try:
            subprocess.check_call(self.gitcmd + ['commit', '-m', msg]) !=0
        except subprocess.CalledProcessError as e:
            print(e, 'git commit failed')
