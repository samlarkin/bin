#!/usr/bin/env python
# coding: utf-8

import re
from random import randint
import string
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('input_file',
                    help='the file to be scrambled')
args = parser.parse_args()


def main(input_file):
    text = read_input(input_file)
    input_numbers = find_input_numbers(text)
    scrambled_numbers = gen_scrambled_numbers(input_numbers)
    output_text = replace_list(text, input_numbers, scrambled_numbers)
    sys.stdout.write(output_text)
    return output_text


def read_input(input_file):
    with open(input_file, 'r') as f:
        text = f.read()
    return text


def find_input_numbers(input_string):
    digit_regex = re.compile(r'\d+')
    input_numbers = digit_regex.findall(input_string)
    return input_numbers


def gen_scrambled_numbers(real_numbers):
    scrambled_numbers = []
    for number in real_numbers:
        scrambled_number = ''
        for digit in number:
            if digit in string.digits:
                random_digit = str(randint(0, 9))
                scrambled_number += random_digit
            else:
                scrambled_number += digit
        scrambled_numbers.append(scrambled_number)
    return scrambled_numbers


def replace_list(input_string, old_list, new_list):
    output_string = input_string
    for old, new in zip(old_list, new_list):
        output_string = output_string.replace(old, new)
    return output_string


if __name__ == '__main__':
    main(args.input_file)
