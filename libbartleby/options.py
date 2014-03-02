# Handle options
"""
Use the concept of optionspec from bup.
Get a optionspec from subcmd, use it to parse a string of options
An example of optionspec:
'bartleby cmd [ -o ]
---
o,option=: description
'
"""

from libbartleby.helpers import log

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

    def __setitem__(self, option, value=True):
        option = self._unalias(option)
        self.options[option] = value

    def __getitem__(self, option):
        option = self._unalias(option)
        return self.options[option]

    def _unalias(self, option):
        return self._aliases.get(option, option) # if option is not an alias, return option

class Options:
    """Init from a option spec, can be used to parse option string"""
    def __init__(self, optionspec):
        """Construct an option string"""
        self._spec = optionspec
        self._aliases = {}
        self._options = {} # usually short
        self._usagestr = ''
        self._has_params = []
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
            helplines.append(self._parse_opt_line(l))
        lines.reverse()
        self._usagestr = '\n'.join(lines + helplines)

    def _parse_opt_line(self, line):
        """Parse a option line in an optionspec"""
        opts, desc = line.split(": ") # Get option's short/long names and its description
        opts = opts.split(",")
        if opts[-1].endswith('='):
            opts[-1]=opts[-1][:-1]
            self._has_params.append(opts[0])
        self._options['opt'] = desc
        if len(opts) > 1: # Has aliases
            for o in opts[1:]:
                if o in self._aliases:
                    raise KeyError("Option '{}': alias {} already set to {}".format(opts[0], o, self._aliases[o]))
                self._aliases[o] = opts[0]
        return("{:<4} {}".format(opts[0], desc))

    def parse(self, arglist):
        """Parse an argument list according to option spec"""
        opt = OptDict(self._aliases)

    def usage(self, msg=''):
        log(self._usagestr)
        if msg:
            log(msg)

    class InvalidOption(Exception):
        def __init__(self, msg=''):
            super().init(msg)
