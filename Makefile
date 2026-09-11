PYTHON ?= .venv/bin/python

.PHONY: install test run validate-docs
install:
	$(PYTHON) -m pip install -r requirements-dev.txt

test:
	$(PYTHON) -m pytest tests/unit -q

run:
	$(PYTHON) -m uvicorn src.api.main:create_app --factory --host 127.0.0.1 --port 8000

validate-docs:
	$(PYTHON) docs/validate.py

.PHONY: up down
up:
	docker compose up --build --wait

down:
	docker compose down
