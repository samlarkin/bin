#!/bin/env python

import os
import re

tagline = re.compile(r'^\:.+\:$')


def main():
    files = os.listdir(os.curdir)
    for fn in files:
        tags = get_tags(fn)
        write_tags(fn, tags)


def get_tags(fn):
    with open(fn, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if tagline.match(line):
                tags = line.split(':')
                tags = tags[1:len(tags)-2]
                return tags


def write_tags(fn, tags):
    with open(fn, 'a') as f:
        f.write("tags = " + str(tags))


if __name__ == '__main__':
    main()
tags = None