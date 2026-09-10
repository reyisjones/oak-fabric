# ADR-001: Incremental foundation and first-run boundary

Date: 2026-09-10. Status: proposed for initial inspection.

## Context

The directive requests autonomous sequential work but explicitly ends the first execution after architecture and assignment preparation. Phase 1 lists Neo4j, while section 29 says to introduce it only after the first image/vector/RAG slice works.

## Decision

Complete the initial planning checkpoint before implementation. Prefer the narrower dependency order in section 29: run PostgreSQL/pgvector, MinIO, and FastAPI first; introduce Neo4j in Phase 4 after validating the image/RAG slice. Keep graph and vector responsibilities separate. Use Compose with persistent volumes and environment configuration. Use plain Python modules and synchronous workflows first. Canonical Markdown derives from reviewed source-backed models; generated HTML remains secondary.

## Alternatives

Start all listed services immediately; include Neo4j in the first Compose milestone; introduce a general agent framework or queue first. These add dependencies before their behavior can be validated against a working slice.

## Tradeoffs

Delayed graph features and synchronous throughput limits are acceptable for a local learning system. PostgreSQL/pgvector reduces initial operational overhead but couples metadata and vector capacity. MinIO introduces an additional service in exchange for source preservation and an object-storage interface. Later Neo4j adds operational and consistency costs in exchange for explicit traversals.

## Consequences

No empty future infrastructure or agent directories. No fabricated graph implementation. Record significant later choices as separate ADRs, including model/dimension selection, review publication semantics, graph synchronization, and any distributed processing. Do not claim the target architecture is implemented.
