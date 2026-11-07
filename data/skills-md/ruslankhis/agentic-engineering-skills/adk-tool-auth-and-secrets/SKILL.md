---
name: adk-tool-auth-and-secrets
description: >-
  Implement or review authenticated Google ADK tools with verified
  user/session ownership at the tool hop, keyless GCP access, Secret Manager
  and delegated OAuth lifecycle controls. Use for tool credential selection,
  cross-user access through a tool, consent/refresh/disconnect flows or
  credential exposure in agent events. Do not activate for generic sign-in UI,
  the verified-principal dependency or owner-filtered HTTP routes
  (adk-fastapi-backend), the agent's session endpoints
  (adk-frontend-integration), MCP or A2A connection wiring
  (adk-agent-interoperability), whole-agent threat models
  (adk-agent-security), screening content for PII or pasted secrets
  (protect-adk-sensitive-data), general IAM administration or model-key
  billing troubleshooting.
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "09"
  validation-date: "2026-09-16"
  verified-against: "google-adk 2.8.0 offline and live tests 2026-09-16; 2.12.0 CHANGELOG and source read 2026-10-24"
  version: "2026.10.28"
---

# Secure ADK tool authentication and credentials

Produce a scoped implementation, repair or audit of this boundary:
**verified application principal → owned session → authorised operation → correct credential → allowlisted result**.
The skill is self-contained. The book and companion repository are optional provenance, not dependencies.

## Inspect and choose

1. Read project instructions, dependency declarations/locks, gateway, tool schemas, identity verification, credential index/store, exports and relevant tests. Preserve the package manager, pinned Python/ADK versions and existing architecture. Never import application modules merely to inspect them: import side effects can initialise clients or read credentials. Note whether the `google-adk` pin is below 2.12.0, the release that stops OAuth2 secrets reaching the serving endpoints (its user-id fix covers A2A requests only; the HTTP routes still take a caller-supplied user id) ([compatibility and evidence](references/compatibility-and-evidence.md)).
2. Optionally run `python "$SKILL_DIR/scripts/inspect_project.py" --project "$TARGET_PROJECT"`, resolving `SKILL_DIR` to this skill's directory. It reads bounded source/manifests and emits locations and static observations, not a security verdict. Use its `--help` for limits and a version expectation. Inspect relevant code at the reported locations without dumping secret values, `.env` files or raw logs.
3. Record the requested operation (review/recommend, implement/fix, or verify), identities at each hop, credential owner, permitted destinations/scopes, persistent stores, replicas, chosen model/backend and which external systems are real or mocked. Infer existing choices before asking; ask only about missing decisions that affect identity, custody, approval or compatibility.
4. Select the required credential branch below. If several apply, handle their shared boundary within this one skill. Explain a short plan before broad changes. Inspection is complete when the principal, credential owner and applicable branch are known, or their unresolved questions are explicitly recorded.

| Target authority | Branch to read |
| --- | --- |
| Workload access to project data or a private service; application-wide secret | [GCP credentials and operations](references/gcp-credentials.md) |
| End-user delegation, reconnect, refresh, rotation or disconnect | [OAuth lifecycle](references/oauth-lifecycle.md) |
| Native ADK authentication, Resume or managed Auth Manager | [Continuation contracts](references/adk-continuations.md) |
| Gateway/tool identity, public output or credential exposure | [Identity and output boundaries](references/identity-and-output.md) |
| Provisioning/repeating a lab, diagnosing access or model admission, preparing hosted release, or verifying cleanup | [Operations runbook](references/operations-runbook.md) |

Read [compatibility and evidence](references/compatibility-and-evidence.md) before adapting an SDK example or making a compatibility claim. Audit/recommendation mode may finish with a concrete design and gaps; it does not require generating an application.

## Implement the selected boundary

- Derive identity from a verified application credential. Scope sessions and resource lookups by that principal. Keep user IDs, secret selectors, tokens and arbitrary authenticated destinations out of model-controlled credential selection.
- Select credentials in trusted code with account/provider/client/scope/revision bindings appropriate to the chosen branch. Enforce operation permission separately from authentication and Cloud IAM.
- Keep long-lived payloads outside prompts, ordinary ADK state and public events. Project public fields explicitly; sanitise failures before framework logging; test every enabled exporter relevant to the change.
- Make the smallest coherent change with the project's interfaces and tests. Do not replace a customised service with the book example or impose its Calendar scope, one-call policy, secret layout, SQLite or development JWTs on an unrelated application.
- For real delegated OAuth, implement the browser/account/lifecycle requirements in the OAuth reference. If required integration prerequisites are absent, finish local work and report the precise unverified/blocked production boundary. Mock success cannot clear it.

The optional [public-text adapter](assets/public_text.py) is a complete, small starter derived from a tested response-boundary repair. Copy/adapt it only when the application's response contract benefits; it is **not** a secret redactor or a replacement for upstream credential exclusion. Its contract and limitations are in the identity/output reference.

## Permission and execution boundaries

<!-- shared:consequential-operations-brief -->
Inspection is read-only, and code generation authorises no deployment, paid
call or live test. Before any consequential operation (an API, billing or
quota change, a billable resource, a secret, IAM, a data migration, a
deployment, a deletion, or a paid or destructive test), read
[consequential operations](references/operating-rules.md#consequential-operations),
present the exact scope and limits, obtain explicit approval and end the turn
to wait for it. Cleanup is a separate confirmed operation on resources this
workflow created.
<!-- /shared:consequential-operations-brief -->

Secret-payload reads, token minting and live model/provider calls are separate actions, each needing its own approval.

## Validate and report

Follow [validation](references/validation.md) for the selected branch. Start with deterministic identity/credential/provider tests, then real ADK orchestration with only the model boundary substituted where possible. Run paid/live checks only under the approved isolated plan. Check replay, user isolation, later invocation/restart and failure handling when affected; add relevant canaries for credential exposure. Verify repeated execution preserves existing state. A static inspector finding is a review lead, not a proved exploit or a passing control.

Report changed files, exact commands and exit/test results, remaining manual steps, production gaps, version limits, created-resource inventory and confirmed cleanup status where applicable. Do not label a partially validated live integration complete.

<!-- shared:evidence-labels-brief -->
Label each result with its tier (`offline`, `local`, `live` or `release`) and
outcome (`pass`, `fail`, `blocked` or `not run`) as
[evidence labels](references/operating-rules.md#evidence-labels) defines them;
earlier, vendor and documentation-only results are `historical`,
`vendor-measured` or `guidance`, never this session's evidence.
<!-- /shared:evidence-labels-brief -->

Independent community project; not affiliated with or endorsed by Google. Provenance and measured limits: [compatibility and evidence](references/compatibility-and-evidence.md).
