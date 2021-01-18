#!/usr/bin/python3
""" Sync reading list between taskwarrior and ~/notes/ """
import os
import json
import re


class TaskParser:
    """ Parsing tasks from taskwarrior and passing them to a markdown file """
    def __init__(self, project, path_to_notes):
        self.project = project
        self.path_to_notes = path_to_notes
        self.json = f'{self.project}.json'
        self.task_data = []
        self.md_list = ''

    def __repr__(self):
        return f"TaskParser('{self.project}', '{self.path_to_notes}')"

    def export_project(self):
        cmd = f"task project:{self.project} export > {self.json}"
        os.system(cmd)

    def read_json(self):
        with open(self.json, 'r') as json_file:
            self.task_data = json.load(json_file)
        return self.task_data

    def get_md_list(self):
        with open(self.path_to_notes, 'r') as md_file:
            self.md_list = md_file.read()
        return self.md_list

    def gen_md_line(self, task):
        md_line = f"* {task['description']}" + '\n'
        return md_line

    def append_md_line(self, md_line):
        with open(self.path_to_notes, 'a') as md_file:
            md_file.write(md_line)

    def find_match(self, task):
        if task['description'] in self.md_list or task['status'] == 'deleted':
            return True
        return False

    def add_to_md_list(self, task):
        if self.find_match(task) is False:
            md_line = self.gen_md_line(task)
            self.append_md_line(md_line)
            return 1
        return 0

    def cleanup(self):
        os.system(f'rm {self.json}')

    def sync_task_to_md(self):
        self.export_project()
        self.read_json()
        self.get_md_list()
        count = 0
        for task in self.task_data:
            count += self.add_to_md_list(task)
        print(f"{count} task(s) added to list at '{self.path_to_notes}'")


class MarkdownParser:
    """ Parsing reading list entries and passing them to taskwarrior """
    def __init__(self, path_to_notes, task_data):
        self.path_to_notes = path_to_notes
        self.desc_re = re.compile(r'[A-Z].+\*.+\*')
        self.task_data = task_data

    def get_md_list(self):
        with open(self.path_to_notes, 'r') as md_file:
            self.md_list = md_file.readlines()
        return self.md_list

    def match_book_desc(self, text):
        return self.desc_re.search(text)

    def find_match(self, description):
        for task in self.task_data:
            if task['description'] == description:
                return True
        return False

    def add_task(self, project, description):
        os.system(f"task add project:{project} '{description}'")
        return 1

    def sync_md_to_task(self):
        self.get_md_list()
        added = 0
        for md_line in self.md_list:
            match = self.match_book_desc(md_line)
            if match:
                description = match.group()
                task_exists = self.find_match(description)
                if task_exists is False:
                    added += self.add_task('reading', description)
        print(f"{added} task(s) added via 'task add project:reading'")


def main():
    tw_parser = TaskParser('reading', '/home/sam/notes/2020-08-28_5.md')
    tw_parser.sync_task_to_md()
    tw_parser.cleanup()

    md_parser = MarkdownParser(tw_parser.path_to_notes, tw_parser.task_data)
    md_parser.sync_md_to_task()


if __name__ == '__main__':
    main()
