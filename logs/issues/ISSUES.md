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

## RAG-001

- ID: RAG-001
- Date: 2026-09-11
- Component: LM Studio structured generation
- Symptom: First live RAG query returned 502 after draft exclusion succeeded.
- Root Cause: LM Studio rejected response_format.type=json_object with HTTP 400; this server accepts json_schema or text.
- Fix: Replace generic JSON mode with an explicit evidence JSON schema; retain exact quote/citation validation.
- Validation: Original failure in [evaluation](../validation/phase-2.3-evaluation.jsonl); exact provider error in [diagnostic](rag-001-provider-error.txt). Live re-evaluation pending.
- Status: Fix applied, validation pending.

RAG-001 validation: supported JSON schema requests now succeed. Two source questions and the unsupported pricing question passed the original checks in [retry evidence](../validation/phase-2.3-evaluation-retry.jsonl). Status: resolved. A separate answer-completeness gap was found during output inspection below.

## RAG-002

- ID: RAG-002
- Date: 2026-09-11
- Component: Answer completeness and evaluation
- Symptom: A two-part question requested database and vector extension, but the answer named only PostgreSQL.
- Root Cause: Evidence selection did not explicitly require coverage of all question parts; the initial evaluation checked only the database keyword.
- Fix: Require expected phrases for both parts in evaluation and explicitly instruct evidence selection to cover every answerable part using additional exact quotes.
- Validation: Missing pgvector reproduced from saved model output in [coverage audit](rag-002-coverage.txt). Updated live evaluation pending.
- Status: Fix under validation.

RAG-002 follow-up: the prompt-only fix did not improve the two-part answer; stricter live evaluation still failed (see [failed retry](../validation/phase-2.3-complete-evaluation.jsonl)). Revised focused fix: after validating the model's exact quote, return its full bounded source chunk as the cited passage. This preserves surrounding facts and qualifications instead of trusting the model to choose sufficient sentence boundaries. The answer remains source text, not a generated paraphrase; broader multi-source completeness is still an evaluation concern.

RAG-002 resolution: passage preservation passed the stricter live evaluation for both PostgreSQL and pgvector, plus original-source retrieval and unsupported-pricing abstention. Evidence: [final passage evaluation](../validation/phase-2.3-passage-evaluation.jsonl). Status: resolved for the tested cases; broad corpus completeness remains a documented evaluation limitation.

## MODEL-001

- ID: MODEL-001
- Date: 2026-09-11
- Component: Embedding response validation
- Symptom: Malformed JSON root types (null/list/integer) raised an uncaught AttributeError instead of the model-service error.
- Root Cause: Validation assumed an object root before calling get().
- Fix: Convert the root-type AttributeError into the existing sanitized ModelError boundary.
- Validation: Three regression failures reproduced in [before](../validation/model-001-before.txt); all 14 embedding tests pass in [after](../validation/model-001-after.txt).
- Status: Resolved.

## BUILD-003

- ID: BUILD-003
- Date: 2026-09-12
- Component: Temporary Docker client configuration
- Symptom: Container build exited 125 with unknown flag --build.
- Root Cause: The prior temporary Docker configuration no longer existed, so the isolated client could not discover the Compose plugin.
- Fix: Recreated the temporary configuration with the installed Docker Desktop plugin directory; user Docker settings remain unchanged.
- Validation: Original error in [build log](../build/phase-3.1-container.txt); retry pending.
- Status: Fix applied, validation pending.

BUILD-003 configuration fix confirmed: Compose is discovered again; retry reached daemon connection and revealed a separate stopped-runtime issue. Status: resolved for plugin discovery.

## ENV-003

- ID: ENV-003
- Date: 2026-09-12
- Component: Docker Desktop runtime
- Symptom: Build retry cannot connect to the local Docker daemon.
- Root Cause: Selected Docker Desktop daemon is unavailable; application startup is being attempted.
- Fix: Start Docker Desktop, then retry the same container build.
- Validation: [Connection error](../build/phase-3.1-container-retry.txt); startup and build verification pending.
- Status: In progress.

ENV-003 resolution: Docker Desktop startup completed successfully and the rebuilt API, PostgreSQL and MinIO containers all passed health checks. Evidence: [startup](../runtime/phase-3.1-docker-start.txt) and [final build](../build/phase-3.1-container-final.txt). Status: resolved.

## IMAGE-001

- ID: IMAGE-001
- Date: 2026-09-12
- Component: Vision extraction of multi-panel diagrams
- Symptom: Real cheat-sheet extraction returned section headings as components, zero arrows, and misread section 12.
- Root Cause: The extraction prompt did not distinguish informational panel headings from nodes within embedded diagrams.
- Fix: Explicitly extract nodes and arrows inside each diagram panel, keeping repeated nodes distinct and headings as grouping context.
- Validation: Initial draft retained under documents/generated/image-analysis; focused real-image retry pending.
- Status: In progress.

IMAGE-001 retry: the clarified prompt still produced zero arrows and omitted panel 11, filling the 50-component limit with prose. Prompt-only correction failed. Next focused diagnostic: run the same source and contract with the already installed Qwen vision model to distinguish provider capability from workflow defects. No additional model download.

IMAGE-001 next focused fix: add an explicit, provenance-recorded panel focus to the existing CLI. Dense infographics can be analyzed one diagram at a time while preserving the full original. No image crop or fabricated connection is introduced. Retry scope: panel 11 only.

## IMAGE-002

- ID: IMAGE-002
- Date: 2026-09-12
- Component: Qwen local vision diagnostic
- Symptom: No response headers arrived before the 120-second client timeout.
- Root Cause: Provider inference did not finish within the configured request window; loading versus generation cost is unconfirmed.
- Fix: No speculative timeout increase; retain bounded requests and return to Gemma with a narrower panel scope for IMAGE-001.
- Validation: Timeout captured in [runtime log](../runtime/image-001-qwen.txt); original retained, no Qwen draft created.
- Status: Open diagnostic limitation; Qwen is not selected as the validated image provider.

IMAGE-001 focused retry reached panel 11 but was rejected for duplicate connections ([log](../runtime/image-001-focused.txt)). Validation correctly prevented acceptance. Focused follow-up: explicitly require each edge once; capture the controlled real-image model response in the evaluation log to inspect any remaining factual or structural errors. Structural validation remains unchanged.

IMAGE-001 final Gemma focus outcome: structurally valid but visually incorrect. Vector Database and Relevant Context are missing, User Query is shortened to Query, and Similarity Search → LLM is an unsupported shortcut. [Subset evaluation](../validation/image-001-focused.json) fails. Focus support is retained as an explicitly scoped feature, not claimed as a complete accuracy fix. A warm Qwen focused comparison is pending.

IMAGE-002 follow-up: the focused Qwen retry responded within the request window but returned empty content, rejected as invalid JSON ([log](../runtime/image-001-qwen-focused.txt)). The timeout is not consistently reproducible; provider structured-output/generation behavior needs diagnosis. No model output was accepted. Status: open.

IMAGE-001 current outcome: automatic real-image acceptance remains failed after targeted prompt and panel-focus attempts. Original-byte checks pass; 78 unit tests pass. Detailed [visual review](../validation/ai-embeddings-review.md) records expected source facts and every attempt. Status: open; milestone 3.1 remains incomplete and 3.2 has not started.
