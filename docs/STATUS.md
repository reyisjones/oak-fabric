# Project status

Updated: 2026-09-11.

| Field | Latest state |
| --- | --- |
| Current Phase | Phase 2 — Document RAG |
| Last Completed Task | Milestone 2.1: Markdown/PDF extraction with source/page provenance |
| Current Task | Milestone 2.2: chunking validated; model/vector ingestion integration pending |
| Pending Tasks | Complete 2.2; milestones 2.3–11, with conditional tools justified individually |
| Open Issues | DEPS-001 test deprecations; OPS-001 local storage limitations |
| Recent Fixes | Docker startup, credential-helper workaround, package networking, C# heading preservation |
| Architecture Decisions | ADR-001 through ADR-004; synchronous processing and explicit provenance |
| Next Recommended Action | Integrate LM Studio embeddings (768 dimensions), then validate persistent vector ingestion |

## Completed

Initial planning; Git master initialization and first push; milestone 1.1 API and configuration; milestone 1.2 healthy Compose containers and persistent PostgreSQL vector/MinIO round-trips; milestone 2.1 Markdown/PDF extraction. Chunking portion of 2.2 is tested, but the milestone is not complete.

Evidence: [unit tests](../logs/validation/current-tests.txt), [storage write](../logs/validation/phase-1.2-storage-write.txt), [post-restart read](../logs/validation/phase-1.2-storage-read.txt), [container status](../logs/runtime/phase-1.2-services.txt), [HTTP response](../logs/validation/phase-1.2-http.json).

## In Progress

Milestone 2.2. Deterministic overlapping chunks preserve the directive's required metadata, PDF page numbers, and distinct source references. Embeddings, index ingestion, and real-model validation remain unimplemented.

## Pending

Model adapter, persistent document ingestion, retrieval/cited RAG, image analysis, review lifecycle, graph, controlled agents, encyclopedia, POCs, observability, and portable deployment. See [roadmap](ROADMAP.md).

## Blocked

User selected LM Studio at http://localhost:1234/v1. Model listing and a real two-input embedding request pass; embeddings contain 768 finite values. Docker API container also reaches http://host.docker.internal:1234/v1. Generation with google/gemma-4-e4b returned API_OK with a normal stop. The model prerequisite is validated; no current model-provider blocker. Image analysis will also require a supplied source image in Phase 3.

## Issues Found

[Issue records](../logs/issues/ISSUES.md). Dependency warnings are visible and nonblocking. Docker Desktop's credential helper stalls; public image downloads/builds succeeded using temporary isolated client configuration without editing user settings.

## Fixes Applied

Started Docker Desktop; retried package installation with authorized networking; passed isolated configuration through build subprocess environment; corrected Markdown closing-hash handling and validated the regression.

## Technical Decisions

[ADR-001](decisions/ADR-001-incremental-foundation.md), [ADR-002](decisions/ADR-002-api-foundation.md), [ADR-003](decisions/ADR-003-compose-storage.md), [ADR-004](decisions/ADR-004-document-extraction.md). Character-based chunk limits are simple and deterministic; model token limits must be checked by the eventual adapter.

## Known limitations and technical debt

No upload/query endpoints beyond health, model integration, authentication, or production TLS. PDFs have no OCR/table reconstruction; hostile PDF processing needs resource isolation before public exposure. Storage is single-node with administrative bootstrap credentials; least-privilege application access remains pending before ingestion. No source image supplied. Two upstream test deprecations remain. Container image versions are tagged, not digest-pinned.

## Next Task

Use the validated LM Studio provider to implement embeddings and idempotent document/vector ingestion. Validate a real model round-trip before advancing to 2.3. The learning checkpoint is authorized to continue; no repeated architecture approval is required.

LM Studio preflight evidence: [host API, embeddings, generation](../logs/validation/lmstudio-preflight-2026-09-11.json) and [container connectivity](../logs/validation/lmstudio-container-2026-09-11.txt). This validates the provider, not end-to-end RAG.
