---
name: cryptpad
description: >-
  Use CryptPad encrypted collaboration for integration, automation, and diagnosis with its
  browser integration API, instance discovery, document import/export, and
  session-key lifecycle. Use for CryptPad API feasibility, embedded editors,
  sharing, persistence, or self-hosted instance troubleshooting. Do not use for
  EncryptPad/OpenPGP, generic office-file conversion, or designing an unrelated
  collaboration service.
license: MIT
compatibility: Python 3.10+ for discovery tools; a browser and a compatible CryptPad instance for editing; Node.js for adapter tests.
---

# CryptPad

## When not to use

- For local office-file creation or conversion, use `documents` or `anydoc`.
- For general API contract design, use `api-design-and-evolution`.
- For container operations, use `docker-compose`; keep CryptPad-specific configuration here.
- EncryptPad is a different OpenPGP desktop application.

## Workflow

1. Establish the instance origin, deployed version, document application, and task:
   existing CryptDrive content, embedding an externally stored document, or instance operations.
   Never infer rights from a title, successful HTTP request, or editor UI alone.
2. Read [architecture and interface boundaries](references/architecture.md) for feasibility.
   Prefer the documented browser integration API for external storage; use an authorized
   browser session for existing CryptDrive documents. Do not invent bearer-token CRUD routes.
3. For public instance discovery, run the CLI below. For an embed, read
   [integration contracts](references/integration.md), then use the adapter and plan templates.
   For self-hosting failures, read [operations](references/operations.md).
4. This skill can guide actions that change external state: editing, importing, sharing,
   key rotation, deployment and retention changes.
   **Confirm the target, scope, and rollback path before acting. Read-only discovery may proceed without confirmation.**
   Use existing explicit authorization when it covers these details. Destructive operations
   still require an explicit user directive. Prepare reversible work before escalating gaps.
5. Verify the result on the normal browser path: document loads, edits synchronize,
   the save reaches durable storage, and a fresh session reopens the saved content.
   Check view-only access with a real view key. HTTP discovery is not this verification.
6. Deliver the artifact or diagnosis, with version/source evidence, tests actually run,
   and remaining limitations. Stop after three non-converging diagnostic passes and report
   the exact failed boundary and next required evidence. Do not substitute raw ciphertext
   for exported document content or claim a schema-valid eval proves runtime behavior.

## Tools

Run from this skill's root; tools use only Python's standard library and output JSON.

```sh
python3 scripts/cryptpad.py probe --origin https://cryptpad.example.org
python3 scripts/cryptpad.py inspect-link < /secure/path/document-link.txt
python3 -m unittest discover -s scripts -p 'test_*.py'
```

[CLI](scripts/cryptpad.py): `probe` GETs `/api/config` and `/cryptpad-api.js`, refuses
redirects, bounds response size and timeout, and parses only JSON inside the known AMD
wrapper without executing JavaScript. Exit 0 means both resources were recognized,
1 means incomplete discovery, 2 means invalid input. `enableEmbedding: false` is a
configuration finding, not a network failure. No version or end-to-end health is inferred.

`inspect-link` is offline and reads stdin to avoid putting capability links in argv.
It reports only origin, known application and presence of query/fragment, never their
values or arbitrary paths. It does not validate the key or determine effective rights.
Keep the input file protected; do not paste real keys into logs or shell history.

[Tests](scripts/test_cryptpad.py) exercise malformed input, secret redaction, response
recognition, failure handling, and save/key callbacks. Node.js enables the adapter test;
without it that test is explicitly skipped.

## Integration essentials

- Load the instance's `/cryptpad-api.js`; call `window.CryptPadAPI(containerId, config)`.
  This is a browser API, not a server-side REST document service.
- The embedding service owns durable storage, user authorization and session-key sharing.
  Integration sessions are transient; normal CryptDrive persistence is a separate workflow.
- Default to CryptPad-generated session keys with `onNewKey`. Atomically compare the old
  stored key and persist the winning edit/view pair. Return the winning edit key to the
  callback even when a concurrent update won. Never return each client's candidate blindly.
- `onSave` receives a Blob. Acknowledge only after a durable save. Preserve visible unsaved
  state on failure; retries need idempotent or revision-aware storage.
- `mode: 'view'` with an edit key only locks the UI. Use a real view key, and do not expose
  edit keys through the view user's storage API. Verify feature support on the deployed version.
- Removing an application ACL entry does not terminate a running key-bearing session.
  Plan rotation and migration to a fresh session; do not claim retroactive secrecy.
- E2EE on CryptPad's side does not encrypt your application's stored exports. If E2EE is
  required, encrypt/decrypt in the trusted client and design key distribution accordingly.

## Templates and evidence

- Use [integration plan](templates/integration-plan.md) to define storage, key ownership,
  authorized changes and acceptance tests before implementation.
- Adapt [callback adapter](templates/integration-adapter.mjs) for application-owned persistence
  and atomic key updates. It supplies no backend, credentials or encryption scheme.
- Use [browser configuration example](templates/browser-integration.md) to wire the adapter
  to the documented API. It is a scaffold requiring real application services.
- Record source revisions and compatibility using [research sources](references/sources.md).
- [Output-quality cases](evals/evals.json) cover integration and diagnostic behavior.
  [Trigger probes](evals/trigger-queries.json) are separate harness inputs.
