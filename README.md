# Open Architecture Knowledge Fabric

A local architecture knowledge laboratory: preserve sources, create reviewable knowledge, and retrieve cited evidence.

Implemented: Docker foundation, authenticated Markdown/PDF ingestion, original-byte preservation, 768-dimensional Nomic embeddings, draft review/approval, vector search, and source-quoted RAG through LM Studio. See [project status](docs/STATUS.md) for validation gates and pending work. Image analysis, Neo4j, GraphRAG, and POC generation are not implemented yet.

## Setup

1. Use Python 3.14 and Docker Desktop. Start LM Studio at localhost:1234 with `text-embedding-nomic-embed-text-v1.5` and `google/gemma-4-e4b` available.
2. Copy `.env.example` to `.env` only if no `.env` exists. Fill the five blank secret fields with distinct random values. Existing workspace secrets are already configured; do not overwrite them. Keep `.env` private and out of Git.
3. Run:

```sh
python3 -m venv .venv
make install
make test
make up
make bootstrap
```

`make bootstrap` applies the additive document migration and limited storage accounts; it works with existing volumes. API liveness is at localhost:8000/health; MinIO console is at localhost:9001. PostgreSQL and MinIO S3 remain internal. The container connects to LM Studio at host.docker.internal:1234/v1.

`make down` preserves named volumes. Do not use `down -v` unless intentionally deleting project data. Check Compose without printing credentials using `docker compose config --quiet`. `make run` is also available for health-only local development; full ingestion uses the Compose environment.

## Ingest, review, approve, query

Export FABRIC_API_KEY from your private configuration into the current shell before running these requests. The API accepts raw Markdown/PDF bytes, not multipart form data.

```sh
curl --fail -H "Authorization: Bearer $FABRIC_API_KEY" \
  --data-binary @tests/fixtures/storage-guide.md \
  'http://localhost:8000/ingest/document?source=tests/fixtures/storage-guide.md'
```

The result includes an entry `id`. Inspect `GET /documents/<id>` with the same Authorization header, then explicitly publish it using `POST /documents/<id>/approve`. Drafts are not searchable. A new source revision remains draft until approved, then supersedes the previous approved revision.

```sh
curl --fail -H "Authorization: Bearer $FABRIC_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"question":"Where are original architecture sources preserved?","top_k":5}' \
  http://localhost:8000/rag/query
```

`POST /search` accepts the same JSON and returns scored source chunks. Answers use exact quotations and structured citations; unsupported questions abstain. This first format prioritizes inspectable evidence over narrative summaries.

## Validate

`make evaluate` ingests the controlled fixture, checks deduplication/source-byte equality and rollback under faults, explicitly approves the test fixture, and evaluates known-source questions plus abstention. It requires real running storage and models; test fixture records remain inspectable. `make validate-docs` checks documentation links and tracking fields.

Evidence lives under [logs](logs/build/README.md), with [issue records](logs/issues/ISSUES.md), [current architecture](docs/architecture/current.md), [roadmap](docs/ROADMAP.md), and [learning assignments](docs/learning/progress.md).

This is a single-machine authenticated lab. PDF OCR, public-facing resource isolation/TLS, model migrations, and broader answer-quality evaluation remain pending. See architecture ADRs for design tradeoffs. Docker Desktop credential-helper failures observed during development and the temporary configuration workaround are recorded in the issue log; user Docker settings were not changed.
