import json
from pathlib import Path
from typing import Any, Dict

import yaml

from gendiff.formats.general_format_instruments import (
    _get_data_path,
    add_indent,
    create_stylish_diff,
    find_diff,
    get_file_extention,
)


def create_stylish_format(data1: Dict[str, Any], data2: Dict[str, Any]) -> str:
    dict_diff = find_diff(data1, data2)
    formated_diff = add_indent(create_stylish_diff(*dict_diff.values()))
    return formated_diff


def load_json(file1_path: Path, file2_path: Path) -> None | str:
    
    try:
        data1 = json.load(open(file1_path))
        data2 = json.load(open(file2_path))
        
    except json.decoder.JSONDecodeError:
        return None

    return create_stylish_format(data1, data2)


def load_yaml(file1_path: Path, file2_path: Path) -> None | str:

    data1 = yaml.safe_load(open(file1_path))
    data2 = yaml.safe_load(open(file2_path))
    
    try:
        data1.keys()
        data2.keys()    
    except AttributeError:
        return None
    
    return create_stylish_format(data1, data2)
        

def generate_diff(file1: str, file2: str, format_name: str = 'stylish') -> None:

    if format_name != 'stylish':
        return

    file1_path = _get_data_path(file1)
    file2_path = _get_data_path(file2)

    if file1_path is None or file2_path is None:
        print('File not found!', end='')
        return
    
    file_extention = get_file_extention(file1, file2)

    if file_extention == 'json':
        formated_diff = load_json(file1_path, file2_path)
        if formated_diff is None:
            print('Incorrect JSON file uploaded', end='')
            return
        print(formated_diff, end='')
    elif file_extention == 'yaml':
        formated_diff = load_yaml(file1_path, file2_path)
        if formated_diff is None:
            print('Incorrect YAML file uploaded', end='')
            return
        print(formated_diff, end='')
    else:
        print('Incorrect file format or loaded files with different extentions',
               end='')

    
    
