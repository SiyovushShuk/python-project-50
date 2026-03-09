from pathlib import Path

from gendiff.formats.gendiff import generate_diff


def test_base(capsys):

    generate_diff('file1.json', 'file2.json')

    result = capsys.readouterr()

    correct = Path(__file__).parent / "test_data" / 'correct.txt'

    assert result.out == open(correct, 'r', encoding='utf-8').read()


def test_empty(capsys):

    generate_diff('file1.json', 'empty.json')

    result = capsys.readouterr()

    correct = Path(__file__).parent / "test_data" / 'empty_correct.txt'

    assert result.out == open(correct, 'r', encoding='utf-8').read()


def test_error_file(capsys):
    
    generate_diff('file1.json', 'error.json')

    result = capsys.readouterr()

    assert result.out == 'Incorrect JSON file uploaded'


def test_reverse(capsys):

    generate_diff('file2.json', 'file1.json')

    result = capsys.readouterr()

    correct = Path(__file__).parent / "test_data" / 'correct_reverse.txt'

    assert result.out == open(correct, 'r', encoding='utf-8').read()


def test_missing_file(capsys):
    
    generate_diff('missing.json', 'file2.json')

    result = capsys.readouterr()

    assert result.out == 'File not found!'


def test_base_yaml(capsys):

    generate_diff('file1.yaml', 'file2.yaml')

    result = capsys.readouterr()

    correct = Path(__file__).parent / "test_data" / 'correct.txt'

    assert result.out == open(correct, 'r', encoding='utf-8').read()


def test_missing_yaml(capsys):
    
    generate_diff('missing.yml', 'file2.yaml')

    result = capsys.readouterr()

    assert result.out == 'Incorrect YAML file uploaded'


def test_base_yml(capsys):

    generate_diff('file1.yaml', 'file3.yml')

    result = capsys.readouterr()

    correct = Path(__file__).parent / "test_data" / 'correct.txt'

    assert result.out == open(correct, 'r', encoding='utf-8').read()


def test_difficult_json(capsys):

    generate_diff('difficult_file1.json', 'difficult_file2.json')

    result = capsys.readouterr()

    correct = Path(__file__).parent / "test_data" / 'correct_difficult_data.txt'

    assert result.out == open(correct, 'r', encoding='utf-8').read()


def test_different_file_extentions(capsys):
    generate_diff('file1.json', 'file2.yaml')

    result = capsys.readouterr()

    correct = "Incorrect file format or loaded files with different extentions"

    assert result.out == correct


def test_difficult_yaml(capsys):

    generate_diff('difficult_file1.yml', 'difficult_file2.yaml')

    result = capsys.readouterr()

    correct = Path(__file__).parent / "test_data" / 'correct_difficult_data.txt'

    assert result.out == open(correct, 'r', encoding='utf-8').read()


def test_difficult_json_plain(capsys):

    generate_diff('difficult_file1.json', 'difficult_file2.json', 'plain')

    result = capsys.readouterr()

    correct = Path(__file__).parent / "test_data" / 'correct_difficult_plain_data.txt'  # noqa: E501

    assert result.out == open(correct, 'r', encoding='utf-8').read()


def test_difficult_yaml_plain(capsys):

    generate_diff('difficult_file1.yml', 'difficult_file2.yaml', 'plain')

    result = capsys.readouterr()

    correct = Path(__file__).parent / "test_data" / 'correct_difficult_plain_data.txt'  # noqa: E501

    assert result.out == open(correct, 'r', encoding='utf-8').read()


def test_difficult_different_plain(capsys):

    generate_diff('difficult_file1.json', 'difficult_file2.yaml', 'plain')

    result = capsys.readouterr()

    correct = "Incorrect file format or loaded files with different extentions"

    assert result.out == correct


def test_json_format_json(capsys):

    generate_diff('file1.json', 'file2.json', 'json')

    result = capsys.readouterr()

    correct = Path(__file__).parent / "test_data" / 'correct_json_format.txt'

    assert result.out == open(correct, 'r', encoding='utf-8').read()


def test_yaml_format_json(capsys):

    generate_diff('file1.yaml', 'file2.yaml', 'json')

    result = capsys.readouterr()

    correct = Path(__file__).parent / "test_data" / 'correct_json_format.txt'

    assert result.out == open(correct, 'r', encoding='utf-8').read()


def test_difficult_format_json(capsys):

    generate_diff('difficult_file1.json', 'difficult_file2.json', 'json')

    result = capsys.readouterr()

    correct = Path(__file__).parent / "test_data" / 'correct_difficult_format_json.txt'  # noqa: E501

    assert result.out == open(correct, 'r', encoding='utf-8').read()