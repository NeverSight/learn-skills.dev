---
name: crm
description: >-
  Operate HubSpot CRM from a terminal or agent: list and search contact
  records, view deal pipeline stages, and — with explicit confirmation — move
  deals between stages, backed by a bundled crm-cli script that is read-only
  by default and gates every stage change behind a --dry-run/--yes
  confirmation. Use when an agent needs to answer questions about contacts or
  deals, produce pipeline views, or apply a confirmed stage change. Do not use
  for building HubSpot apps or workflow automations (that is HubSpot app
  development), marketing/sequence automation, or other CRMs like Salesforce
  (that is their own tooling).
license: MIT
compatibility: >-
  The bundled crm-cli script runs on Python 3.9+ with only the standard
  library. --help and all reads need no network beyond api.hubapi.com; live
  reads require a HubSpot private app access token with the relevant object
  scopes (crm.objects.contacts.read, crm.objects.deals.read) and network
  access to api.hubapi.com.
metadata:
  source: https://developers.hubspot.com/docs/api/crm/understanding-the-crm
  source_index: references/00-source-index.md
  research_checked: "2026-08-03"
---

# HubSpot CRM Operations

Use this skill to read and, with explicit confirmation, update HubSpot CRM data through the HubSpot CRM v3 API: contact records, contact search, deal pipeline views, and deal stage changes. This is a **tool skill** for one CRM vendor (**HubSpot**). Building HubSpot apps or workflows is application development; this skill owns the everyday agent workflow: answering "who is this contact?", "what is in the pipeline?", and applying a confirmed stage change.

## Operating contract

1. **Read-only discovery before any mutation.** List and search contacts, view deals and pipelines freely. The bundled `crm-cli` script makes reads without writing anything.
2. **Confirm the target, scope, and rollback path before acting.** Moving a deal to a new stage changes a shared pipeline that revenue reporting reads: it requires an explicit human directive naming the deal and the target stage, plus `--dry-run` preview and `--yes` confirmation through `crm-cli`. Stage moves are reversible but leave audit history — confirm before acting.
3. **Respect bounded reads.** HubSpot pages with `limit`; never page past what the task needs. `crm-cli --limit` caps every listing and search.
4. **Keep evidence bounded.** Quote short names, emails, amounts, and stage labels; never dump full records, tokens, or raw payloads into chat.
5. **Know the object model.** Contacts and deals are distinct objects with property maps; stage transitions must use a stage ID from the deal's pipeline (`pipelines list`), not a stage label.

## The crm-cli script

`scripts/crm-cli` is an agent-first, stdlib-only CLI over the HubSpot CRM v3 API. It covers the full issue scope: records, search, and pipeline views.

```bash
crm/scripts/crm-cli --help                                # no token or network needed
crm/scripts/crm-cli --json --limit 20 contacts list
crm/scripts/crm-cli --json contacts get --id 51
crm/scripts/crm-cli --json contacts search --query "ada"
crm/scripts/crm-cli --json --limit 20 deals list
crm/scripts/crm-cli --json deals list --pipeline default --stage appointmentscheduled
crm/scripts/crm-cli --json pipelines list
crm/scripts/crm-cli deals update-stage --id 901 --stage closedwon --dry-run   # preview
crm/scripts/crm-cli deals update-stage --id 901 --stage closedwon --yes       # confirmed
```

Exit codes: 0 success, 1 API error or failed check, 2 usage error. Stage changes are guarded: without `--dry-run` or `--yes` the script refuses with exit 1 and never calls the API. Reads are bounded by `--limit` (default 20, max 100).

## Operating loop

1. **Scope the question**: is this a lookup (who/what is in the CRM) or a change (move a deal)? Locate the object with `contacts search`/`contacts list` or `deals list`.
2. **Read with bounds**: `contacts get` for one record, `deals list` for the pipeline view (optionally filtered by pipeline and stage), `pipelines list` to resolve stage labels to IDs.
3. **Triage the answer**: map the question to evidence (contact details, deal amount/stage, pipeline distribution).
4. **Act with confirmation**: only a human directive to change, previewed with `--dry-run` and confirmed with `--yes`.
5. **Verify**: re-read the deal (`deals list --stage <target>`) and confirm the stage moved.

