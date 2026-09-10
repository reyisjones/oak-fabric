# Learning progress

| Topic | Status | What I implemented | What I understand | Questions | Mistakes | Concepts to revisit | Next assignment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Architecture and first slice | Ready for user inspection | No user implementation recorded; assistant created planning artifacts | Not assessed | Is the image → reviewed knowledge → cited answer flow clear? | None assessed | Vector similarity versus graph relationships | Inspect the architecture and trace one source to its cited answer |
| Foundation | Pending | None | Not assessed | Docker daemon availability; model choice | None assessed | Persistence and readiness | After inspection, review the minimal health API and service round-trips |

## First manageable assignment

Read [vision.md](../architecture/vision.md) and [ADR-001](../decisions/ADR-001-incremental-foundation.md). Trace one hypothetical architecture image from original bytes through review to a cited answer. Identify where the original, metadata, and embeddings live; explain why Neo4j comes later. Note one unclear point here or in the conversation. Optionally supply a real architecture image for the future ingestion fixture.

The concept: object storage retains original evidence, PostgreSQL tracks its identity and status, and pgvector retrieves similar evidence. Keeping these roles explicit makes answers inspectable and permits later graph enrichment.

Acceptance: the learner can inspect the flow and distinguish generated drafts from approved knowledge. Inspection has not yet occurred; do not mark understanding or approval complete. After feedback, review gaps, record corrections, and proceed to milestone 1.1.
