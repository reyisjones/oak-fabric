# ADR-006: Approved-source retrieval and verifiable answers

Date: 2026-09-11. Status: accepted; initial real-model evaluation passed.

## Context

The first RAG milestone needs demonstrable provenance and faithfulness, not merely fluent answers.

## Decision

Query Nomic with its search_query prefix, perform exact cosine search in pgvector, and retrieve at most five chunks from approved revisions above a 0.35 similarity threshold. Ask the generation model to select up to three exact contiguous quotations and their evidence IDs. Validate every quote against its cited chunk; return the full bounded source passage for each validated selection, constructing source/page/section references in Python. Preserving the passage retains nearby facts and qualifications. Empty evidence produces explicit abstention. Invalid citations, altered quotations, and truncated model output fail rather than publish unsupported text.

## Alternatives

Free-form summarization is more expressive but harder to check reliably. Exact quotation limits the first answer format while enabling objective source-faithfulness tests. A semantic entailment model is deferred.

## Tradeoffs

Quotation matching guarantees textual support, not that a quote is relevant or complete. Evaluation must test retrieval correctness and question relevance separately. The initial threshold is a baseline, not a calibrated probability. Small fixture evaluations do not establish general answer quality. No graph traversal, cross-document synthesis, or automatic research is included.

## Consequences

Return citation objects alongside text. Use LM Studio json_schema mode, not unsupported json_object mode. Preserve approved-source boundaries and superseded revisions. Evaluate positive questions and unsupported questions with known expected sources before completing milestone 2.3. Later narrative answers must retain source validation and add appropriate faithfulness evaluation.

Provider reference: [LM Studio structured output](https://lmstudio.ai/docs/developer/openai-compat/structured-output).
