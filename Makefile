install:
	uv sync

gendiff:
	uv run gendiff

build:
	uv build

package-install:
	uv tool install dist/*.whl

lint:
	uv run ruff check .

test-coverage:
	uv run pytest --cov=gendiff --cov-report xml

check:
	 test lint

test:
	 uv run pytest

.PHONY: install test lint selfcheck check build


