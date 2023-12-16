#!/usr/bin/env python
"""Sort files in a given directory by time modified.

If no directory is specified, the program will default to the current
working directory.
"""

import os
import argparse
import sys


def main():
    """Sort and rename files."""
    args = cli()
    if args.dirpath is None:
        args.dirpath = os.curdir
    sorted_list = sort_dir_by_mtime(args.dirpath)
    rename_files_sorted(
        sorted_list,
        os.path.split(os.path.abspath(args.dirpath))[1]
    )
    return


def cli():
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--dirpath',
        help='directory to be sorted'
    )
    args = parser.parse_args()
    return args


def sort_dir_by_mtime(dirpath):
    """Sorts contents of directory by mtime.

    Return a sorted list of files in directory.
    """
    files = os.listdir(dirpath)
    files = [os.path.join(dirpath, f) for f in files]
    files.sort(key=os.path.getmtime)
    return files


def rename_files_sorted(sorted_list, rename_stem):
    """ Rename the files in a directory

    Choose names such that they are listed in the order of sorted_list.
    """
    for index, path in enumerate(sorted_list):
        head, tail = os.path.split(path)
        _, ext = os.path.splitext(tail)
        number = '0' * (5 - len(str(index))) + str(index)
        new_path = os.path.join(head, f"{rename_stem}_{number}{ext.lower()}")
        sys.stderr.write(f"executing ... os.rename({path}, {new_path})\n")
        os.rename(path, new_path)
    return


if __name__ == '__main__':
    main()
