### Hexlet tests and linter status:
[![Actions Status](https://github.com/SiyovushShuk/python-project-50/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/SiyovushShuk/python-project-50/actions)
[![PythonCI](https://github.com/SiyovushShuk/python-project-50/actions/workflows/pythonci.yml/badge.svg)](https://github.com/SiyovushShuk/python-project-50/actions/workflows/pythonci.yml)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=SiyovushShuk_python-project-50&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=SiyovushShuk_python-project-50)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=SiyovushShuk_python-project-50&metric=coverage)](https://sonarcloud.io/summary/new_code?id=SiyovushShuk_python-project-50)

### Package description
This package show differences between two files in console. Formats: stylish (default format), plain and json.

Stylish format: in tree format show different between files where - is delete, + is add. 
Plain format: show what was deleted, added, or changed.
Json format: show diffrence in json format

### Recommended requiremnts

Python version 13.3

### Links

This project was built using these tools:

| Tool                                                                   | Description                                             |
|------------------------------------------------------------------------|---------------------------------------------------------|
| [uv](https://docs.astral.sh/uv/)                                       | "An extremely fast Python package and project manager, written in Rust" |
| [ruff](https://docs.astral.sh/ruff/)                                   | "An extremely fast Python linter and code formatter, written in Rust" |
| [pyyaml](https://pyyaml.org/)                                          | "A full-featured YAML processing framework for Python" |
| [Pytest](https://pytest.org)                                           | "A mature full-featured Python testing tool"            |

---

### Setup

```bash
make install
make build
make package-install
```
