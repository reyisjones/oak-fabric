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
