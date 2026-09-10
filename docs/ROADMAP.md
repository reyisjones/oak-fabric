# Sequential roadmap

Complete and validate each milestone before the next. All implementation milestones are pending. Conditional additions require a documented use case; they are not prerequisites for the core platform.

| ID | Deliverable | Required completion evidence |
| --- | --- | --- |
| 0 | Assessment, inventory, architecture, tracking, first assignment | Passing documentation validator and reviewed artifact inventory |
| 1.1 | Configuration, pinned dependencies, minimal health API and tests | Unit tests and successful local health response |
| 1.2 | Compose API, PostgreSQL/pgvector, MinIO, volumes | Compose validation; all services healthy; extension query; object round-trip; restart persistence |
| 2.1 | Markdown/PDF extraction and provenance | Fixture tests including page references and malformed input |
| 2.2 | Chunking, embeddings and pgvector ingestion | Chunk metadata tests; real model/vector round-trip; repeat ingestion without duplication |
| 2.3 | Retrieval and cited RAG | Expected-source evaluation; unsupported questions abstain; citations resolve |
| 3.1 | Image preservation and structured analysis | Real image fixture, checksum unchanged, entity/relationship accuracy review, uncertainty labels |
| 3.2 | Markdown/Mermaid generation and approval | Required sections/files; Mermaid parse; valid links; draft excluded until explicit approval |
| 3.3 | First image-to-cited-answer slice | Image → JSON → documentation → metadata/vector → expected cited answer |
| 4.1 | Neo4j schema and graph ingestion | Real graph round-trip; idempotency; dangling relationship rejection |
| 4.2 | Bounded graph queries | Expected paths and entity extraction evaluation |
| 5 | GraphRAG fusion | Source-preserving context; graph traversal and faithfulness evaluations |
| 6 | Specialized controlled workflows | Tool boundaries, failure/retry and validation tests; external research only on request |
| 7 | Encyclopedia, cross-links, standalone HTML | Approved entry generation; link/duplicate checks; visual inspection |
| 8 | POC generator | Generated README, Compose, service, data, diagram, configuration, tests and tutorial; isolated build/start/test |
| 9 | Justified data platform additions | One ADR and measured workload per tool; corresponding integration test |
| 10 | OpenTelemetry, Prometheus, Grafana | Correlated trace; scraped metric; dashboard evidence; secret redaction |
| 11 | Kubernetes manifests and Helm | Manifest/schema and chart validation; deployment on a test cluster |

For every issue: capture error → identify root cause → document → apply one focused fix → rerun affected validation → record outcome. A failed required test blocks its milestone. Mocks alone do not prove service/model integration.

The Phase 1 Neo4j ordering conflict is resolved explicitly in [ADR-001](decisions/ADR-001-incremental-foundation.md). Optional Azure deployment is outside the initial core scope.
