# Define a translatin project here

import os, shutil
from libbartleby import config, helpers, translator
from libbartleby.repository import Repository

class Project(Repository):
    def __init__(self, path):
        """Construct a project"""
        super().__init__(os.path.abspath(path))
        self.config = config.Config(os.path.join(self.path, helpers.configname))
        self.orig_path = os.path.join(self.path, 'orig')

    def create(self):
        if os.path.exists(self.path):
            if not helpers.dir_empty(self.path):
                raise OSError("Create project: {} exists and not empty".format(self.path))
        else:
            os.mkdir(self.path)
        os.mkdir(self.orig_path)

    def import_orig(self, path, lang):
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
        self._update_orig_file_list()
        self.config.set_orig_lang(lang)
        self.config.writecfg()

    def _get_orig_files(self):
        """Get files under self.orig_path"""
        if not os.path.exists(self.orig_path):
            raise OSError("{} doesn't exits".format(self.orig_path))
        orig_files = []
        for dirpath, dirs, files in os.walk(self.orig_path):
            relpath = os.path.relpath(dirpath, self.orig_path)
            if relpath == '.':
                relpath = ''
            for filename in files:
                relname = os.path.join(relpath, filename)
                orig_files.append(relname)
        return orig_files

    def _update_orig_file_list(self):
        """Update original file list"""
        orig_files = self._get_orig_files()
        with open(os.path.join(self.path, helpers.filelistname), 'w+') as filelist:
            for filename in orig_files:
                realfile = os.path.join(self.orig_path, filename)
                filelist.write(filename + " : " + translator.get_filetype(realfile) + '\n')

    def update_original(self):
        """docstring for update_original"""
    def update_translations(self):
        """docstring for update_translations"""
