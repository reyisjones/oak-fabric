# Current implementation

Milestone 1.1 provides a local FastAPI application with GET /health, an application factory, environment validation, and nine unit tests. There is no ingestion or storage integration yet.

- src/api/main.py defines the HTTP contract and development documentation exposure.
- src/common/config.py validates APP_ENV at application startup.
- requirements.txt pins runtime dependencies; requirements-dev.txt adds pinned test dependencies.
- Makefile provides install, test, run, and documentation validation commands.

The endpoint reports process liveness only. Python 3.14 local execution was tested. See [test evidence](../../logs/validation/phase-1.1-tests.txt) and [live response](../../logs/validation/phase-1.1-http.json). The [vision](vision.md) describes future capabilities.

## Validated Docker foundation

Compose runs the API, PostgreSQL 17/pgvector 0.8.6, and MinIO with persistent named volumes. All health checks pass. A real vector and object survived storage restart. The API remains independent of storage until document ingestion is implemented. See [ADR-003](../decisions/ADR-003-compose-storage.md) and [container logs](../../logs/runtime/phase-1.2-containers.txt).

## Document extraction

Milestone 2.1 adds `src/extraction/documents.py`: Markdown/PDF bytes become immutable document/section records with SHA-256 identity, source, title, UTC timestamp, and PDF page numbers. Invalid/empty/encrypted/oversized documents fail explicitly. There is no upload endpoint yet. [ADR-004](../decisions/ADR-004-document-extraction.md) records limitations. Twenty-two tests pass in [validation evidence](../../logs/validation/phase-2.1-tests.txt).

## Chunking under milestone 2.2

`src/chunking/text.py` creates deterministic overlapping character windows within each extracted section/page. Every chunk includes required provenance and empty technology/architecture/tag lists until evidence supports enrichment. Stable IDs include source identity and offsets. No embeddings or semantic retrieval are implemented yet. Storage currently contains only dedicated validation probes, not indexed documents.
