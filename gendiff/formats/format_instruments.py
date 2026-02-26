from pathlib import Path
from typing import Any, Dict


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


def get_file_extention(file1, file2):
    _, file1_extention = file1.split('.')
    _, file2_extention = file2.split('.')

    if file1_extention and file2_extention == 'json':
        return 'json'
    elif file1_extention and file2_extention == 'yaml' \
        or file1_extention and file2_extention == 'yml':
        return 'yaml'