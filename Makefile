.PHONY: setup test lint format download explore

setup:
	pip install -r requirements-dev.txt

test:
	pytest tests/

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

download:
	python -m src.data.download

explore:
	python -m src.data.explore
