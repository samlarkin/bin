#!/usr/bin/python3
""" Parses output from taskwarrior and adds items from reading project
to my reading list at ~/notes/2020-08-28_5.md, first checking whether
there's already an entry for that book

"""
import os
import json
import re


def main():
    export_project('reading')
    tasks = read_json('reading.json')
    path = '/home/sam/notes/2020-08-28_5.md'
    reading_list = get_reading_list(path)
    description_re = re.compile(r'[A-Z].+\*.+\*')
    added = 0
    for task in tasks:
        add = add_to_reading_list(task, reading_list, path)
        if add is not None:
            added += add
    if added == 1:
        book = 'book'
    else:
        book = 'books'
    print(f'{added} {book} added to reading list at {path}')
    tasks_added = 0
    for list_line in reading_list.split('\n'):
        desc = description_re.search(list_line)
        if desc:
            done = False
            for task in tasks:
                if task['description'] == desc.group():
                    done = True
                    break
            if done is False:
                print(desc.group())
                tasks_added += add_to_task('reading', desc.group())
    print(f'{tasks_added} tasks added to task project:reading')
    cleanup('reading')


def export_project(project):
    cmd = f"task project:{project} export > {project}.json"
    os.system(cmd)


def read_json(file_name):
    with open(f'{file_name}', 'r') as json_file:
        task_data = json.load(json_file)
    return task_data


def get_reading_list(path):
    with open(path, 'r') as md_file:
        reading_list = md_file.read()
    return reading_list


def gen_md_line(task):
    md_line = f"* {task['description']}" + '\n'
    return md_line


def append_md_line(md_line, path):
    with open(path, 'a') as md_file:
        md_file.write(md_line)


def add_to_reading_list(task, reading_list, path):
    if task['description'] not in reading_list:
        md_line = gen_md_line(task)
        append_md_line(md_line, path)
        return 1


def add_to_task(project, description):
    cmd = f"task add project:{project} '{description}'"
    os.system(cmd)
    return 1


def cleanup(project):
    cleanup_cmd = f'rm {project}.json'
    os.system(cleanup_cmd)


if __name__ == '__main__':
    main()
