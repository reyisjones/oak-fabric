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

.PHONY: bootstrap evaluate
bootstrap:
	$(PYTHON) infrastructure/docker/bootstrap.py

evaluate:
	docker compose exec -T api mkdir -p /tmp/oak-evaluation
	docker compose cp tests/fixtures/storage-guide.md api:/tmp/oak-evaluation/storage-guide.md
	docker compose cp tests/evaluation/rag-cases.json api:/tmp/oak-evaluation/rag-cases.json
	docker compose exec -T api python - < tests/integration/validate_ingestion.py
	docker compose exec -T api python - < tests/integration/validate_ingestion_failures.py
	docker compose exec -T api python - < tests/evaluation/validate_rag.py
