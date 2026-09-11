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

## BUILD-001

- ID: BUILD-001
- Date: 2026-09-10
- Component: Python dependency installation
- Symptom: pip reports DNS resolution failures and no matching FastAPI distribution.
- Root Cause: Restricted sandbox network prevented access to the package index; not a missing package version.
- Fix: Re-ran the same dependency installation with approved network access and disabled the unavailable user cache.
- Validation: Installation exited 0; nine API tests passed and live HTTP health returned the expected JSON. See [initial error](../build/phase-1.1-dependencies.txt) and [retry](../build/phase-1.1-dependencies-retry.txt).
- Status: Resolved.

## DEPS-001

- ID: DEPS-001
- Date: 2026-09-10
- Component: Test dependencies
- Symptom: Two deprecation warnings from Starlette TestClient using httpx and an AnyIO alias.
- Root Cause: Pinned upstream Starlette uses compatibility interfaces deprecated by the current dependency versions.
- Fix: No application change needed; keep warnings visible rather than suppressing them. Revisit test client dependencies during the next dependency update.
- Validation: All nine tests pass; warnings captured in [test output](../validation/phase-1.1-tests.txt).
- Status: Open, nonblocking dependency maintenance.

### ENV-001 resolution

Docker Desktop status reported the application was not running. Started it using `docker desktop start`; `docker version` subsequently returned both client and server successfully. Root cause confirmed: Docker Desktop was stopped. Status: resolved for daemon availability. Evidence: [startup](../runtime/docker-start.txt), [server check](../runtime/docker-after-start.txt). Service validation is separate.

## BUILD-002

- ID: BUILD-002
- Date: 2026-09-10
- Component: Docker image pull
- Symptom: Compose pull showed no download progress; two docker-credential-desktop get processes remained waiting.
- Root Cause: Pull was waiting in the Desktop credential helper. Registry connectivity works; the underlying credential-helper failure is not diagnosed.
- Fix: Stop only this pull and its helper subprocesses; retry public images with a temporary empty Docker client configuration and explicit local daemon socket. User Docker configuration remains unchanged.
- Validation: Pending isolated public pull; see phase-1.2-pull logs.
- Status: Investigating.

BUILD-002 follow-up: the empty temporary configuration did not discover Compose (exit 1: unknown command). Added the installed Docker Desktop CLI plugin directory to the temporary configuration, then retried. This changes only the diagnostic configuration, not the project architecture.

BUILD-002 validation: isolated image pull exited 0. Compose build initially spawned buildx without inheriting the command-line configuration, causing another credential-helper wait. Applied the same focused workaround through DOCKER_CONFIG and DOCKER_HOST environment variables so child processes inherit it. Build retry is recorded separately. Do not edit or remove the user's credential store.

BUILD-002 resolution: public image pull, inherited-config build, and Compose health checks all passed. Vector and object round-trips passed before and after restart. Status: resolved for this execution using the temporary config workaround; the user's Desktop credential helper still needs separate maintenance.

## OPS-001

- ID: OPS-001
- Date: 2026-09-10
- Component: Foundation storage
- Symptom: MinIO warns a single host failure makes data unavailable; PostgreSQL initialization notes trust for local socket connections.
- Root Cause: Intentional single-node local lab and upstream PostgreSQL local initialization defaults. PostgreSQL has no host-published port; network clients require the configured password.
- Fix: Documented the development limitation; no high-availability or production security claim. Add backup/restore and least-privilege application credentials before broader use. Do not change unrelated storage settings during the round-trip milestone.
- Validation: Services healthy, vector/object round-trips survive restart; warning evidence in [container logs](../runtime/phase-1.2-containers.txt).
- Status: Accepted local limitation; revisit before deployment.

## EXTRACTION-001

- ID: EXTRACTION-001
- Date: 2026-09-10
- Component: Markdown heading extraction
- Symptom: Regression test showed the heading C# became C.
- Root Cause: Heading regex treated a trailing hash as a closing marker even without separating whitespace.
- Fix: Strip closing hash sequences only when preceded by whitespace.
- Validation: Reproduced with a failing regression; all 14 extraction tests pass after the focused fix. See [before](../validation/extraction-001-before.txt) and [after](../validation/extraction-001-after.txt).
- Status: Resolved.

## ENV-002

- ID: ENV-002
- Date: 2026-09-11
- Component: LM Studio connectivity validation
- Symptom: Sandboxed curl to localhost:1234/v1/models exited 7: could not connect to server.
- Root Cause: Sandbox networking prevented local API access; the server was running.
- Fix: Repeated the same read-only request outside the sandbox.
- Validation: HTTP 200 for model listing, two 768-dimensional embeddings, and generation returning API_OK. The Compose API container also reaches host.docker.internal:1234. See [preflight](../validation/lmstudio-preflight-2026-09-11.json).
- Status: Resolved.
