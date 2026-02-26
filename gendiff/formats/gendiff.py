import json
from typing import Any, Dict, Set

import yaml

from gendiff.formats.format_instruments import (
    _format_differences_in_files,
    _get_data_path,
    _is_line_chanhed,
    get_file_extention,
)


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

    file1_path = _get_data_path(file1)
    file2_path = _get_data_path(file2)

    if file1_path is None or file2_path is None:
        print('File not found!', end='')
        return

    if file_extention == 'json':
        print(generate_diff_json(file1_path, file2_path), end='')
    elif file_extention == 'yaml':
        print(generate_diff_yaml(file1_path, file2_path), end='')
    else:
        print('Incorrect file format', end='')


def generate_diff_json(file1_path, file2_path):
    
    try:
        data1 = json.load(open(file1_path))
        data2 = json.load(open(file2_path))
        
    except json.decoder.JSONDecodeError:
        return 'Incorrect JSON file uploaded'

    diff = json.dumps(_find_diff(data1, data2), indent=2)

    return diff.replace('"', '').replace(',', '')


def generate_diff_yaml(file1_path, file2_path):

    data1 = yaml.safe_load(open(file1_path))
    data2 = yaml.safe_load(open(file2_path))
    
    try:
        data1.keys()
        data2.keys()    
    except AttributeError:
        return 'Incorrect YAML file uploaded'

    diff = json.dumps(_find_diff(data1, data2), indent=2)

    return diff.replace('"', '').replace(',', '')