# Learning progress

| Topic | Status | What I implemented | What I understand | Questions | Mistakes | Concepts to revisit | Next assignment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Architecture and first slice | Ready for user inspection | No user implementation recorded; assistant created planning artifacts | Not assessed | Is the image → reviewed knowledge → cited answer flow clear? | None assessed | Vector similarity versus graph relationships | Inspect the architecture and trace one source to its cited answer |
| Foundation | Pending | None | Not assessed | Docker daemon availability; model choice | None assessed | Persistence and readiness | After inspection, review the minimal health API and service round-trips |

## First manageable assignment

Read [vision.md](../architecture/vision.md) and [ADR-001](../decisions/ADR-001-incremental-foundation.md). Trace one hypothetical architecture image from original bytes through review to a cited answer. Identify where the original, metadata, and embeddings live; explain why Neo4j comes later. Note one unclear point here or in the conversation. Optionally supply a real architecture image for the future ingestion fixture.

The concept: object storage retains original evidence, PostgreSQL tracks its identity and status, and pgvector retrieves similar evidence. Keeping these roles explicit makes answers inspectable and permits later graph enrichment.

Acceptance: the learner can inspect the flow and distinguish generated drafts from approved knowledge. Inspection has not yet occurred; do not mark understanding or approval complete. After feedback, review gaps, record corrections, and proceed to milestone 1.1.

## Milestone 1.1 execution

The user authorized continuation after the initial checkpoint. Assistant implemented the API foundation; nine tests and a real local HTTP call passed. Learner understanding has not been assessed. Inspection assignment: run `make test` and `make run`, then request `/health`; explain why a healthy process does not prove database readiness. No learner mistakes are assumed.

## Milestones 1.2 and 2.1

Assistant validated three containers and storage persistence after restart, then implemented Markdown/PDF extraction. Twenty-two cumulative tests pass. Learner inspection remains unassessed. Assignment: inspect the two-page PDF test and explain why retaining page numbers matters for a cited answer; compare a content checksum with a source path. Revisit single-node storage limitations and scanned-PDF/OCR boundaries.

## Chunking inspection

Assistant implemented deterministic character windows with overlap and source/page metadata. Full embedding milestone remains pending model setup. Assignment: inspect `test_chunk_overlap_coverage_and_stable_identity` and explain how overlap retains context and why source references distinguish identical content at different paths. Audit found a heading-regex error for C#; a regression test reproduced it and the focused fix passed. Learner understanding is not inferred from assistant test results.
