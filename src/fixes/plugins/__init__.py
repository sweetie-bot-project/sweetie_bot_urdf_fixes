#!/usr/bin/env python

import os
import sys
import inspect

from collections import OrderedDict

path = os.path.dirname(os.path.realpath(__file__))
loaded = OrderedDict()

functions_names = [("rollout", "Apply fixes"), ("rollback", "Rollback fixes")]

functions = {'rollout': [],
             'rollback': []}

# Load loaded
sys.path.insert(0, path)
listd = os.listdir(path)
listd.sort()
for f in listd:
    fname, ext = os.path.splitext(f)
    if ext == '.py' \
    and fname != '__init__':
        mod = __import__(fname)
        loaded[fname] = mod.Plugin()
        for function, val in functions.items():
          if function in dir(loaded[fname]):
           functions[function].append(loaded[fname].name)
sys.path.pop(0)

