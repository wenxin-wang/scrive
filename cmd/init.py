#!/usr/bin/env python3

from libbartleby import helpers, options
from libbartleby.project import Project

import sys, os

optspec = """
bartleby init [-i importpath] [path]
---
i,import=: import file or directory
,origlang=: the language of original files
"""

optionParser = options.Options(optspec)
optionParser.usage()
opts, remains = optionParser.parse(sys.argv[1:])

paths = remains if remains else [os.getcwd()]
importpath = opts['i']
origlang= opts['origlang']
if importpath:
    if not origlang:
        raise Exception("Must give the language of imported files")
    if not os.path.isabs(importpath):
        importpath = os.path.join(os.getcwd(), importpath)

for p in paths:
    if not os.path.isabs(p):
        p = os.path.join(os.getcwd(), p)
    if p == importpath:
        raise Exception("Project path cannot be the same as import path")

    proj = Project(p)
    proj.create()

    if(importpath):
        proj.import_orig(importpath, origlang)

    proj.init()
    files = proj.get_status()
    proj.add_to_cache(files[1]+files[2])
    proj.commit("Initialized project {}".format(os.path.basename(p)))
