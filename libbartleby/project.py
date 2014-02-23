# Define a translatin project here

import os, shutil
from libbartleby import config, helpers

class Project:
    def __init__(self, path):
        """Construct a project"""
        self.path = os.path.abspath(path)
        self.config = config.Config(os.path.join(self.path, helpers.configname))
        self.orig_path = os.path.join(self.path, 'orig')
    def create(self, importpath=''):
        if os.path.exists(self.path):
            return
        try:
            os.mkdir(self.path)
            os.mkdir(self.orig_path)
            self.config["Language"] = {}
            self.config["Language"]['Orig'] = 'en_US'
            self.config.writecfg()
        except OSError as e:
            print(e)
        if importpath:
            self._import(importpath)
    def _import(self, path):
        if not os.path.exists(path):
            raise OSError("Project import: {} doesn't exits".format(path))
        elif os.path.isdir(path):
            for dirpath, dirs, files in os.walk(path):
                relpath = os.path.relpath(dirpath, path)
                for dirname in dirs:
                    os.mkdir(os.path.join(self.orig_path, relpath, dirname))
                for filename in files:
                    shutil.copy(os.path.join(dirpath, filename), os.path.join(self.orig_path, relpath, filename))
        else:
            filename = os.path.basename(path)
            shutil.copy(path, os.path.join(self.orig_path, filename))
    def update_original(self):
        """docstring for update_original"""
    def update_translations(self):
        """docstring for update_translations"""
