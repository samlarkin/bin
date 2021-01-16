#!/usr/bin/python3
import os
import re

for f in os.listdir('.'):
    if re.match(r'.+\.raw', f):
        (name, ext) = f.split('.')
        cmd = f"mv {f} {name + '.txt'}"
        os.system(cmd)
