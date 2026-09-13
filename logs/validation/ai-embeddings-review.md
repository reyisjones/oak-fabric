# AI Embeddings source review

Date: 2026-09-12. Reviewer: Codex, through direct visual inspection. This is an engineering validation record, not human approval or canonical knowledge.

Source: [AI-Embedings.png](../../images/incoming/AI-Embedings.png). SHA-256: `6aaf119577d61320072c8b8d69d1a65dc156bc79bfe0fefd6e6599f09487f2d6`. The 932 × 1688 original is preserved byte-for-byte under images/processed.

## Observed scope

The source is an educational cheat sheet attributed in the image to @techly23, with multiple independent panels. Panel 11, “COMPLETE RAG EMBEDDING FLOW”, contains these visible directed sequences:

- Documents → Chunking → Embeddings → Vector Database.
- User Query → Query Embedding → Similarity Search (Top-K) → Relevant Context → LLM → Answer.

There are ten boxes and eight explicit directed arrows in that panel. No arrow joins the database to the lower row. No concrete database or LLM vendor is printed in panel 11. These missing details must remain unspecified. Product names and numerical advice elsewhere in the sheet are source claims, not independently verified technical recommendations.

## Actual model outcomes

1. Gemma full sheet: section headings instead of process nodes; zero arrows; section 12 misread.
2. Gemma clarified prompt: prose consumed the component budget; zero arrows; panel 11 omitted.
3. Qwen full sheet: request timed out at 120 seconds; no draft.
4. Gemma panel focus: duplicate edges; structural validation rejected the response.
5. Gemma panel focus plus unique-edge instruction: valid structure, but Vector Database and Relevant Context omitted, User Query shortened, and an unsupported Similarity Search → LLM shortcut added.
6. Qwen panel focus: empty response content; structural validation rejected it. This retry did return before timeout, but did not produce usable JSON. Underlying generation/template behavior remains unconfirmed.

## Result

FAIL for automatic real-image acceptance. Neither valid JSON nor a passing synthetic test is sufficient evidence of reconstruction accuracy. The original and separate draft attempts remain intact. No entry was approved, rendered into canonical documentation, embedded, or indexed. Milestone 3.1 remains in progress; 3.2 has not started.

The panel-focus option and preservation tests pass. The [focused accuracy report](image-001-focused.json) records missing and unsupported edges. The [unit suite](phase-3.1-real-unit.txt) has 78 passing tests and two pre-existing dependency warnings.

Next: diagnose the vision provider's structured response behavior using saved evidence before another extraction attempt. Do not relax the visual acceptance fixture or silently substitute a typical RAG flow for the source.
