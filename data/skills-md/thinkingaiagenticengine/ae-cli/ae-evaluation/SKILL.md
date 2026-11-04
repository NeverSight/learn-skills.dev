---
name: ae-evaluation
version: 2.4.5
description: "Operate the Agent Evaluation (agent-test) platform through ae-cli: manage evaluation assets, configure and run Agent or preset-output evaluations, and analyze results. Use for platform evaluation tasks and their model, credential, integration, or schedule setup."
---

# ae-evaluation

Use `ae-cli evaluation +<command> [options]` for existing operations and the resource commands below for new capabilities. All 121 commands target the Agent Evaluation platform.
AE Agent resource management belongs to `ae-agent`; this skill manages evaluation assets and agents under test.

## Read only the relevant reference

Before executing a command, read the reference for the operation. Do not load all references.
References contain command inputs, JSON contracts, and task-specific workflows; use command `--help` for additional flags.

| Task | Reference |
|---|---|
| Create/import datasets, manage fields and cases, publish versions | [datasets.md](references/datasets.md) |
| Configure LLM judges/templates, publish evaluator versions, calibrate or optimize prompts | [evaluators.md](references/evaluators.md) |
| Create/configure/start/retry/cancel runs, inspect results/traces, export results | [runs.md](references/runs.md) |
| Configure/test models and agents, manage credentials | [connections.md](references/connections.md) |
| Change resource visibility or administer project members | [access-and-members.md](references/access-and-members.md) |
| Download imported/exported files to disk | [files.md](references/files.md) |
| Create/update/delete recurring evaluation schedules | [schedules.md](references/schedules.md) |
| Connect/import AI Monitor data, configure TE reporting, discover TE Claude catalog | [integrations.md](references/integrations.md) |

## Endpoint and authentication

- In both personal terminals and AE sandboxes, evaluation commands default to the current AE Host and call `<current-host>/agenteval/api/v1/...` (an optional trailing `/agent` is removed from the host). Use `--host` to select another AE Host. Evaluation requests use the HTTP or HTTPS scheme configured for that AE Host, consistent with other AE commands. Legacy `--endpoint` and `AE_EVAL_BASE_URL` values may only match the current AE Host; other values fail before credentials are sent. Remove these settings and use `--host` to select a host.
- Session exchange and evaluation requests reject redirects; session exchange has a 30-second timeout.
- Path resource IDs must contain only letters, digits, hyphens, or underscores; separators and URL escape syntax are rejected locally.
- Use the online platform. Do not suggest localhost/loopback endpoints or obtain tokens from a local `agent-test/.env`.
- Authentication uses `AE_EVAL_ACCESS_TOKEN` when explicitly set; it is sent only as `Authorization: Bearer` and must never appear in command arguments or output.
- In an AE sandbox, when `AE_EVAL_ACCESS_TOKEN` is unset, ae-cli automatically exchanges the sandbox-provisioned `cli-token` through te-claude for a short-lived evaluation session. The CLI token is never sent to Agent Evaluation. If the token can access multiple TE projects, set `AE_EVAL_TE_PROJECT_ID` to the authorized TE project id.
- Outside a sandbox, obtain a session token through the platform web console (`sessionStorage.getItem('agent.evaluation.session-token')`) or `POST /agenteval/api/v1/auth/session`. An unset token produces `EVAL_ACCESS_TOKEN_MISSING`.
- Successful commands return JSON by default; use the actual error envelope to diagnose failures.

## IDs, versions, and mutations

- Discover real IDs with list/get commands. UUIDs are version-7 strings; never guess IDs, JSON payload shapes, frequency fields, or `lock_version` values.
- Published dataset, evaluator, and evaluation-task versions are immutable and separate from drafts. Runs and schedules pin versions; existing published versions cannot be overwritten. Publishing unchanged assets returns `ASSET_VERSION_NO_CHANGES`.
- Read operations can run once inputs are known. Writes require user intent; high-risk operations retain confirmation unless the user authorizes bypassing it with `--yes`.
- Credential enabling/disabling, run cancellations, deletes, ownership transfers, template disabling, access-scope changes, and member admission/permission changes are high-risk writes. Check command help for risk and role requirements; references identify ADMIN-only operations.
- Before each mutation requiring `--lock-version`, read the current resource. Every successful mutation increments its version; re-read before the next mutation.
- Use the corresponding get command for runs, datasets, evaluators, models, agents, credentials, dataset cases, TE report config, and AI Monitor connection. Schedules use `+list_schedules`; calibration cases use `+list_calibration_cases`.
- Field mutations use the dataset version; case mutations use the case version. First creation of TE report config or AI Monitor connection omits `--lock-version`; updates require the current value, including 0.
- Async dataset imports, evaluation-set imports, and result exports require a fresh unique `--idempotency-key` per attempt. Poll the relevant status until completion; resource creation alone does not establish readiness.
- Prefer `--dry-run` before broad/destructive writes whose targets have not been validated. It previews the request without executing it.
- Evaluation errors redact the submitted credential values and session tokens; server-provided error messages and hints are not persisted in CLI logs. Stable business error codes are preserved unchanged; non-sensitive diagnostics remain available in the JSON error envelope.
- Case data is redacted from command logs for both single-case and batch writes. Sensitive JSON parse failures report the flag and syntax guidance without echoing the input.
- Credential secrets are write-only. Never echo secrets, session claims, or sensitive trace evidence; use redacted dry-run output.

## Evaluation lifecycle

1. Select a published dataset version with `+list_dataset_versions`.
2. Choose `LIVE_AGENT` (default) to call an Agent/model, or `PRESET_RESULT` to score outputs stored in the dataset. PRESET_RESULT must omit agent/model config IDs. `IMPORTED_OUTPUT` is legacy data only; never recommend it.
3. Create a draft run, bind at least one ACTIVE evaluator (prefer pinned published versions), and configure complete field mapping plus result filter fields. An explicit empty result filter is required when no fields are selected.
4. Prefer `+validate_run` before starting. It runs the start preflight without a body or lock version. Read the latest run, then `+start_run` with its current lock version.
5. Inspect overview/distribution, drill into cases, and use the run reference for retry, trace, and export semantics.

Read [runs.md](references/runs.md) for the executable sequence and mapping examples. Setup of datasets, evaluators, or connections needs only the matching reference above.

## Transport transition

The existing platform contract exposes REST operations rather than evaluation
capabilities registered in this repository. New commands retain that transport
for typed input, permission confirmation, and file handling. They are Transitional;
see the matching references for migration records. Check deployment Gateway
coverage before extending these commands; prefer existing equivalent capabilities.

Transition status: transitional
Owning module: Agent Evaluation (agent-test)
Current transport: authenticated REST /agenteval/api/v1
Gateway target: TBD (evaluation capability registration)
Review after: 2027-01-21
Exit condition: once equivalent evaluation capabilities are available, migrate
selected typed/file commands to L2 or replace simple wrappers with L3; retain
existing + commands only where compatibility or orchestration justifies them.

This record also applies to the locale and process-evidence updates in the
existing evaluator/run references. It is a migration plan, not a claim that a
particular deployed Gateway has been inspected.
