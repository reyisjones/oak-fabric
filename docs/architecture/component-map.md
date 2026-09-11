# Component map

Foundation, document ingestion, review/approval, embeddings, and source-grounded RAG are validated. Image and graph capabilities remain pending.

| Component | Responsibility | Technology | Dependencies | Phase | Status |
| --- | --- | --- | --- | --- | --- |
| Local runtime | Reproducible services and volumes | Docker Compose | Docker daemon | 1 | Validated |
| API | Health, bounded ingestion and queries | FastAPI / Python | Configuration and stores | 1 | Validated |
| Metadata and vector index | Provenance, lifecycle, similarity | PostgreSQL / pgvector | Persistent volume | 1–2 | Validated for documents |
| Original storage | Immutable source bytes | MinIO | Persistent volume | 1 | Validated |
| Document processing | Markdown/PDF extraction, chunks | Python | Source storage | 2 | Validated |
| Model adapter | Embedding and text/vision inference | LM Studio compatible HTTP API | Configured models | 2–3 | Text/embeddings validated; vision pending |
| RAG | Evidence retrieval and cited answers | Python | pgvector and model adapter | 2 | Validated |
| Image workflow | Image to validated model and documents | Vision model / Python | RAG, source preservation | 3 | Pending |
| Review workflow | Draft correction and explicit approval | Metadata state / Markdown | Ingestion | 2–3 | Document approval validated; image correction pending |
| Knowledge graph | Entities and explicit relationships | Neo4j | Validated image/RAG slice | 4 | Deferred |
| GraphRAG | Fuse graph and vector evidence | Python | Neo4j / RAG | 5 | Pending |
| Agents | Controlled specialized operations | Python functions | Validated retrieval and rendering | 6 | Pending |
| Encyclopedia | Cross-linked knowledge and HTML | Markdown / Mermaid / HTML | Approved models | 7 | Pending |
| POC generator | Generate reviewable executable templates | Python / Compose | Approved architecture | 8 | Pending |
| Data platform | Analytics, tables, scheduling, events | DuckDB / Iceberg / Airflow / Spark / Kafka | Measured need | 9 | Conditional |
| Observability | Traces, metrics, dashboards | OpenTelemetry / Prometheus / Grafana | Working services | 10 | Pending |
| Portable deployment | Cluster packaging | Kubernetes / Helm | Stable Compose | 11 | Pending |
| Optional tools | Connectors, experiments, notebooks, BI | Airbyte / MLflow / JupyterLab / Superset | Demonstrated use case | Later | Conditional |
