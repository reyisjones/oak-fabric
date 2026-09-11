# Open Architecture Knowledge Fabric

A local, open-source architecture knowledge laboratory. Preserve sources, turn them into reviewable structured knowledge, retrieve cited evidence, and eventually generate executable POCs.

**Current state:** milestone 1.1 validated: FastAPI health endpoint and environment configuration. Docker foundation is validated, including persistence round-trips. See [current implementation](docs/architecture/current.md).

Start with [project status](docs/STATUS.md), [assessment](docs/assessment.md), [target architecture](docs/architecture/vision.md), and [roadmap](docs/ROADMAP.md). The [component map](docs/architecture/component-map.md) distinguishes future capabilities from current implementation. [Learning progress](docs/learning/progress.md) contains the first inspection assignment.

Run `python3 docs/validate.py` to validate documentation links and required planning artifacts. This does not validate an application or containers. Evidence is saved in [validation logs](logs/validation/initial-review.txt). See [issues](logs/issues/ISSUES.md) for environment limitations.

## Run locally

```sh
python3 -m venv .venv
make install
make test
make run
```

In another terminal, run `curl --fail http://127.0.0.1:8000/health`. Expected response: `{"status":"ok","service":"oak-fabric"}`. APP_ENV accepts development (default), test, or production. Set it in the process environment; local execution does not automatically read .env. `/health` is liveness only.

## Docker foundation

Copy `.env.example` to `.env` only if `.env` does not already exist. Fill both blank password values with unique local secrets. Then run `make up`. The API binds to localhost:8000; MinIO console binds to localhost:9001. PostgreSQL and the MinIO S3 API are internal to Compose. `make down` stops the project while retaining named volumes; avoid `down -v` unless intentionally deleting all project data.

Configuration can be checked without printing secrets: `docker compose config --quiet`. Container startup and storage verification are tracked in [project status](docs/STATUS.md). The API currently has no storage integration, so its liveness does not imply storage readiness.

Markdown/PDF extraction and deterministic source-linked chunking are available as Python library functions in `src.extraction.documents` and `src.chunking.text`. Scanned PDFs require OCR, which is not implemented. Embeddings and RAG remain pending model configuration.

To verify storage persistence, generate a UUID with `python3 -c 'import uuid; print(uuid.uuid4())'`, run `python3 tests/integration/validate_storage.py write <uuid>`, restart only `postgres` and `minio`, wait with `docker compose up --wait`, and run the same script with `read <uuid>`. The probe uses its own table and bucket and retains its records for inspection.
