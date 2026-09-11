# ADR-004: Text extraction with explicit provenance

Date: 2026-09-10. Status: accepted for milestone 2.1.

## Context

Retrieval needs source-linked text before model integration. Markdown and digitally generated PDFs are the first supported inputs.

## Decision

Use pure functions accepting a source reference and bytes. Compute document identity with SHA-256 of original bytes, keep the source reference, and preserve PDF page numbers. Split Markdown at ATX headings while ignoring headings inside fenced code. Use pypdf for text extraction. Fail explicitly for unsupported, empty, malformed, encrypted, oversized, or textless documents. Initial limits: 20 MiB input and 500 PDF pages.

## Alternatives

OCR, layout reconstruction, and a general ingestion framework would widen scope before basic extraction is validated. Retain original bytes at the future ingestion boundary so better extraction can be applied later.

## Tradeoffs

No OCR, table reconstruction, or Setext heading recognition. A PDF's extracted text may not preserve reading order. Input/page limits do not fully constrain decompressed PDF streams: hostile PDFs need process-level resource isolation before public upload is exposed. The module is currently a local library, not an upload endpoint. Content IDs identify identical bytes; ingestion must separately track multiple source references for the same content.

## Consequences

Do not infer facts from empty pages. Store provenance before chunking. Tests use known text fixtures, including two-page PDF evidence, encrypted/malformed rejection, and code-fence handling.

Reference: [pypdf text extraction and limits](https://pypdf.readthedocs.io/en/stable/user/extract-text.html).
