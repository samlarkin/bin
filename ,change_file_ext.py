#!/usr/bin/env python
# coding: utf-8

import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    'from_ext',
    help='file extension to change from e.g. [.txt]'
)
parser.add_argument(
    'to_ext',
    help='file extension to change to e.g. [.md]'
)
parser.add_argument(
    '-d',
    '--dirpath',
    help='path to the directory of the files to be changed e.g. '
         '[/home/user]\n'
         'If DIRPATH is not set, the program will default to the '
         'current working directory.'
)
args = parser.parse_args()


def main(args):
    if args.dirpath is None:
        args.dirpath = os.curdir
    for f in os.listdir(args.dirpath):
        condition = has_ext(f, args.from_ext)
        if condition is None:
            continue
        else:
            root = condition[0]
            sys.stderr.write(
                f"executing ... os.rename("
                f"{os.path.join(args.dirpath, f)} "
                f"{os.path.join(args.dirpath, root + args.to_ext)})\n"
            )
            os.rename(
                f"{os.path.join(args.dirpath, f)}",
                f"{os.path.join(args.dirpath, root + args.to_ext)}"
            )


def has_ext(file_name, from_ext):
    root, ext = os.path.splitext(file_name)
    if ext == from_ext:
        return (root, ext)
    return None


if __name__ == '__main__':
    main(args)
