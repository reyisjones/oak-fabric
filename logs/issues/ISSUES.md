# Issue records

## ENV-001

- ID: ENV-001
- Date: 2026-09-10
- Component: Local Docker runtime
- Symptom: docker version cannot query server; initially reports socket permission denied.
- Root Cause: Initial sandbox restriction obscured runtime state. Read-only unrestricted retry confirms selected Docker daemon is unreachable. Whether Desktop is stopped or context/socket is stale is not yet established.
- Fix: Focused diagnostic retry removed sandbox restriction; no daemon/configuration mutation applied. Before milestone 1.2, start Docker Desktop or correct its context after inspection.
- Validation: Retry exits 1 with daemon connection error; see [runtime evidence](../runtime/docker-preflight.txt).
- Status: Open; blocks container validation, not initial documentation. Do not mark resolved until docker version shows server data and subsequent Compose checks pass.

No build/runtime implementation exists yet. Record later issues individually with these same fields and link their affected validation results.
