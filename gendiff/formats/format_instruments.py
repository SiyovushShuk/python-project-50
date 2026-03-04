from pathlib import Path
from typing import Any, Dict, List, Set


def _get_data_path(filename):
    try:
        return next(Path('.').rglob(filename)).resolve()
    except StopIteration:
        return None


def _is_line_changed(line_one, line_two):
    return line_one != line_two


def _create_format_line(file, lines, diff, symbol):
    for line in lines:
        if isinstance(file[line], dict):
            formatted_line = {}
            _create_format_line(file[line],
                                file[line].keys(),
                                formatted_line, ' ')
            diff[f'{symbol} {line}'] = formatted_line
            continue
        diff[f'{symbol} {line}'] = file[line]


def _sort_logic(item, sybmol_priority='-'):
    name_line, _ = item

    first_symbol = name_line[0]

    clean_line = name_line.lstrip('+- ').strip()

    if sybmol_priority == '-':
        return clean_line, -ord(first_symbol)
    else:
        return clean_line, ord(first_symbol)
    

def find_diff(first_file: Dict[str, Any], second_file: Dict[str, Any]
               ) -> Dict[str, Any]:
    
    diff: Dict = {}
    diff['first_file'] = first_file
    diff['second_file'] = second_file

    first_file_lines = first_file.keys()
    second_file_lines = second_file.keys()

    general_lines = first_file_lines & second_file_lines

    only_in_first = first_file_lines - second_file_lines
    only_in_second = second_file_lines - first_file_lines

    diff['only_in_first'] = only_in_first
    diff['only_in_second'] = only_in_second

    unchanged_lines: Set = set()
    changed_lines: Set = set()

    for name_line in general_lines:
        if _is_line_changed(first_file[name_line], second_file[name_line]):
            changed_lines.add(name_line)
        else:
            unchanged_lines.add(name_line)

    diff['unchanged_lines'] = unchanged_lines
    diff['changed_lines'] = changed_lines

    return diff
    

def create_stylish_diff(
        first_file: Dict[str, Any],
        second_file: Dict[str, Any],
        only_in_first: Set[str],
        only_in_second: Set[str],
        unchanged_lines: Set[str],
        changed_lines: Set[str],
        /
        ) -> Dict[str, Any]:
    sorted_diff_file: Dict = {}

    _create_format_line(first_file, only_in_first, sorted_diff_file, '-')
    _create_format_line(second_file, only_in_second, sorted_diff_file, '+')
    _create_format_line(first_file, unchanged_lines, sorted_diff_file, ' ')

    for line in changed_lines:

        if isinstance(first_file[line], dict) and \
            isinstance(second_file[line], dict):
            children_diff = find_diff(first_file[line], second_file[line])
            formated_children = create_stylish_diff(*children_diff.values())
            sorted_diff_file[f'  {line}'] = formated_children
        else:
            if isinstance(first_file[line], dict):
                formatted_line = {}
                _create_format_line(
                    first_file[line],
                    first_file[line].keys(),
                    formatted_line, ' '
                    )
                sorted_diff_file[f'- {line}'] = formatted_line
                sorted_diff_file[f'+ {line}'] = second_file[line]
                continue
            elif isinstance(second_file[line], dict):
                formatted_line = {}
                _create_format_line(
                    second_file[line],
                    second_file[line].keys(),
                    formatted_line, ' '
                    )
                sorted_diff_file[f'- {line}'] = first_file[line]
                sorted_diff_file[f'+ {line}'] = formatted_line
                continue
            sorted_diff_file[f'- {line}'] = first_file[line]
            sorted_diff_file[f'+ {line}'] = second_file[line]

    sorted_diff_file = dict(sorted(
        sorted_diff_file.items(),
        key=lambda item: _sort_logic(item)
    ))

    return sorted_diff_file


def add_indent(
        diff: Dict[str, Any],
        deep_level: int = 1,
        key_name: str = ''
    ) -> str:

    count_spaces = (4 * deep_level) - 2
    if deep_level - 1 == 0:
        begin_str = '{'
    else:
        begin_str = (((4 * (deep_level - 1)) - 2) * ' ') + f'{key_name}: ' + '{'
    indent = count_spaces * ' '

    formated_lines: List = [begin_str]
    
    keys = diff.keys()

    for key in keys:
        if isinstance(diff[key], dict):
            formated_lines.append(add_indent(diff[key], deep_level + 1, key))
            continue
        
        formated_lines.append(indent + key + f': {diff[key]}')
    formated_lines.append(((count_spaces - 2) * ' ') + '}')

    result = '\n'.join(formated_lines).replace('None',
                            'null').replace('True',
                                            'true').replace('False',
                                                            'false')

    return result


def get_file_extention(file1: str, file2: str) -> str | None:
    _, file1_extention = file1.split('.')
    _, file2_extention = file2.split('.')

    if file1_extention and file2_extention == 'json':
        return 'json'
    elif file1_extention and file2_extention == 'yaml' \
        or file1_extention and file2_extention == 'yml':
        return 'yaml'
    else:
        return None