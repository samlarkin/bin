#!/usr/bin/python3
import os
import re

directory = input('Enter the absolute path of the directory:\n')
from_ext = input("Change files with extension [e.g. .txt]:\n")
to_ext = input("To files with extension [e.g. .md]:\n")
regex = re.compile(f'.+{from_ext}')

for f in os.listdir(directory):
    if regex.match(f):
        (name, ext) = f.split('.')
        cmd = f"mv {f} {name + to_ext}"
        os.system(cmd)
