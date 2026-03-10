from typing import Any, Dict, List, Set

from gendiff.formats.general_format_instruments import find_diff


def format_complex_str_value(value: Any) -> str:
    if isinstance(value, dict):
        return '[complex value]'
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return 'null'
    if isinstance(value, str):
        return f"'{value}'"
    return str(value)


def create_parent_property(parent_property: str, key: str) -> str:
    if parent_property == '':
        return key
    return f'{parent_property}.{key}'


def create_added_line(
        file: Dict[str, Any],
        keys: List[str], lines: List[str],
        parent_property: str = ''
    ) -> None:

    for key in keys:
        value = format_complex_str_value(file[key])
        property_path = create_parent_property(parent_property, key)
        lines.append(f"Property '{property_path}' was added with value: {value}")  # noqa: E501


def create_removed_line(
        keys: List[str], lines: List[str],
        parent_property: str = ''
    ) -> None:

    for key in keys:
        property_path = create_parent_property(parent_property, key)
        lines.append(f"Property '{property_path}' was removed")


def create_update_line(
        file1: Dict[str, Any],
        file2: Dict[str, Any],
        keys: List[str],
        lines, parent_property: str = ''
    ) -> None:

    for key in keys:
        property_path = create_parent_property(parent_property, key)
        first_value = file1[key]
        second_value = file2[key]
        if isinstance(file1[key], dict) and isinstance(file2[key], dict):
            child_diff = find_diff(file1[key], file2[key])
            create_added_line(file2[key],
                                child_diff['only_in_second'],
                                lines, property_path
                            )
            create_removed_line(child_diff['only_in_first'],
                                lines, property_path
                            )
            create_update_line(file1[key],
                                file2[key],
                                child_diff['changed_lines'],
                                lines, property_path
                            )
            continue
        elif isinstance(file1[key], dict):
            first_value = '[complex value]'
            second_value = format_complex_str_value(file2[key])
        elif isinstance(file2[key], dict):
            first_value = format_complex_str_value(file1[key])
            second_value = '[complex value]'
        else:
            first_value = format_complex_str_value(file1[key])
            second_value = format_complex_str_value(file2[key])
        lines.append(f"Property '{property_path}' was updated. From {first_value} to {second_value}")  # noqa: E501


def create_plain_diff(first_file: Dict[str, Any],
        second_file: Dict[str, Any],
        only_in_first: Set[str],
        only_in_second: Set[str],
        unchanged_lines: Set[str],
        changed_lines: Set[str],
        /
        ) -> str:
    
    lines: List[str] = []

    create_added_line(second_file, only_in_second, lines)
    create_removed_line(only_in_first, lines)
    create_update_line(first_file, second_file, changed_lines, lines)
    
    lines.sort()

    result = '\n'.join(lines).replace(
                                        'None',
                                        'null'
                                        ).replace(
                                            'True',
                                            'true').replace(
                                                    'False',
                                                    'false')
    return result


def create_plain_format(
            first_data: Dict[str, Any],
            second_data: Dict[str, Any]
        ) -> str:
    
    dict_diff = find_diff(first_data, second_data)
    formated_diff = create_plain_diff(*dict_diff.values())
    return formated_diff