import json
from typing import Any, Dict, Set
from pathlib import Path


def _get_data_path(filename):
    try:
        return next(Path('.').rglob(filename)).resolve()
    except StopIteration:
        return None

def _is_line_chanhed(line_one, line_two):
    return line_one != line_two


def _create_format_line(file, lines, diff, symbol):
    for line in lines:
        diff[f'{symbol} {line}'] = file[line]


def _sort_logic(item, sybmol_priority='-'):
    name_line, _ = item

    first_symbol = name_line[0]

    clean_line = name_line.lstrip('+- ').strip()

    if sybmol_priority == '-':
        return clean_line, -ord(first_symbol)
    else:
        return clean_line, ord(first_symbol)


def _format_differences_in_files(
        first_file: Dict[str, Any],
        second_file: Dict[str, Any],
        only_in_first,
        only_in_second,
        unchanged_lines,
        changed_lines
        ):
    sorted_diff_file: Dict = {}

    _create_format_line(first_file, only_in_first, sorted_diff_file, '-')
    _create_format_line(second_file, only_in_second, sorted_diff_file, '+')
    _create_format_line(first_file, unchanged_lines, sorted_diff_file, ' ')

    for line in changed_lines:
        sorted_diff_file[f'- {line}'] = first_file[line]
        sorted_diff_file[f'+ {line}'] = second_file[line]

    sorted_diff_file = dict(sorted(
        sorted_diff_file.items(),
        key=lambda item: _sort_logic(item)
    ))

    return sorted_diff_file


def _find_diff(first_file: Dict[str, Any], second_file: Dict[str, Any]
               ) -> Dict[str, Any]:

    first_file_lines = first_file.keys()
    second_file_lines = second_file.keys()

    general_lines = first_file_lines & second_file_lines

    only_in_first = first_file_lines - second_file_lines
    only_in_second = second_file_lines - first_file_lines

    unchanged_lines: Set = set()
    changed_lines: Set = set()

    for name_line in general_lines:
        if _is_line_chanhed(first_file[name_line], second_file[name_line]):
            changed_lines.add(name_line)
        else:
            unchanged_lines.add(name_line)

    diff: Dict = {}

    diff = _format_differences_in_files(first_file,
                                        second_file,
                                        only_in_first,
                                        only_in_second,
                                        unchanged_lines,
                                        changed_lines)

    return diff


def generate_diff(file1, file2):
    
    file_extention = get_file_extention(file1, file2)

    if file_extention == 'json':
        print(generate_diff_json(file1, file2), end='')
    elif file_extention == 'yaml':
        print(generate_diff_yaml(file1, file2), end='')
    else:
        print('Incorrect file format', end='')


def get_file_extention(file1, file2):
    _, file1_extention = file1.split('.')
    _, file2_extention = file2.split('.')

    if file1_extention and file2_extention == 'json':
        return 'json'
    elif file1_extention and file2_extention == 'yaml' \
        or file1_extention and file2_extention == 'yml':
        return 'yaml'



def generate_diff_json(file1, file2):

    file1_path = _get_data_path(file1)
    file2_path = _get_data_path(file2)

    if file1_path is None or file2_path is None:
        return 'File not found!'
    
    try:
        data1 = json.load(open(file1_path))
        data2 = json.load(open(file2_path))
        
    except json.decoder.JSONDecodeError:
        return 'Incorrect JSON file uploaded'

    diff = json.dumps(_find_diff(data1, data2), indent=2)

    return diff.replace('"', '').replace(',', '')


def generate_diff_yaml(file1, file2):
    pass