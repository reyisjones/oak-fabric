# Learning progress

Updated: 2026-09-11. The user authorized autonomous continuation. Implementation below is assistant work; learner understanding has not been assessed.

| Topic | Status | What I implemented | What I understand | Questions | Mistakes | Concepts to revisit | Next assignment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Architecture | Initial checkpoint released | Assistant planning and ADRs | Learner inspection unassessed | Where is original evidence retained? | None attributed to learner | Vector versus graph responsibilities | Trace a source through the current architecture |
| Foundation | Validated | Compose API, PostgreSQL/pgvector, MinIO and persistence tests | Unassessed | Why is liveness different from readiness? | Docker daemon/credential-helper issues diagnosed | Volumes and restricted credentials | Inspect bootstrap and storage round-trip evidence |
| Extraction | Validated | Markdown/PDF extraction and provenance | Unassessed | Why preserve PDF page numbers? | C# heading bug fixed with regression test | OCR and hostile-PDF boundaries | Inspect test_pdf_page_provenance |
| Chunking and embeddings | Validated | Stable chunks, Nomic vectors, metadata transaction and deduplication | Unassessed | Why must query/document prefixes differ? | No partial rows in injected failure tests | Content identity versus source revision identity | Repeat fixture ingestion and compare IDs |
| RAG | Validated on initial three-case corpus | Approved-source search and exact cited passages | Unassessed | Does source support imply a complete answer? | Unsupported JSON mode fixed; short quote omitted nearby pgvector fact, fixed by passage preservation | Faithfulness, relevance and completeness are distinct | Inspect expected_phrases and live responses |
| Image analysis | CLI and synthetic smoke tested; real image pending | Decoder, schema and review-draft CLI | Unassessed | Which real diagram should become the first entry? | None assessed | Extracted facts versus inferred relationships | Supply one source architecture image for the next milestone |

## Concepts in this milestone

An embedding maps text to a vector; Nomic requires different prefixes for document and query intent. The vector dimension and model identity are index invariants. PostgreSQL transactions prevent partially indexed revisions, while MinIO preserves original evidence even if later indexing fails.

Review is explicit: imported documents are drafts, and only approved revisions are searched. RAG asks a model to choose evidence, then checks that its quotation exists in the cited chunk. Returning the surrounding passage avoids dropping nearby facts. This proves textual support, but evaluation must still check relevance and answer completeness.

No agent framework, asynchronous queue, graph service, or new model download was necessary for this milestone.

## Image observation preparation — 2026-09-12

Assistant implemented decoding limits, structured references, separate inferences, original-byte preservation and versioned review drafts. Seventy-seven unit tests pass; live Gemma correctly reconstructs the labeled synthetic Client → API fixture. Real-diagram acceptance and learner understanding remain unassessed. Assignment: provide one real architecture diagram, then compare visible labels/arrows with the JSON observations and identify any uncertainty or unsupported claim before rendering or indexing.

### Real image validation — 2026-09-12

- Topic: Schema validity versus factual accuracy in vision extraction.
- Status: AI-Embedings.png supplied; real-model accuracy debugging in progress.
- What I implemented: Preserved the source, recorded explicit panel scope, added a node/edge baseline from visual inspection and retained failed extraction evidence.
- What I understand: User understanding remains unassessed.
- Questions: Which arrows are actually drawn, and which would merely be expected in a typical RAG architecture?
- Mistakes: Gemma returned headings instead of nodes; a focused attempt duplicated edges. Qwen timed out on the full image and returned empty content on the focused retry.
- Concepts to revisit: Prompt compliance is not a correctness guarantee; schema validation and source comparison are complementary.
- Next assignment: Inspect panel 11 and compare the two rows with the expected node/edge fixture. Notice the absent connection between the vector database and query row.
