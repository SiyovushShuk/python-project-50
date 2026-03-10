import json
from pathlib import Path

import yaml

from gendiff.formats.general_format_instruments import (
    _get_data_path,
    get_file_extention,
)
from gendiff.formats.json import create_json_format
from gendiff.formats.plain import create_plain_format
from gendiff.formats.stylish import create_stylish_format


def load_json(
            first_file_path: Path,
            second_file_path: Path,
            format_name
        ) -> None | str:
    
    try:
        first_file = json.load(open(first_file_path))
        second_file = json.load(open(second_file_path))
        
    except json.decoder.JSONDecodeError:
        return None

    if format_name == 'plain':
        return create_plain_format(first_file, second_file)
    elif format_name == 'stylish':
        return create_stylish_format(first_file, second_file)
    elif format_name == 'json':
        return create_json_format(first_file, second_file)
    else:
        return 'Incorrect format'


def load_yaml(
            first_file_path: Path,
            second_file_path: Path,
            format_name
        ) -> None | str:

    first_file_data = yaml.safe_load(open(first_file_path))
    second_file_data = yaml.safe_load(open(second_file_path))
    
    try:
        first_file_data.keys()
        second_file_data.keys()    
    except AttributeError:
        return None
    
    if format_name == 'plain':
        return create_plain_format(first_file_data, second_file_data)
    elif format_name == 'stylish':
        return create_stylish_format(first_file_data, second_file_data)
    elif format_name == 'json':
        return create_json_format(first_file_data, second_file_data)
    else:
        return 'Incorrect format'
        

def generate_diff(
            first_file_name: str,
            second_file_name: str,
            format_name: str = 'stylish'
        ) -> None:

    first_file_path = _get_data_path(first_file_name)
    second_file_path = _get_data_path(second_file_name)

    if first_file_path is None or second_file_path is None:
        print('File not found!', end='')
        return
    
    file_extention = get_file_extention(first_file_name, second_file_name)

    if file_extention == 'json':

        formated_diff = load_json(
                        first_file_path,
                        second_file_path,
                        format_name)
        
        if formated_diff is None:
            print('Incorrect JSON file uploaded', end='')
            return
        
        formated_diff = formated_diff + '\n'
        print(formated_diff, end='')
        return formated_diff

    elif file_extention == 'yaml':
        formated_diff = load_yaml(
                        first_file_path,
                        second_file_path,
                        format_name)
        
        if formated_diff is None:
            print('Incorrect YAML file uploaded', end='')
            return
        
        formated_diff = formated_diff + '\n'
        print(formated_diff, end='')
        return formated_diff

    else:
        print('Incorrect file format or loaded files with different extentions',
               end='')

    
    
