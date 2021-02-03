#!/usr/bin/env python
"""Sync reading list with taskwarrior"""

import os
import json
import re
import argparse
import sys


def main():
    """Execute syncing procedure"""
    args = cli()
    reading_data = ReadingData('reading', args.file)
    tp = TaskParser(reading_data)
    tp.sync_task_to_md()
    mp = MarkdownParser(reading_data)
    mp.sync_md_to_task()
    reading_data.cleanup()
    return


def cli():
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file',
        nargs='?',
        default='/home/sam/notes/2020-08-28_5.md',
        help='reading list file for reading/writing markdown notes'
    )
    args = parser.parse_args()
    return args


class ReadingData:
    """Data holder class for reading list"""

    def __init__(self, project, md_file_path):
        self.project = project
        self.md_file_path = md_file_path
        self.json = f'/home/sam/tmp/{self.project}.json'
        self.task_project_export()
        self.task_data = self.read_json()
        self.md_list = self.get_md_list()

    def __repr__(self):
        return f"ReadingData('{self.project}', '{self.md_file_path}')"

    def task_project_export(self):
        cmd = f"task project:{self.project} export > {self.json}"
        sys.stderr.write(f'executing ... {cmd}\n')
        os.system(cmd)

    def read_json(self):
        with open(self.json, 'r') as json_file:
            self.task_data = json.load(json_file)
        sys.stderr.write(f'reading ... {self.json}\n')
        return self.task_data

    def get_md_list(self):
        with open(self.md_file_path, 'r') as md_file:
            self.md_list = md_file.read()
        sys.stderr.write(f'reading ... {self.md_file_path}\n')
        return self.md_list

    def cleanup(self):
        sys.stderr.write(f'removing ... {self.json} temporary file\n')
        os.system(f'rm {self.json}')


class TaskParser:
    """Parse taskwarrior tasks and pass them to a markdown file"""

    def __init__(self, reading_data):
        self.reading_data = reading_data

    def __repr__(self):
        return f'TaskParser({str(self.reading_data)})'

    def append_md_line(self, task):
        with open(self.reading_data.md_file_path, 'a') as md_file:
            md_file.write(f"* {task['description']}" + '\n')

    def new_entry_required(self, task):
        if task['description'] in self.reading_data.md_list:
            return False
        elif task['status'] == 'deleted':
            return False
        return True

    def add_to_md_list(self, task):
        if self.new_entry_required(task) is True:
            self.append_md_line(task)
            return 1
        return 0

    def sync_task_to_md(self):
        count = 0
        for task in self.reading_data.task_data:
            count += self.add_to_md_list(task)
        sys.stderr.write(
            f"{count} task(s) added to list at "
            f"'{self.reading_data.md_file_path}'\n"
        )


class MarkdownParser:
    """Parse markdown reading list and generate taskwarrior tasks"""

    def __init__(self, reading_data):
        self.reading_data = reading_data
        self.desc_re = re.compile(r'[A-Z].+\*.+\*')

    def __repr__(self):
        return f'MarkdownParser({str(self.reading_data)})'

    def match_book_desc(self):
        return self.desc_re.findall(self.reading_data.md_list)

    def new_entry_required(self, description):
        for task in self.reading_data.task_data:
            if task['description'] == description:
                return False
        return True

    def add_task(self, description):
        cmd = f"task add project:{self.reading_data.project} '{description}'\
                wait:eoy"
        os.system(cmd)
        return 1

    def sync_md_to_task(self):
        added = 0
        for description in self.match_book_desc():
            if self.new_entry_required(description) is True:
                added += self.add_task(description)
        sys.stderr.write(
            f"{added} task(s) added via 'task add project:reading'\n"
        )


if __name__ == '__main__':
    main()
