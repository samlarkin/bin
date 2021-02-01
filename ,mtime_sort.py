#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument(
    '-d',
    '--dirpath',
    help='directory to be sorted'
)
args = parser.parse_args()


def main(args):
    """ main procedure """
    if args.dirpath is None:
        sort_dir_by_mtime(os.curdir)
    else:
        dirpath = args.dirpath
        sorted_list = sort_dir_by_mtime(dirpath)
    rename_files_sorted(
        sorted_list,
        os.path.split(os.path.abspath(dirpath))[1]
    )


def sort_dir_by_mtime(dirpath):
    """ Sorts contents of directory by mtime
    Returns a sorted (by mtime) list of files in directory.

    """
    files = os.listdir(dirpath)
    files = [os.path.join(dirpath, f) for f in files]
    files.sort(key=os.path.getmtime)
    return files


def rename_files_sorted(sorted_list, rename_stem):
    """ Renames the files in a directory, such that they are listed in
    the order of sorted_list.

    """
    for index, path in enumerate(sorted_list):
        head, tail = os.path.split(path)
        _, ext = os.path.splitext(tail)
        number = '0' * (5 - len(str(index))) + str(index)
        new_path = os.path.join(head, f"{rename_stem}_{number}{ext.lower()}")
        sys.stderr.write(f"executing ... os.rename({path}, {new_path})\n")
        os.rename(path, new_path)


if __name__ == '__main__':
    main(args)
