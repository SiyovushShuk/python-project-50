import json
import yaml
from typing import Any, Dict, Set, List
from gendiff.formats.format_instruments import (
    _get_data_path,
    get_file_extention,
    _find_diff
)


def generate_diff(file1, file2):
    
    file_extention = get_file_extention(file1, file2)

    file1_path = _get_data_path(file1)
    file2_path = _get_data_path(file2)

    if file1_path is None or file2_path is None:
        print('File not found!', end='')
        return

    if file_extention == 'json':
        print(stylish(generate_diff_json(file1_path, file2_path), 1, ''))
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

    return _find_diff(data1, data2)


def generate_diff_yaml(file1_path, file2_path):

    data1 = yaml.safe_load(open(file1_path))
    data2 = yaml.safe_load(open(file2_path))
    
    try:
        data1.keys()
        data2.keys()    
    except AttributeError:
        return 'Incorrect YAML file uploaded'

    diff = json.dumps(_find_diff(data1, data2), indent=4)

    return diff.replace('"', '').replace(',', '')


def stylish(diff: Dict[str, Any], deep_level: int, key_name):

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
            formated_lines.append(stylish(diff[key], deep_level + 1, key))
            continue
        
        formated_lines.append(indent + key + f': {diff[key]}')
    formated_lines.append(((count_spaces - 2) * ' ') + '}')

    return '\n'.join(formated_lines)
        
        


    
    
