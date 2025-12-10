format:
	pre-commit run --all-files


run:
	poetry run python3 main.py


test:
	poetry run pytest -vvv tests.py


env:
	poetry env use 3.14
	poetry install --with dev --no-root
	poetry run pre-commit install
