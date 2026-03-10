from pathlib import Path
from typing import Any, Dict, List, Set

from gendiff.formats.general_format_instruments import find_diff


def _create_format_line(
            file: Path,
            lines: List[str],
            diff: Dict[str, Any],
            symbol: str
            ) -> None:
    
    for line in lines:
        if isinstance(file[line], dict):
            formatted__children_line = {}
            _create_format_line(file[line],
                                file[line].keys(),
                                formatted__children_line, ' ')
            diff[f'{symbol} {line}'] = formatted__children_line
            continue
        diff[f'{symbol} {line}'] = file[line]


def _sort_logic(item: str, sybmol_priority: str = '-'):
    name_line, _ = item

    first_symbol = name_line[0]

    clean_line = name_line.lstrip('+- ').strip()

    if sybmol_priority == '-':
        return clean_line, -ord(first_symbol)
    else:
        return clean_line, ord(first_symbol)


def create_stylish_diff(
        first_file: Dict[str, Any],
        second_file: Dict[str, Any],
        only_in_first: Set[str],
        only_in_second: Set[str],
        unchanged_lines: Set[str],
        changed_lines: Set[str],
        /
        ) -> Dict[str, Any]:
    
    formated_diff: Dict[str, Any] = {}

    _create_format_line(first_file, only_in_first, formated_diff, '-')
    _create_format_line(second_file, only_in_second, formated_diff, '+')
    _create_format_line(first_file, unchanged_lines, formated_diff, ' ')

    for line in changed_lines:

        if isinstance(first_file[line], dict) and \
            isinstance(second_file[line], dict):
            children_diff = find_diff(first_file[line], second_file[line])
            formated_children = create_stylish_diff(*children_diff.values())
            formated_diff[f'  {line}'] = formated_children
        elif isinstance(first_file[line], dict):
            formatted_children_line = {}
            _create_format_line(
                first_file[line],
                first_file[line].keys(),
                formatted_children_line, ' '
                )
            formated_diff[f'- {line}'] = formatted_children_line
            formated_diff[f'+ {line}'] = second_file[line]
        elif isinstance(second_file[line], dict):
            formatted_children_line = {}
            _create_format_line(
                second_file[line],
                second_file[line].keys(),
                formatted_children_line, ' '
                )
            formated_diff[f'- {line}'] = first_file[line]
            formated_diff[f'+ {line}'] = formatted_children_line
        else:
            formated_diff[f'- {line}'] = first_file[line]
            formated_diff[f'+ {line}'] = second_file[line]

    sorted_diff = dict(sorted(
        formated_diff.items(),
        key=lambda item: _sort_logic(item)
    ))

    return sorted_diff


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

    result = '\n'.join(formated_lines).replace(
                                        'None',
                                        'null'
                                        ).replace(
                                            'True',
                                            'true').replace(
                                                    'False',
                                                    'false')

    return result


def create_stylish_format(
                file_one_data: Dict[str, Any],
                file_two_data: Dict[str, Any]
                ) -> str:
    
    dict_diff = find_diff(file_one_data, file_two_data)
    formated_diff = add_indent(create_stylish_diff(*dict_diff.values()))
    return formated_diff