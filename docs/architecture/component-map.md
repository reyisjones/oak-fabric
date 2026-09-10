# Component map

All implementation statuses below are pending or conditional. Only planning documentation exists.

| Component | Responsibility | Technology | Dependencies | Phase | Status |
| --- | --- | --- | --- | --- | --- |
| Local runtime | Reproducible services and volumes | Docker Compose | Docker daemon | 1 | Pending; daemon unavailable |
| API | Health, bounded ingestion and queries | FastAPI / Python | Configuration and stores | 1 | Pending |
| Metadata and vector index | Provenance, lifecycle, similarity | PostgreSQL / pgvector | Persistent volume | 1–2 | Pending |
| Original storage | Immutable source bytes | MinIO | Persistent volume | 1 | Pending |
| Document processing | Markdown/PDF extraction, chunks | Python | Source storage | 2 | Pending |
| Model adapter | Embedding and text/vision inference | Ollama or compatible HTTP API | Configured models | 2–3 | Pending |
| RAG | Evidence retrieval and cited answers | Python | pgvector and model adapter | 2 | Pending |
| Image workflow | Image to validated model and documents | Vision model / Python | RAG, source preservation | 3 | Pending |
| Review workflow | Draft correction and explicit approval | Metadata state / Markdown | Image workflow | 3 | Pending |
| Knowledge graph | Entities and explicit relationships | Neo4j | Validated image/RAG slice | 4 | Deferred |
| GraphRAG | Fuse graph and vector evidence | Python | Neo4j / RAG | 5 | Pending |
| Agents | Controlled specialized operations | Python functions | Validated retrieval and rendering | 6 | Pending |
| Encyclopedia | Cross-linked knowledge and HTML | Markdown / Mermaid / HTML | Approved models | 7 | Pending |
| POC generator | Generate reviewable executable templates | Python / Compose | Approved architecture | 8 | Pending |
| Data platform | Analytics, tables, scheduling, events | DuckDB / Iceberg / Airflow / Spark / Kafka | Measured need | 9 | Conditional |
| Observability | Traces, metrics, dashboards | OpenTelemetry / Prometheus / Grafana | Working services | 10 | Pending |
| Portable deployment | Cluster packaging | Kubernetes / Helm | Stable Compose | 11 | Pending |
| Optional tools | Connectors, experiments, notebooks, BI | Airbyte / MLflow / JupyterLab / Superset | Demonstrated use case | Later | Conditional |
