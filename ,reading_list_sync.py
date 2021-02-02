import os
import json
import re


class ReadingData:
    """ Data holder class for reading list """
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
        os.system(cmd)
        print(f'task project:{self.project} exported to {self.json}')

    def read_json(self):
        with open(self.json, 'r') as json_file:
            self.task_data = json.load(json_file)
        print(f'task list read from {self.json}')
        return self.task_data

    def get_md_list(self):
        with open(self.md_file_path, 'r') as md_file:
            self.md_list = md_file.read()
        print(f'Markdown reading list read from {self.md_file_path}')
        return self.md_list

    def cleanup(self):
        os.system(f'rm {self.json}')
        print('Temporary file {self.json} removed')


class TaskParser:
    """ Parse taskwarrior tasks and pass them to a markdown file """
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
        print(f"{count} task(s) added to list at "
              f"'{self.reading_data.md_file_path}'")


class MarkdownParser:
    """ Parse markdown reading list and generate taskwarrior tasks """
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
        print(f"{added} task(s) added via 'task add project:reading'")


def main():
    reading_data = ReadingData('reading', '/home/sam/notes/2020-08-28_5.md')
    tp = TaskParser(reading_data)
    tp.sync_task_to_md()
    mp = MarkdownParser(reading_data)
    mp.sync_md_to_task()


if __name__ == '__main__':
    main()
