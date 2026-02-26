import argparse
from pathlib import Path

from gendiff.formats.gendiff import generate_diff


def _get_data_path(filename):
    try:
        return next(Path('.').rglob(filename)).resolve()
    except StopIteration:
        print(f'File {filename} not found!', end='')

        
def main():

    parser = argparse.ArgumentParser(prog='gendiff',
                                    description='Compares two configuration files and shows a difference.')  # noqa: E501

    parser.add_argument('first_file')
    parser.add_argument('second_file')

    parser.add_argument(
    '-f', '--format', metavar='FORMAT', help='set format of output')
    # print(json.dumps(data, indent=4))

    args = parser.parse_args()

    generate_diff(_get_data_path(args.first_file),
                _get_data_path(args.second_file))


if __name__ == "__main__":
    main()




