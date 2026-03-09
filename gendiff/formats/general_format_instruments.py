from pathlib import Path
from typing import Any, Dict, Set


def _get_data_path(filename):
    try:
        return next(Path('.').rglob(filename)).resolve()
    except StopIteration:
        return None


def _is_line_changed(line_one, line_two):
    return line_one != line_two
    

def find_diff(first_file: Dict[str, Any], second_file: Dict[str, Any]
               ) -> Dict[str, Any]:
    
    line_diff: Dict = {}
    line_diff['first_file'] = first_file
    line_diff['second_file'] = second_file

    first_file_lines = first_file.keys()
    second_file_lines = second_file.keys()

    general_lines = first_file_lines & second_file_lines

    only_in_first = first_file_lines - second_file_lines
    only_in_second = second_file_lines - first_file_lines

    line_diff['only_in_first'] = only_in_first
    line_diff['only_in_second'] = only_in_second

    unchanged_lines: Set = set()
    changed_lines: Set = set()

    for name_line in general_lines:
        if _is_line_changed(first_file[name_line], second_file[name_line]):
            changed_lines.add(name_line)
        else:
            unchanged_lines.add(name_line)

    line_diff['unchanged_lines'] = unchanged_lines
    line_diff['changed_lines'] = changed_lines

    return line_diff
    

def get_file_extention(file1: str, file2: str) -> str | None:
    _, file1_extention = file1.split('.')
    _, file2_extention = file2.split('.')

    yaml_extentions = ['yaml', 'yml']

    if file1_extention == 'json' and file2_extention == 'json':
        return 'json'
    elif file1_extention in yaml_extentions \
        and file2_extention in yaml_extentions:
        return 'yaml'
    else:
        return None