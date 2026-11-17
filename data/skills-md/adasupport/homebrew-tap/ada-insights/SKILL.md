---
name: ada-insights
description: Investigate an Ada agent's real conversations, AI reasoning, topics, and coaching with adacli to find what it gets wrong and where knowledge/playbook gaps are. Use when the user asks why the agent failed a conversation, what customers ask, where resolution is low, or to diagnose/triage agent behavior.
require-tools:
  - Bash
  - Read
---

# Finding what the agent gets wrong

The conversation + reasoning + topic + analytics data is the map of what customers don't
understand and where the agent fails. Use it to diagnose, not just report.

## Start from analytics, narrow to conversations

```bash
adacli <instance> analytics summary --json                  # ClickHouse resolution, volume, and CSAT
adacli <instance> analytics topics --json                   # ClickHouse topic performance
adacli <instance> topics generated list --json              # AI-generated topics
adacli <instance> conversations search --resolution not-resolved --since 30d --all --limit 500 --json  # the failure cohort
adacli <instance> conversations search --topic <t> --csat 1 2 --all --limit 500 --json  # low-CSAT in a topic
adacli <instance> conversations recent --json               # newest first (40-row default cap); see the canonical recent note in the `adacli` skill
```

The `--resolution` (resolved|not-resolved|unclear), `--csat`, `--handoff`, `--channel`, and
`--language` filters let you assemble a failure cohort server-side instead of scanning by hand.
A bare `search` returns a single page; add `--all --limit <n>` to page the whole cohort. See the canonical `--all` note in the `adacli` skill for the walk exit-code behavior.

## Why the agent hands off

Read counts first. Each command below returns numbers or a few ids, not whole conversations.

```bash
adacli <instance> conversations handoff-reasons --since 7d --count --json      # conversations per reason, sorted
adacli <instance> conversations handoff-reasons --since 7d --samples 5 --json  # + 5 sample ids per reason
adacli <instance> conversations handoff-reasons --handoff-reason tool_failed --with-reasoning   # + short redacted reasoning
adacli <instance> conversations search --handoff-reason tool_failed --since 7d --all --limit 50 --json   # the cohort
adacli <instance> conversations handoffs <id> --json                           # one conversation's attempts
```

Each handoff attempt has a `reason_code` (one of ten values, or `null`) and a `reasoning` text.
The ten values are `tool_failed`, `end_user_requested`, `out_of_scope`, `tool_unavailable`,
`knowledge_unavailable`, `issue_unresolved`, `handoff_configured`, `other`, `system_failed` and
`unclassified`. Each report row, and `handoff_reason` in `conversations diagnose`, has a
`fix_surface`: `tool` (fix or add a tool), `knowledge`, `routing` (the playbook or handoff that
sends it to a person), `system` (report to Ada), `none` (usually correct) or `unknown`.

- A reason belongs to an **attempt**, which can fail. For escalation, use `--handoff` (the
  `HANDOFF` filter); the report shows it as `totals.escalated`.
- `null` means no code was recorded. It is not `unclassified`.
- Unified Reasoner v2 agents record `unclassified` for handoffs outside Playbooks. A Playbook
  handoff step records `unclassified` until the system assigns its reason after a save.
- `reasoning` is often `null`. Do not expect it. Use the `reason_code`, the target, the outcome
  and the transcript.
- Read `reasoning` only through these commands. They use the transcript API, which applies the
  account's redaction rules. Do not quote it from `conversations reasoning --json`.

## Drill into a single conversation

```bash
adacli <instance> conversations details <id> --json     # resolution, summary, guidance, coaching, handoffs, metavars
adacli <instance> conversations transcript <id> --json  # what was said
adacli <instance> conversations reasoning <id> --json    # WHY: AI reasoning + which articles/playbooks fired
adacli <instance> conversations coaching <id> --json     # coaching items triggered
```

The `reasoning` log is the key artifact: it shows which knowledge was retrieved and which
playbook/guidance applied — so you can see whether a failure was missing knowledge, a
mis-firing playbook, or a knowledge gap.

These single-id readers (`reasoning`, `transcript`, `log`, `details`, `guidance`) exit `22` on a
degraded read — see the canonical exit-22 note in the `adacli` skill: retry the read, do not
treat the empty result as a finding.

**Shortcut — let adacli draw the conclusion:**

```bash
adacli <instance> conversations diagnose <id> --json
```
`diagnose` deterministically joins the reasoning + resolution evidence into a typed verdict:
`surface` (knowledge | playbook | guidance | handoff | unknown), the `target` id to fix, a
`confidence`, and a `why`. Its `handoff_reason` names the latest recorded handoff reason and
its `fix_surface`. Use it instead of hand-classifying every conversation. (adacli names
the surface; *you* author the fix — see **ada-optimize** to close the loop.) A `surface` of
`unknown` means the read was unverifiable (exit `22`): retry the read, do not author a fix
(canonical exit-22 note in the `adacli` skill).

## A practical "where are the gaps" pass

1. `analytics topics --json` → rank topics by volume × low resolution.
2. For the worst topic, `conversations search --topic <t> --all --limit 500 --json` → sample several.
3. For each sample, `conversations reasoning <id> --json` → classify the failure:
   - no relevant article retrieved → **knowledge gap** (fix via **ada-knowledge**)
   - wrong/again-and-again playbook → **playbook issue**
   - right info, wrong behavior → **guidance issue**
4. Summarize the pattern + the specific fix for the user. Don't change anything without
   showing the diagnosis first.

## Review recommended intents

The classifier proposes intents for conversations no active intent covers.

```bash
adacli <instance> topics class recommendations --json          # candidates, by volume and gap share
adacli <instance> conversations search --intent <intent-id> --all --limit 20 --json  # sample one
adacli <instance> topics class recommendations approve <intent-id> [--name ...]   # preview; add --yes to apply
adacli <instance> topics class recommendations dismiss <intent-id>               # preview; add --yes to apply
adacli <instance> topics class intents update <topic-id> <intent-id> --included "..."  # refine an active intent
```

Approve, dismiss and update change the live taxonomy. Show the user the sampled evidence and
the preview first, and run `--yes` only after they agree.

## Rules

- This skill is **read-only** — it diagnoses. Make changes via **ada-knowledge**,
  `guidance`, or `playbooks`, and validate with **ada-test-agent**.
- Conversation data can be large/PII-bearing — sample a bounded set, don't dump everything.
- Cite specific conversation ids and reasoning evidence in your findings.
