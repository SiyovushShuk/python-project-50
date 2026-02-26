from pathlib import Path

from gendiff.formats.gendiff import generate_diff
from gendiff.scripts.gendiff import _get_data_path


def test_base(capsys):

    generate_diff(_get_data_path('file1.json'), _get_data_path('file2.json'))

    result = capsys.readouterr()

    correct = Path(__file__).parent / "test_data" / 'correct.txt'

    assert result.out == open(correct, 'r', encoding='utf-8').read()


def test_empty(capsys):

    generate_diff(_get_data_path('file1.json'), _get_data_path('empty.json'))

    result = capsys.readouterr()

    correct = Path(__file__).parent / "test_data" / 'empty_correct.txt'

    assert result.out == open(correct, 'r', encoding='utf-8').read()


def test_error_file(capsys):
    
    generate_diff(_get_data_path('file1.json'), _get_data_path('error.json'))

    result = capsys.readouterr()

    assert result.out == 'Incorrect JSON file uploaded'


def test_reverse(capsys):

    generate_diff(_get_data_path('file2.json'), _get_data_path('file1.json'))

    result = capsys.readouterr()

    correct = Path(__file__).parent / "test_data" / 'correct_reverse.txt'

    assert result.out == open(correct, 'r', encoding='utf-8').read()


def test_missing_file(capsys):
    
    generate_diff(_get_data_path('missing.json'), _get_data_path('file2.json'))

    result = capsys.readouterr()

    assert result.out == 'File missing.json not found!'