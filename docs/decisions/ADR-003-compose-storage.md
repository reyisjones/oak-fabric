# ADR-003: Local persistence and container boundaries

Date: 2026-09-10. Status: accepted; startup and persistence validated.

## Context

The foundation needs reproducible PostgreSQL/vector and original-object storage before ingestion begins.

## Decision

Use three Compose services: a non-root API, PostgreSQL 17 with pgvector 0.8.6, and MinIO. Keep database and S3 ports internal. Publish only API and object console on loopback. Use required credentials with no password defaults, named volumes, and a first-database-init vector extension script. The API has no store dependency yet, so no artificial startup dependency is configured.

## Alternatives

Host-installed services reduce container use but violate Docker-first reproducibility. Neo4j and orchestration services remain deferred according to ADR-001.

## Tradeoffs

PostgreSQL bootstrap user and MinIO root are foundation-only administrative credentials. Introduce limited application users before ingestion exposes data access. Tagged images are reproducible at version level but not immutable; record resolved digests after validation and revisit patch/security updates before deployment.

## Consequences

Run storage round-trips independently of API health. Recheck records after service restart. Initialization scripts run only on empty volumes; future schema changes need explicit migrations. Test probe records use a dedicated table and bucket and remain inspectable. Do not claim production readiness.

Sources: [pgvector installation](https://github.com/pgvector/pgvector) and [Compose health/startup semantics](https://docs.docker.com/compose/how-tos/startup-order/).
