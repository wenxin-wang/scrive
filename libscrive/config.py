# Config file parser
import os
import configparser

class Config(configparser.ConfigParser):
    def __init__(self, file):
        """instantiate a config parser"""
        self.cfgfile = file
        super().__init__()
        self.readcfg()

    def __str__(self):
        return '\n'.join('[' + section + ']\n' + '\n'.join(str(k)+'='+str(v) for (k,v) in self[section].items()) for section in self.sections())

    def readcfg(self):
        if os.path.isfile(self.cfgfile):
            self.read(file)

    def writecfg(self):
        """Write a config file to disk"""
        with open(self.cfgfile, 'w') as cfg:
            self.write(cfg)

    def set_orig_lang(self, lang, force=False):
        """Set the language of original project"""
        if self.has_option("Original", "lang") and not force:
            raise Exception("Language of the original project already setted and we didn't force the changing")
        if not self.has_section("Original"):
            self.add_section("Original")
            self["Original"]["lang"] = lang
