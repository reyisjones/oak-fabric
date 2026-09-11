# Project status

Updated: 2026-09-11.

| Field | Latest state |
| --- | --- |
| Current Phase | Phase 2 complete; Phase 3 awaiting source image |
| Last Completed Task | 2.3 source-grounded document RAG, including strict live evaluation |
| Current Task | Awaiting a real source image for milestone 3.1 |
| Pending Tasks | Image analysis and later phases |
| Open Issues | Source image needed; DEPS-001 upstream test warnings; local deployment limitations |
| Recent Fixes | LM Studio JSON schema compatibility; multi-part evidence selection |
| Architecture Decisions | ADR-005 ingestion; ADR-006 exact cited quotations |
| Next Recommended Action | Supply one real architecture image for milestone 3.1 |

## Completed

Initial planning and Git setup; healthy API/PostgreSQL/pgvector/MinIO containers and restart persistence; Markdown/PDF extraction; deterministic source-linked chunking; actual LM Studio embeddings; transactional vector/metadata storage; idempotent re-ingestion; restricted application storage accounts; bearer authentication; explicit draft approval.

Evidence: [real ingestion](../logs/validation/phase-2.2-ingestion.txt), [failure rollback](../logs/validation/phase-2.2-failure-recovery.txt), [unit tests](../logs/validation/phase-2.3-unit.txt), [LM Studio preflight](../logs/validation/lmstudio-preflight-2026-09-11.json).

## In Progress

No next-phase implementation is active until a source image is available. Phase 2 live evaluation passed source retrieval, two-part completeness, exact passage support and unsupported-question abstention. The approved document, source bytes and vectors also survived restart. No image implementation has begun.

## Pending

Image analysis, structured architecture rendering/review, Neo4j, GraphRAG, specialized workflows, encyclopedia, POCs, justified data platform additions, observability, and Kubernetes packaging. See [roadmap](ROADMAP.md).

## Blocked

No provider blocker. Phase 3 requires a real source architecture image; none was supplied in the initial inventory. The previous initial architecture checkpoint was explicitly released by the user.

## Issues Found

See [issues](../logs/issues/ISSUES.md). RAG-001 schema compatibility, RAG-002 passage completeness, and MODEL-001 malformed response handling resolved. Original-source objects may remain unindexed after a failed operation, intentionally retained for retry.

## Fixes Applied

Started Docker Desktop and isolated its stalled credential helper for public downloads. Corrected C# heading parsing. Used LM Studio's supported evidence schema. Strengthened multi-part answer evaluation and evidence-selection instructions.

## Technical Decisions

[ADR-005](decisions/ADR-005-local-model-ingestion.md) and [ADR-006](decisions/ADR-006-cited-extractive-rag.md). Keep source revisions distinct, preserve original bytes, publish only explicit approvals, and reject model/index incompatibility. No queue or agent framework was added.

## Known limitations and technical debt

No image analyzer or graph integration. No OCR/table reconstruction. Authenticated local uploads are trusted; hostile PDF processing needs stronger process isolation before public exposure. Single-node HTTP is not production deployment. Model changes require index migration. Character chunking is not a token guarantee. Exact quotes prove textual support but do not alone prove relevance/completeness. Two dependency deprecation warnings remain. Image tags are not digest-pinned.

## Next Task

Begin milestone 3.1 with a supplied real diagram; preserve its original bytes and distinguish observed facts from uncertainty. Learning assignments are available without requiring repeated architecture approval.

Final Phase 2 evidence: [unit suite](../logs/validation/phase-2-final-unit.txt) and [strict real-model evaluation](../logs/validation/phase-2.3-passage-evaluation.jsonl). Three cases are a baseline, not broad quality certification.

Post-restart evidence: [approved document persistence](../logs/validation/phase-2-persistence.txt).
