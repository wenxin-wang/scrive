# Config file parser
import os
import configparser

class Config(configparser.ConfigParser):
    def __init__(self, file):
        """instantiate a config parser"""
        self.cfgfile = file
        super().__init__()
        if os.path.isfile(self.cfgfile):
            self.read(file)
    def __str__(self):
        return '\n'.join('[' + section + ']\n' + '\n'.join(str(k)+'='+str(v) for (k,v) in self[section].items()) for section in self.sections())
    def writecfg(self):
        """Write a config file to disk"""
        with open(self.cfgfile, 'a+') as cfg:
            self.write(cfg)
