import os
from exceptions import NoContentError
from output import bold_red


def check_empty(data):
    if not data:
        raise NoContentError


def trim_line(line):
    line = line.upper()
    splitted = line.split()
    prepared = ''.join(splitted)
    return prepared


def trim_lines(file_raw_data):
    validated_lines = list()
    for line in file_raw_data:
        line_without_comments = (line.split('#')[0] or '').strip()
        if line_without_comments:
            validated_lines.append(line_without_comments)

    trimmed = list()
    for line in validated_lines:
        trimmed.append(trim_line(line))

    return trimmed


def read_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'File {file_path} doesn\'t exist')
    with open(file_path, 'r') as file:
        file_raw_data = file.readlines()
    trimmed_data = trim_lines(file_raw_data)
    try:
        check_empty(trimmed_data)
    except NoContentError as e:
        exit(bold_red(e))

    return trimmed_data
