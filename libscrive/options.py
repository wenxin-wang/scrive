# Handle options
"""
Use the concept of optionspec from bup.
Get a optionspec from subcmd, use it to parse a string of options
An example of optionspec:
'scrive cmd [ -o ]
---
o,option=: description
,no_short: no short name
'
"""

import getopt
from libscrive.helpers import log

class OptDict:
    """
    options =
    {
        option1: value1
        option2: True
    }
    aliases = 
    {
        o1: option1
        o2: option2
    }
    """
    def __init__(self, aliases):
        self._options = {}
        self._aliases = aliases

    def __setitem__(self, option, value):
        option = self._unalias(option)
        self._options[option] = value

    def __getitem__(self, option):
        option = self._unalias(option)
        return self._options.get(option, None)

    def _unalias(self, option):
        return self._aliases.get(option, option) # if option is not an alias, return option

class Options:
    """Init from a option spec, can be used to parse option string"""
    def __init__(self, optionspec):
        """Construct an option string"""
        self._spec = optionspec
        self._aliases = {}
        self._short_opts = ''
        self._long_opts = []
        self._usagestr = ''
        self._parse_spec() # set self._usagestr, self._options and self._aliases

    def _parse_spec(self):
        """
        Parse the optionspec, generate usagestr and a set of OptDict
        """
        lines = [ s.strip() for s in self._spec.strip().split('\n')]
        helplines = []
        while lines:
            l = lines.pop() # In reverse order
            if l == '---': break # The rest is usage string
            helplines.append(self._parse_spec_line(l))
        helplines.reverse()
        lines.reverse()
        self._usagestr = '\n'.join(lines + helplines)

    def _parse_spec_line(self, line):
        """Parse a option line in an optionspec"""
        opts, desc = line.split(": ") # Get option's short/long names and its description
        opts = opts.split(",")

        has_short = True
        if opts[0] == '':
            has_short = False
            del opts[0]

        if opts[-1].endswith('='): # Takes a value
            has_value = True
            opts[-1]=opts[-1][:-1]
        else:
            has_value = False

        if has_short:
            self._short_opts += opts[0] + (':' if has_value else '')
        else:
            self._long_opts.append(opts[0] + ('=' if has_value else ''))

        if len(opts) > 1: # Has aliases
            for o in opts[1:]:
                if o in self._aliases:
                    raise KeyError("Option '{}': alias {} already set to {}".format(opts[0], o, self._aliases[o]))
                self._aliases[o] = opts[0]
                self._long_opts.append(o + ('=' if has_value else ''))
        return("{:<10} {}".format("|".join(opts), desc))

    def parse(self, arglist):
        """Parse an argument list according to option spec"""
        raw_opts, remains = getopt.getopt(arglist, self._short_opts, self._long_opts)
        opts = OptDict(self._aliases)
        for k,v in raw_opts:
            if v == '': v = True
            opts[k.lstrip('-')] = v
        return opts, remains

    def usage(self, msg=''):
        log(self._usagestr)
        if msg:
            log(msg)
