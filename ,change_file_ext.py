#!/usr/bin/env python
"""Change file extension of every file in a directory.

If dirpath is not set, the program will default to operating on the
current working directory.

>>> ,change_file_ext.py [-d DIRPATH] FROM_EXT TO_EXT
"""

import os
import sys
import argparse


def main():
    """Identify and rename files"""
    args = cli()
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
    return


def has_ext(file_name, from_ext):
    """Check file extension for match with from_ext

    Return tuple of (root, ext) if the extension matches from_ext.
    Otherwise return None.
    """
    root, ext = os.path.splitext(file_name)
    if ext == from_ext:
        return (root, ext)
    return None


def cli():
    """Parse and return command line arguments"""
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
    return args


if __name__ == '__main__':
    main()