## Records, search, pipeline views

- **Contact records** (`/objects/contacts`): list (GET) or retrieve one (GET by ID); the CLI summarizes first/last name, email, company, and created date. Search (`POST /objects/contacts/search`) finds contacts by query text, bounded by `--limit`.
- **Deal pipeline views** (`/objects/deals`): list deals with amount, pipeline, and stage, optionally filtered to one pipeline or stage. `pipelines list` (`/pipelines/deals`) returns the pipelines with their stage IDs and labels — use the stage ID when filtering or updating.
- **Stage changes** (`PATCH /objects/deals/{id}`): a guarded mutation that sets the `dealstage` property. Preview the target stage with `--dry-run`, confirm with `--yes`, and verify with a follow-up read. Only stage moves are in scope; other deal property edits are application work.

## Access model

- HubSpot private app access tokens (`pat_...`) scope per object and read/write. Reads need `crm.objects.contacts.read` and `crm.objects.deals.read`; stage updates need `crm.objects.deals.write`.
- Records carry a `properties` map keyed by property names (e.g. `dealstage`, `dealname`, `amount`). Property values are strings; the CLI summarizes the fields this skill uses.
- Tokens are credentials: store in `HUBSPOT_TOKEN`, never in code, chat, or commits. Rotate a leaked token in the private app settings.

## Reference routing

| Load when | Reference |
|---|---|
| Sources, scope tables, refresh procedure | `references/00-source-index.md` |
| Endpoints, pagination, object model, stage updates, errors | `references/01-hubspot-crm-operations.md` |

## Included artifacts

- `scripts/crm-cli`: bounded, stdlib-only CLI (contacts list/get/search, deals list/update-stage, pipelines list; `--json`; `--limit`; mutations gated by `--dry-run`/`--yes`).
- `tests/test_crm_cli.py`: 13 deterministic tests against a stub HubSpot API, including the mutation gate and the read-only contract.
- `references/`: dated source index + HubSpot CRM operations reference.
- `evals/evals.json`: six output-quality evaluation cases for agent runs.

## Verification boundary

| Claim | Minimum evidence |
|---|---|
| A contact exists | `crm-cli contacts search --query ... --json` or `contacts get` returns the record |
| A pipeline view is accurate | `crm-cli deals list --json` returns deals with stage IDs and the filter applied |
| A stage label maps to an ID | `crm-cli pipelines list --json` returns the pipeline stage map |
| A stage change landed | `crm-cli deals update-stage --yes` exits 0 and a follow-up `deals list --stage` shows the deal |
| A mutation is safe to run | `crm-cli deals update-stage --dry-run` prints the exact deal + target stage |

## Hard boundaries

- Never move a deal without a human directive, `--dry-run` preview, and `--yes` confirmation — pipeline changes feed revenue reporting and audit history.
- Never claim a record is missing when the token may lack object scope; check the access model first.
- Never page reads past `--limit`; never dump full records, tokens, or raw payloads into chat.
- This skill operates the HubSpot CRM API. It does not build HubSpot apps or cover other CRMs.

## When not to use

- **Building HubSpot apps, workflow automations, or custom objects** — that is HubSpot app development; see [backend-engineering](../backend-engineering/SKILL.md) for service design.
- **Marketing, sequences, and email automation in HubSpot** — that is the HubSpot Marketing surface, not the CRM API this skill covers.
- **Other CRMs** (Salesforce, Pipedrive, Zoho) — each has its own API and tooling; this skill covers HubSpot.
- **CRM strategy, sales process design, or pipeline methodology** — that is organizational/strategy work, not an API operation.
