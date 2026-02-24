import argparse
import json
from pathlib import Path
from typing import Any, Dict


def _get_data_path(filename):
    return Path(__file__).parent.parent / "data" / filename


def _find_diff(first_file: Dict[str, Any], second_file: Dict[str, Any]):

    first_file_lines: Dict = {}
    second_file_lines: Dict = {}

    for first_file_key in first_file:
        if first_file_key in second_file.keys():

            if first_file[first_file_key] == second_file[first_file_key]:
                first_file_lines[first_file_key] = first_file[first_file_key]
                second_file_lines[first_file_key] = second_file[first_file_key]
                continue

            first_file_lines[first_file_key] = first_file[first_file_key]
            second_file_lines[first_file_key] = second_file[first_file_key]

            continue

        first_file_lines[first_file_key] = first_file[first_file_key]

    first_file_lines = dict(sorted(first_file_lines.items()))
    second_file_lines = dict(sorted(second_file_lines.items()))

    missed_keys = sorted(second_file.keys() - first_file.keys())

    difference = _format_defferences(first_file_lines, second_file_lines,
                                     missed_keys, second_file)

    return difference


def _format_defferences(first_file_lines,
                        second_file_lines,
                        missed_keys,
                        second_file):
    difference = {}

    for key in first_file_lines:

        if second_file_lines.get(key) is None:
            difference[f'- {key}'] = first_file_lines[key]
            continue

        if first_file_lines[key] == second_file_lines[key]:
            difference[f'  {key}'] = first_file_lines[key]
            continue

        difference[f'- {key}'] = first_file_lines[key]
        difference[f'+ {key}'] = second_file_lines[key]

    for key in missed_keys:
        difference[f'+ {key}'] = second_file[key]

    return difference
        

def generate_diff(file1, file2):
    data1 = json.load(open(_get_data_path(file1)))

    data2 = json.load(open(_get_data_path(file2)))
    diff = json.dumps(_find_diff(data1, data2), indent=2)

    print(diff.replace('"', '').replace(',', ''))


def main():

    parser = argparse.ArgumentParser(prog='gendiff',
                                    description='Compares two configuration files and shows a difference.')  # noqa: E501

    parser.add_argument('first_file')
    parser.add_argument('second_file')

    parser.add_argument(
    '-f', '--format', metavar='FORMAT', help='set format of output')
    # print(json.dumps(data, indent=4))

    args = parser.parse_args()

    generate_diff(args.first_file, args.second_file)


if __name__ == "__main__":
    main()




