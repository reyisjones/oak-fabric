# ADR-007: Image observations as separate review drafts

Date: 2026-09-12. Status: implementation tested; real-diagram acceptance pending.

## Context

Document RAG is validated, but no real architecture image has been supplied. The next milestone can prepare image decoding, a structured observation contract, and a controlled vision workflow without publishing unreviewed architecture claims.

## Decision

Reuse the LM Studio client and its advertised vision-capable Gemma model. Validate PNG/JPEG/WebP bytes (10 MiB, 16 million pixels, one frame) before inference. Preserve the original bytes in images/processed under their SHA-256 digest. Never alter or remove the incoming source.

Use a small Pydantic contract for observed components, directed connections, boundaries, uncertainties, and separate inferences. Require visible-evidence descriptions and valid component references; reject duplicate IDs/edges, unknown references, extra fields, truncated responses, and unexplained empty analyses. The model must not infer printed technology names from icons or add missing infrastructure.

Each CLI run writes a new JSON draft under documents/generated/image-analysis with source digest, model, timestamp, and validation state. It does not update PostgreSQL, vectors, approved knowledge, or earlier drafts. Model/structure failures retain the original but do not produce an accepted analysis file. A successful structural check never implies visual correctness or human approval.

## Alternatives

Waiting for an image before implementing any testable structure wastes independent work. Treating a synthetic diagram as a real architecture would overstate validation. Building image APIs, graph integration, rendering and approval together would cross unvalidated milestones.

## Tradeoffs

One extra image-decoding dependency is required. Local files are the initial interface; HTTP image ingestion and canonical review/rendering remain future work. Each successful run creates a new draft rather than caching potentially stale model output. Original sources are content-addressed, not protected by filesystem object-lock controls. Dense or ambiguous diagrams require human correction and evaluation.

## Consequences

A clearly labeled synthetic two-box diagram proves the image request path works and checks known labels/arrow direction. It is not an encyclopedia source and does not complete milestone 3.1. A real source diagram is still required before moving to Markdown/Mermaid generation in 3.2.

References: [LM Studio chat completions](https://lmstudio.ai/docs/developer/openai-compat/chat-completions), [structured output](https://lmstudio.ai/docs/developer/openai-compat/structured-output).
