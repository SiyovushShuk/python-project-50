import json
from pathlib import Path

import yaml

from gendiff.formats.general_format_instruments import (
    _get_data_path,
    get_file_extention,
)
from gendiff.formats.plain import create_plain_format
from gendiff.formats.stylish import create_stylish_format


def load_json(file1_path: Path, file2_path: Path, format_name) -> None | str:
    
    try:
        data1 = json.load(open(file1_path))
        data2 = json.load(open(file2_path))
        
    except json.decoder.JSONDecodeError:
        return None

    if format_name == 'plain':
        return create_plain_format(data1, data2)
    elif format_name == 'stylish':
        return create_stylish_format(data1, data2)
    else:
        return 'Incorrect format'


def load_yaml(file1_path: Path, file2_path: Path, format_name) -> None | str:

    data1 = yaml.safe_load(open(file1_path))
    data2 = yaml.safe_load(open(file2_path))
    
    try:
        data1.keys()
        data2.keys()    
    except AttributeError:
        return None
    
    if format_name == 'plain':
        return create_plain_format(data1, data2)
    elif format_name == 'stylish':
        return create_stylish_format(data1, data2)
    else:
        return 'Incorrect format'
        

def generate_diff(file1: str, file2: str, format_name: str = 'stylish') -> None:

    file1_path = _get_data_path(file1)
    file2_path = _get_data_path(file2)

    if file1_path is None or file2_path is None:
        print('File not found!', end='')
        return
    
    file_extention = get_file_extention(file1, file2)

    if file_extention == 'json':
        formated_diff = load_json(file1_path, file2_path, format_name)
        if formated_diff is None:
            print('Incorrect JSON file uploaded', end='')
            return
        print(formated_diff, end='')
    elif file_extention == 'yaml':
        formated_diff = load_yaml(file1_path, file2_path, format_name)
        if formated_diff is None:
            print('Incorrect YAML file uploaded', end='')
            return
        print(formated_diff, end='')
    else:
        print('Incorrect file format or loaded files with different extentions',
               end='')

    
    
