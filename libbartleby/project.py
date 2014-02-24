# Define a translatin project here

import os, shutil
from libbartleby import config, helpers
from libbartleby.repository import Repository

class Project(Repository):
    def __init__(self, path):
        """Construct a project"""
        super().__init__(os.path.abspath(path))
        self.config = config.Config(os.path.join(self.path, helpers.configname))
        self.orig_path = os.path.join(self.path, 'orig')
    def create(self, importpath=''):
        if os.path.exists(self.path):
            if not helpers.dir_empty(self.path):
                raise OSError("Create project: {} exists and not empty".format(self.path))
        else:
            os.mkdir(self.path)
        os.mkdir(self.orig_path)
        self.config["Language"] = {}
        self.config["Language"]['Orig'] = 'en_US'
        self.config.writecfg()
        if importpath:
            self._import(importpath)
        self.init()
        files = self.get_status()
        self.add_to_cache(files[1]+files[2])
        self.commit("Initialized project {}".format(os.path.basename(self.path)))
    def _import(self, path):
        if not os.path.exists(path):
            raise OSError("Project import: {} doesn't exits".format(path))
        elif os.path.isdir(path):
            for dirpath, dirs, files in os.walk(path):
                relpath = os.path.relpath(dirpath, path)
                for dirname in dirs:
                    dest = os.path.join(self.orig_path, relpath, dirname)
                    os.mkdir(dest)
                for filename in files:
                    orig = os.path.join(dirpath, filename)
                    dest = os.path.join(self.orig_path, relpath, filename)
                    shutil.copy(orig, dest)
        else:
            filename = os.path.basename(path)
            orig = path
            dest = os.path.join(self.orig_path, filename)
            shutil.copy(orig, dest)
    def update_original(self):
        """docstring for update_original"""
    def update_translations(self):
        """docstring for update_translations"""
