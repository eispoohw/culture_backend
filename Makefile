PROJECT="Culture Backend"

run:
	python3 manage.py runserver

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

venv:
	source .venv/bin/activate

run_black:
	black . -l 150

run_isort:
	isort .

run_mypy:
	mypy .

cc: run_isort run_black

.PHONY: run

