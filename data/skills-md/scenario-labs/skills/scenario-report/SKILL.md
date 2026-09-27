---
name: scenario-report
description: "Use when a Scenario user wants to report a bug or request a change, on the public tracker at github.com/scenario-labs/skills or by email to support@scenario.com: turning a failed generation, MCP tool error, or unclear skill into a reproducible report, collecting trace ids with diagnostics_run, stripping keys, signed asset URLs, and personal data, asking before sharing a team or project id, or building a prefilled issue URL. Keywords: file an issue, feature request, feedback."
license: MIT
---

# Reporting Scenario bugs and change requests

## Overview

Public tracker: `https://github.com/scenario-labs/skills/issues`, forms `bug.yml` and `change-request.yml`. Offer `support@scenario.com` as the private alternative, and let the user pick.

Two constraints. A public issue is permanent, so redact first and post only after the user approves the exact text. The reader has no access to the user's account, so the report must carry everything needed to reproduce from outside.

Connection and the core generation loop: see the `scenario` skill in this repo. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

Account, billing, credit, quota, sign-in, and security problems never go in a public issue: send those to `support@scenario.com` or in-app support at `app.scenario.com`.

## Quick reference

| Step     | Do                                                                |
| -------- | ----------------------------------------------------------------- |
| Classify | bug or change request, one problem each                           |
| Gather   | failing call, verbatim error, `diagnostics_run` from that session |
| Redact   | strip identity and secrets; ask before any team or project id     |
| Dedupe   | search open and closed issues, comment on a match                 |
| Draft    | fill every field, label guesses as guesses                        |
| Approve  | show the final text, post only on a yes                           |
| Post     | GitHub tool, prefilled URL, or email                              |

## Redact before drafting

Never include API keys or tokens, signed URLs from `asset_download` (the URL is a credential), account emails or names, local paths containing a username, or unreleased art, prompts, and model names the user has not agreed to publish.

Team and project ids identify the account, so strip them by default. Ask for one only when it changes the diagnosis (a Forbidden or scope error, a model only one team can see): quote the id you would post, and treat anything short of a yes as no. Email is the better home for it.

`diagnostics_run` is the best evidence and the biggest leak: `self_test.detail` can enumerate every team and project the user belongs to, and `tenant` can encode their account. Copy only `version`, `endpoint`, `auth_type`, `self_test.layer`, `self_test.latencyMs`, `generated_at`, and the ids under `confirmed_trace_ids` and `candidate_trace_ids`. Nothing else from that report.

Job, asset, and model ids match the report to a server-side request: include them with the user's agreement. Signed download URLs, never.

## Make it reproducible

Name the model id and whether `search` finds it with `public=true`, the exact `parameters` sent to `model_run`, the verbatim error, the UTC timestamp, and at least one trace id. Substitute a short public prompt for a confidential one and say so. Say when a model is team-private: the reader reproduces against a public equivalent.

## Worked example: a texture upscale that never finishes

1. `diagnostics_run` in the failing session, keeping only the fields listed above and the trace ids.
2. Re-run the failing call once: arguments, verbatim response, UTC time. Check with `search` whether the upscaler is public, so the reader can run it too, then search the tracker, open and closed, for `jobs_wait pending`.
3. Draft. Title: `jobs_wait keeps returning the same texture upscale job in pending_job_ids for 20 minutes`. Steps: the `model_schema_get`, `model_run`, and repeated `jobs_wait` calls with their arguments. Expected: the job completes or fails. Actual: `status` stays `in_progress`, `pending_job_ids` unchanged. Evidence: job id, trace ids, timestamp.
4. Show the user the full text, and post only on a yes.

## Posting

- With GitHub tooling: search `repo:scenario-labs/skills` for duplicates, then create the issue with the label `bug` or `enhancement`, mirroring the form headings in the body.
- Browser only: build `https://github.com/scenario-labs/skills/issues/new?template=bug.yml&summary=...&repro=...`, percent-encoding each value. Parameter names are the form field ids: `summary`, `area`, `repro`, `expected`, `actual`, `evidence`, `env`, `frequency`; change requests switch to `template=change-request.yml` and use `problem`, `area`, `today`, `proposal`, `impact` (a param matching no field id on the selected form is dropped silently). The user ticks the confirmation boxes and submits. Past about 8000 characters the URL returns 414: drop `evidence`.
- By email: `support@scenario.com`, subject `[bug] <title>` or `[change request] <title>`, body carrying those same fields as labeled lines. Whatever was withheld from a public issue (team id, project id, account email) travels safely here.

## Common mistakes

- Pasting the whole `diagnostics_run` output, which leaks the team and project list.
- Publishing a team or project id nobody asked for, or asking for one the diagnosis does not need.
- A title like "generation is broken": name the surface, the symptom, and the condition.
- Three problems in one issue: each needs its own reproduction and its own close.
- Reporting the hypothesis ("the API is down") instead of the observation. Observation first, hypothesis last and marked as one.
