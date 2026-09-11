# ADR-005: LM Studio, immutable sources, and transactional ingestion

Date: 2026-09-11. Status: accepted; milestone 2.2 validated.

## Context

The user supplied LM Studio. Preflight verified Nomic embeddings (768 dimensions), Gemma generation, and Docker host connectivity.

## Decision

Use a small urllib model adapter and the supplied endpoint. Prefix Nomic inputs with search_document or search_query, validate response model/indexes/dimensions/finiteness, and reject model changes against the persisted index configuration. Batch at most eight chunks per request, capped at 100 chunks per document.

Preserve original bytes at a content-addressed MinIO key before embedding. Insert source revision metadata and all vectors in one PostgreSQL transaction. A revision is identified by source reference plus content digest; duplicate ingestion is a no-op. Identical bytes at different sources keep separate provenance. Failed embeddings or SQL leave no partially indexed document; a preserved but unindexed original may remain for retry.

Documents begin as drafts. Explicit approval publishes a revision and supersedes older approved revisions of the same source under a per-source transaction lock. All data routes require a bearer token. API credentials cannot administer PostgreSQL/MinIO; an explicit bootstrap command provisions schema and grants.

## Alternatives

An ORM, queue, and distributed transaction coordinator add overhead before this local slice needs them. Automatic draft publication would violate the review lifecycle. Using a generation model as an embedding fallback would corrupt similarity semantics.

## Tradeoffs

Exact pgvector search and per-request database connections suit the initial corpus. Model timeout is 120 seconds per batch. No automatic model retries or paid provider calls. Character windows do not guarantee token counts; input rejected by a model fails explicitly. MinIO content-addressed PUT retries write identical bytes; no object-lock retention policy is imposed.

## Consequences

Changing embedding model or chunking semantics needs a deliberate index/version migration. Administrative bootstrap remains separate from app startup. Local authenticated uploads are trusted lab inputs; hostile PDF resource isolation remains necessary before exposing uploads outside this machine. Source bodies and credentials are excluded from error logs. The endpoint is not production-ready.

References: [Nomic model instructions](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5), [psycopg transaction semantics](https://www.psycopg.org/psycopg3/docs/basic/usage.html).
