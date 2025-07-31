.PHONY: mypy ruff mypy style style-check test lint all deps

package?=bot_service internal news_aggregator

all: deps test

style:
	python -m black $(package)
	python -m ruff check $(package)
	python -m isort $(package)

mypy:
	python -m mypy --enable-error-code ignore-without-code $(package)

style-check:
	python -m black --check --diff $(package)
	python -m ruff check $(package)  --fix
	python -m isort --check --diff $(package)

lint: style mypy

test: style lint
	python -m pytest .

deps:
	pip install -U mypy ruff black isort

freeze-test-deps:
	poetry export --only=dev > docker/test_requirements.txt

celery:
	celery -A levelarm.application.celery.app worker -B --concurrency=3 --loglevel=INFO
