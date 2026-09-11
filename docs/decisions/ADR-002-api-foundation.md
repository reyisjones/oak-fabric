# ADR-002: Minimal API foundation

Date: 2026-09-10. Status: accepted for milestone 1.1.

## Context

The first API milestone needs a real health endpoint, validated configuration, and repeatable dependencies before storage integration.

## Decision

Use a FastAPI application factory, one immutable settings dataclass, and a typed liveness response. Reject unknown APP_ENV values on startup. Disable interactive documentation and OpenAPI in production. Pin runtime and test dependencies separately. Use Python 3.14, matching the validated local interpreter. Keep Uvicorn bound to loopback for local development.

## Alternatives

A settings framework, dependency injection container, or general service layer would add indirection for one setting and one route. Defer these until a concrete requirement exists.

## Tradeoffs

GET /health checks process liveness only. It must not be interpreted as storage readiness. No ingestion, authentication, or database behavior is implemented in milestone 1.1.

## Consequences

Storage readiness and round-trip validation belong to milestone 1.2. Tests cover HTTP contracts, unsupported methods/routes, configuration rejection, and production schema exposure. Framework testing follows the [FastAPI testing documentation](https://fastapi.tiangolo.com/tutorial/testing/); container packaging follows its [Docker guidance](https://fastapi.tiangolo.com/deployment/docker/).
