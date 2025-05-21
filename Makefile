format:
	pre-commit run --all-files

run:
	poetry run python3 main.py

test:
	poetry run pytest -vvv tests.py
