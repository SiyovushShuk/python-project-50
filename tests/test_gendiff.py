from pathlib import Path

from gendiff.engine import generate_diff


def test_base():

    result = generate_diff('file1.json', 'file2.json')

    correct = Path(__file__).parent / "test_data" / 'correct.txt'

    assert result == open(correct, 'r', encoding='utf-8').read()


def test_empty():

    result = generate_diff('file1.json', 'empty.json')

    correct = Path(__file__).parent / "test_data" / 'empty_correct.txt'

    assert result == open(correct, 'r', encoding='utf-8').read()


def test_error_file(capsys):

    _ = generate_diff('file1.json', 'error.json')
    result = capsys.readouterr()

    assert result.out == 'Incorrect JSON file uploaded'


def test_reverse():

    result = generate_diff('file2.json', 'file1.json')

    correct = Path(__file__).parent / "test_data" / 'correct_reverse.txt'

    assert result == open(correct, 'r', encoding='utf-8').read()


def test_missing_file(capsys):
    
    _ = generate_diff('missing.json', 'file2.json')
    result = capsys.readouterr()

    assert result.out == 'File not found!'


def test_base_yaml():

    result = generate_diff('file1.yaml', 'file2.yaml')

    correct = Path(__file__).parent / "test_data" / 'correct.txt'

    assert result == open(correct, 'r', encoding='utf-8').read()


def test_missing_yaml(capsys):
    
    _ = generate_diff('missing.yml', 'file2.yaml')
    result = capsys.readouterr()

    assert result.out == 'Incorrect YAML file uploaded'


def test_base_yml():

    result = generate_diff('file1.yaml', 'file3.yml')

    correct = Path(__file__).parent / "test_data" / 'correct.txt'

    assert result == open(correct, 'r', encoding='utf-8').read()


def test_difficult_json():

    result = generate_diff('difficult_file1.json', 'difficult_file2.json')

    correct = Path(__file__).parent / "test_data" / 'correct_difficult_data.txt'

    assert result == open(correct, 'r', encoding='utf-8').read()


def test_different_file_extentions(capsys):
    
    _ = generate_diff('file1.json', 'file2.yaml')
    result = capsys.readouterr()

    correct = "Incorrect file format or loaded files with different extentions"

    assert result.out == correct


def test_difficult_yaml():

    result = generate_diff('difficult_file1.yml', 'difficult_file2.yaml')

    correct = Path(__file__).parent / "test_data" / 'correct_difficult_data.txt'

    assert result == open(correct, 'r', encoding='utf-8').read()


def test_difficult_json_plain():

    result = generate_diff('difficult_file1.json', 'difficult_file2.json', 'plain')  # noqa: E501

    correct = Path(__file__).parent / "test_data" / 'correct_difficult_plain_data.txt'  # noqa: E501

    assert result == open(correct, 'r', encoding='utf-8').read()


def test_difficult_yaml_plain():

    result = generate_diff('difficult_file1.yml', 'difficult_file2.yaml', 'plain')  # noqa: E501

    correct = Path(__file__).parent / "test_data" / 'correct_difficult_plain_data.txt'  # noqa: E501

    assert result == open(correct, 'r', encoding='utf-8').read()


def test_difficult_different_plain(capsys):

    _ = generate_diff('difficult_file1.json', 'difficult_file2.yaml', 'plain')  # noqa: E501

    result = capsys.readouterr()

    correct = "Incorrect file format or loaded files with different extentions"

    assert result.out == correct


def test_json_format_json():

    result = generate_diff('file1.json', 'file2.json', 'json')

    correct = Path(__file__).parent / "test_data" / 'correct_json_format.txt'

    assert result == open(correct, 'r', encoding='utf-8').read()


def test_yaml_format_json():

    result = generate_diff('file1.yaml', 'file2.yaml', 'json')

    correct = Path(__file__).parent / "test_data" / 'correct_json_format.txt'

    assert result == open(correct, 'r', encoding='utf-8').read()


def test_difficult_format_json():

    result = generate_diff('difficult_file1.json', 'difficult_file2.json', 'json')  # noqa: E501

    correct = Path(__file__).parent / "test_data" / 'correct_difficult_format_json.txt'  # noqa: E501

    assert result == open(correct, 'r', encoding='utf-8').read()


def test_yaml_plain():

    result = generate_diff('file1.yaml', 'file2.yaml', 'plain')

    correct = Path(__file__).parent / "test_data" / 'correct_plain_data.txt'  # noqa: E501

    assert result == open(correct, 'r', encoding='utf-8').read()


def test_json_plain():

    result = generate_diff('file1.json', 'file2.json', 'plain')

    correct = Path(__file__).parent / "test_data" / 'correct_plain_data.txt'  # noqa: E501

    assert result == open(correct, 'r', encoding='utf-8').read()