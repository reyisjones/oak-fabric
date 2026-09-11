# Architecture Storage Guide

## Original sources
MinIO preserves original architecture documents and images as objects. The original source bytes are retained so generated knowledge can be audited.

## Metadata and vectors
PostgreSQL stores document metadata. The pgvector extension stores 768-dimensional embeddings and supports vector similarity retrieval.

## Graph relationships
Neo4j is planned for explicit relationships between architectures and technologies. It has not been integrated into this platform yet.
