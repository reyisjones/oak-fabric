# Image inventory

Inspected 2026-09-10. The workspace initially contained only directive.md. No images directory exists and no architecture images were supplied.

| Filename | Probable architecture | Technologies | Major components | Relationships | Documentation topic |
| --- | --- | --- | --- | --- | --- |
| None supplied | Unknown | Unknown | Unknown | Unknown | Await source image |

No source claims or architecture reconstructions have been invented. Create images/incoming when image ingestion begins. Preserve original bytes and record source path, checksum, media type, ingestion time, and analysis provenance. Add one row per image after visual inspection. Mark unreadable labels and uncertain relationships explicitly; do not infer them silently.

Rechecked 2026-09-11 after document RAG completion: no PNG/JPEG/WebP/GIF source images found. Phase 3 needs a real diagram supplied by the user; no architecture image has been fabricated or analyzed.

2026-09-12: added tests/fixtures/synthetic-architecture.png as a labeled synthetic test fixture. It contains Client → API with an arrow labeled request. It is not a user-supplied architecture and is not published to the encyclopedia. No real architecture image has been supplied.

| Current fixture | Origin | Components | Relationship | Scope |
| --- | --- | --- | --- | --- |
| [synthetic-architecture.png](../tests/fixtures/synthetic-architecture.png) | Programmatically generated test image | Client, API; no technology names printed | Client → API, labeled request | Live vision smoke only; not canonical knowledge |

## User source received 2026-09-12

[AI-Embedings.png](../images/incoming/AI-Embedings.png) is a 932 × 1688 educational cheat sheet titled “AI EMBEDDINGS COMPLETE CHEAT SHEET”, attributed in the image to @techly23. It contains multiple diagrams and explanatory panels, not one deployed architecture. Original SHA-256: `6aaf119577d61320072c8b8d69d1a65dc156bc79bfe0fefd6e6599f09487f2d6`.

Panel 11 visibly contains Documents → Chunking → Embeddings → Vector Database and User Query → Query Embedding → Similarity Search (Top-K) → Relevant Context → LLM → Answer. No explicit connection joins the two rows. Panel 2 contains Text Input → Embedding Model → Vector Embedding. Technology examples elsewhere include OpenAI, BGE, Sentence Transformers, CLIP, Whisper, Pinecone, Milvus and Weaviate; these are examples printed in the source, not verified deployment choices. Potential documentation topic: embeddings and RAG flows. Numerical/product claims in the cheat sheet have not been independently verified.

The source has been preserved byte-for-byte. The initial model extraction failed visual acceptance (IMAGE-001); it must not be promoted to canonical knowledge. The earlier “no source” entries above describe the historical inventory only.
