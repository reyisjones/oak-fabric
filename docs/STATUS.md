# Project status

Updated: 2026-09-12.

| Field | Latest state |
| --- | --- |
| Current Phase | Phase 3 — Image analyzer; real-diagram acceptance pending |
| Last Completed Task | 2.3 source-grounded document RAG, including strict live evaluation |
| Current Task | 3.1 code and synthetic vision validation complete; real-diagram acceptance pending |
| Pending Tasks | Image analysis and later phases |
| Open Issues | Real source image needed; DEPS-001 upstream test warnings; local deployment limitations |
| Recent Fixes | Restored temporary Docker config and started Docker Desktop |
| Architecture Decisions | ADR-007 image observation drafts; previous ingestion/RAG ADRs |
| Next Recommended Action | Supply one real architecture image for milestone 3.1 |

## Completed

Initial planning and Git setup; healthy API/PostgreSQL/pgvector/MinIO containers and restart persistence; Markdown/PDF extraction; deterministic source-linked chunking; actual LM Studio embeddings; transactional vector/metadata storage; idempotent re-ingestion; restricted application storage accounts; bearer authentication; explicit draft approval.

Evidence: [real ingestion](../logs/validation/phase-2.2-ingestion.txt), [failure rollback](../logs/validation/phase-2.2-failure-recovery.txt), [unit tests](../logs/validation/phase-2.3-unit.txt), [LM Studio preflight](../logs/validation/lmstudio-preflight-2026-09-11.json).

## In Progress

Milestone 3.1 implementation has begun with structural tests and a clearly labeled synthetic vision fixture. Phase 2 live evaluation passed source retrieval, two-part completeness, exact passage support and unsupported-question abstention. The approved document, source bytes and vectors also survived restart. Seventy-seven unit tests and the real LM Studio synthetic-image smoke test pass; a supplied real diagram is still required to complete 3.1.

## Pending

Real-image acceptance, structured architecture rendering/review, Neo4j, GraphRAG, specialized workflows, encyclopedia, POCs, justified data platform additions, observability, and Kubernetes packaging. See [roadmap](ROADMAP.md).

## Blocked

No provider blocker. Phase 3 requires a real source architecture image; none was supplied in the initial inventory. The previous initial architecture checkpoint was explicitly released by the user.

## Issues Found

See [issues](../logs/issues/ISSUES.md). RAG-001 schema compatibility, RAG-002 passage completeness, and MODEL-001 malformed response handling resolved. Original-source objects may remain unindexed after a failed operation, intentionally retained for retry.

## Fixes Applied

Recreated the expired temporary Docker client configuration; Docker startup and container validation passed. Corrected C# heading parsing. Used LM Studio's supported evidence schema. Strengthened multi-part answer evaluation and evidence-selection instructions.

## Technical Decisions

[ADR-005](decisions/ADR-005-local-model-ingestion.md) and [ADR-006](decisions/ADR-006-cited-extractive-rag.md). Keep source revisions distinct, preserve original bytes, publish only explicit approvals, and reject model/index incompatibility. No queue or agent framework was added.

## Known limitations and technical debt

Image analysis exists as a local CLI; no HTTP image endpoint, architecture rendering or graph integration yet. No OCR/table reconstruction. Authenticated local uploads are trusted; hostile PDF processing needs stronger process isolation before public exposure. Single-node HTTP is not production deployment. Model changes require index migration. Character chunking is not a token guarantee. Exact quotes prove textual support but do not alone prove relevance/completeness. Two dependency deprecation warnings remain. Image tags are not digest-pinned.

## Next Task

Complete milestone 3.1 using a supplied real diagram; preserve its original bytes and distinguish observed facts from uncertainty. Learning assignments are available without requiring repeated architecture approval.

Final Phase 2 evidence: [unit suite](../logs/validation/phase-2-final-unit.txt) and [strict real-model evaluation](../logs/validation/phase-2.3-passage-evaluation.jsonl). Three cases are a baseline, not broad quality certification.

Post-restart evidence: [approved document persistence](../logs/validation/phase-2-persistence.txt).

Phase 3 evidence: [unit tests](../logs/validation/phase-3.1-unit.txt), [synthetic vision smoke](../logs/validation/phase-3.1-vision-smoke.txt), [structured output](../logs/validation/phase-3.1-synthetic-analysis.json), and [ADR-007](decisions/ADR-007-image-observation-drafts.md). Synthetic testing does not mark milestone 3.1 complete.

Container packaging and health evidence: [final image-analysis build](../logs/build/phase-3.1-container-final.txt).
