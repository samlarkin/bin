""" Generates an index file for my notes directory

author: Sam Larkin
date: 2021-01-03

"""
import os
import re
import linecache


def get_file_list(notes_path):
    """ Get sorted list of files in notes_path directory with .md type """
    all_files = os.listdir(notes_path)
    regex = re.compile(r'.+(?=\.md)')
    file_list = []
    for file_name in all_files:
        match = regex.match(file_name)
        if match:
            file_list.append(match.group())
    return sorted(file_list)


def overwrite_index(notes_path):
    """ Overwrite index with blank template """
    index_template = notes_path + 'compiler/index_template'
    index = notes_path + 'index.md'
    os.system(f'cat {index_template} > {index}')
    return index


def get_title(notes_path, file_stem):
    """ Get the title by reading the second line of the .md file """
    title = linecache.getline(notes_path + file_stem + '.md', 2)
    title = title.replace('\n', '')
    title = title.replace('title: ', '')
    return title


def compose_line(title, file_stem):
    """ Composes the line to be written to the index in md format """
    index_line = f'* [{title}]({file_stem}.html)' + '\n'
    return index_line


def write_indexline(index, index_line):
    """ Write (append) an entry to the index_file """
    with open(index, 'a') as index_file:
        index_file.write(index_line)


def main(notes_path):
    file_list = get_file_list(notes_path)
    index = overwrite_index(notes_path)

    for file_stem in file_list:
        title = get_title(notes_path, file_stem)
        index_line = compose_line(title, file_stem)
        write_indexline(index, index_line)


if __name__ == '__main__':
    main(notes_path='/home/sam/notes/')
