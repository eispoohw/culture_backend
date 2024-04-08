PROJECT="Culture Backend"

run:
	python3 manage.py runserver

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

venv:
	source .venv/bin/activate

run_black:
	black .

run_isort:
	isort .

run_pylint:
	pylint .

run_mypy:
	mypy .

cc:
	run_black
	run_isort
	run_pylint

.PHONY: run