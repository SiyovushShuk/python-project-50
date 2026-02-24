from gendiff.scripts.gendiff import generate_diff


def test_base(capsys):

    generate_diff('file1.json', 'file2.json')

    result = capsys.readouterr()
    
    assert result.out == '''{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}
'''