from typing import Any, Dict, List, Set
from gendiff.formats.general_format_instruments import find_diff, _sort_logic
import json

def add_removed_lines(file, name_file_lines):
    removed = []
    for name_line in name_file_lines:
        removed.append(name_line)
    removed.sort()
    return removed

def add_added_lines(file, name_file_lines):
    added = []
    for name_line in name_file_lines:
        added.append(name_line)
    added.sort()
    return added

def format_children_diff(first_file, second_file, parent_line, parent_name_line):
    children_diff = find_diff(first_file[parent_name_line], second_file[parent_name_line])
    parent_line = add_updated_lines(first_file[parent_name_line], second_file[parent_name_line], children_diff['changed_lines'])
    parent_line['removed'] = add_removed_lines(first_file[parent_name_line], children_diff['only_in_first'])
    parent_line['added'] = add_added_lines(second_file[parent_name_line], children_diff['only_in_second'])
    parent_line = {k: v for k, v in parent_line.items() if v}

def add_updated_lines(first_file, second_file, name_file_lines):
    updated = {}
    for name_line in name_file_lines:
        updated[name_line] = {
            'new_value': [],
            'old_value': []
        }
        if isinstance(first_file[name_line], dict) and isinstance(second_file[name_line], dict):
            children_diff = find_diff(first_file[name_line], second_file[name_line])
            updated[name_line] = add_updated_lines(first_file[name_line], second_file[name_line], children_diff['changed_lines'])
            updated[name_line]['removed'] = add_removed_lines(first_file[name_line], children_diff['only_in_first'])
            updated[name_line]['added'] = add_added_lines(second_file[name_line], children_diff['only_in_second'])
            updated[name_line] = {k: v for k, v in updated[name_line].items() if v}
            continue       
        updated[name_line]['old_value'].append(first_file[name_line])
        updated[name_line]['new_value'].append(second_file[name_line])
        updated[name_line] = {k: v for k, v in updated[name_line].items() if v}
    updated_keys = sorted(updated)
    sorted_updated_elements = {key: updated[key] for key in updated_keys}
    return sorted_updated_elements

def format_data_to_json(
        first_file: Dict[str, Any],
        second_file: Dict[str, Any],
        only_in_first: Set[str],
        only_in_second: Set[str],
        unchanged_lines: Set[str],
        changed_lines: Set[str],
        /
    ) -> Dict[str, Any]:
    diff = {}

    diff['removed'] = add_removed_lines(first_file, only_in_first)
    diff['added'] = add_added_lines(second_file, only_in_second)
    diff['updated'] = add_updated_lines(first_file, second_file, changed_lines)

    return json.dumps(diff, indent=4)


def create_json_format(data1: Dict[str, Any], data2: Dict[str, Any]) -> str:
    diff = find_diff(data1, data2)
    formated_json = format_data_to_json(*diff.values())
    return formated_json