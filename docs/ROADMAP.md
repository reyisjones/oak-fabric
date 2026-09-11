# Sequential roadmap

Updated: 2026-09-11. Complete and validate each milestone before the next. Conditional additions require a documented workload need.

| ID | Status | Deliverable | Required completion evidence |
| --- | --- | --- | --- |
| 0 | Complete | Assessment, inventory, architecture, tracking, first assignment | Documentation validator and artifact inventory |
| 1.1 | Complete | Configuration, pinned dependencies, minimal health API | Unit tests and live health response |
| 1.2 | Complete | Compose API, PostgreSQL/pgvector, MinIO and volumes | Healthy services, vector/object round-trips, restart persistence |
| 2.1 | Complete | Markdown/PDF extraction and provenance | Text/page fixtures, malformed/oversized input rejection |
| 2.2 | Complete | Chunking, embeddings and pgvector ingestion | Real Nomic vectors, source-byte equality, duplicate no-op, rollback fault tests |
| 2.3 | Complete | Retrieval and cited RAG | Expected sources and complete storage facts; exact passage support; unsupported-question abstention |
| 3.1 | Pending source image | Preserve image and structured analysis | Real diagram, checksum unchanged, component/relationship accuracy and uncertainty review |
| 3.2 | Pending | Markdown/Mermaid generation and approval | Required files, Mermaid parse, valid links, draft exclusion |
| 3.3 | Pending | First image-to-cited-answer slice | Image → JSON → documentation → metadata/vector → expected cited answer |
| 4.1 | Pending | Neo4j schema and ingestion | Real graph round-trip, idempotency, dangling relationship rejection |
| 4.2 | Pending | Bounded graph queries | Expected paths and entity extraction evaluation |
| 5 | Pending | GraphRAG fusion | Source-preserving context and traversal/faithfulness evaluations |
| 6 | Pending | Controlled specialized workflows | Tool boundaries, failures/retries, external research only on request |
| 7 | Pending | Encyclopedia, cross-links and HTML | Approved entry generation, link/duplicate checks, visual inspection |
| 8 | Pending | POC generator | Generated project builds, starts and passes tests in isolation |
| 9 | Conditional | Data platform additions | ADR and measured workload per tool; integration validation |
| 10 | Pending | OpenTelemetry, Prometheus and Grafana | Correlated trace, scraped metric, dashboard and secret-redaction checks |
| 11 | Pending | Kubernetes and Helm | Manifest/chart checks and actual test-cluster deployment |

Phase 2 evidence: [57 unit tests](../logs/validation/phase-2-final-unit.txt), [real ingestion](../logs/validation/phase-2.2-ingestion.txt), [rollback faults](../logs/validation/phase-2.2-failure-recovery.txt), and [live RAG evaluation](../logs/validation/phase-2.3-passage-evaluation.jsonl). The initial three-case RAG corpus establishes only a baseline; it does not demonstrate general answer quality.

For every issue: capture → identify root cause → document → one focused fix → rerun affected validation → record outcome. Mocks do not prove service integration. The Neo4j ordering conflict is resolved in [ADR-001](decisions/ADR-001-incremental-foundation.md). Optional Azure deployment is outside the initial core scope.
