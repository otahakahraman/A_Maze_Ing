.PHONY: install run debug clean lint lint-strict

install:
	python -m pip install -e . flake8 mypy

run:
	python a_maze_ing.py config.txt

debug:
	python -m pdb a_maze_ing.py config.txt

clean:
	find . -type d \( -name __pycache__ -o -name .mypy_cache -o -name .pytest_cache \) -prune -exec rm -rf {} +
	rm -rf build dist *.egg-info

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
