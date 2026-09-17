---
name: polylane-automations
description: Author, scope, and operate Polylane automations — unattended agent runs wired as trigger → instructions → tools → actions → destinations. Use when the user wants something to happen without them — "whenever X happens", "on every deploy", "every morning", "auto-rollback if it breaks" — including reacting to alerts, incidents, deploys, pushes, cron schedules, or webhooks; rolling back bad deployments automatically; auto-triaging alerts into issues; scheduled reports and recurring production health checks; incident-response automation; and routing results to Slack, email, or webhooks. Retrieve from Polylane docs — never guess commands or schemas.
---

# Polylane Automations

An automation is an unattended agent run: a typed event fires, an agent executes your instructions with an allowed set of skills (tools), optional **actions** apply side-effects, and **destinations** deliver the result. Every piece is declarative JSON.

This file carries the model and the authoring process — not the type catalogs, which have live sources:

| Source | How to retrieve | Use for |
|--------|----------------|---------|
| API schema | `polylane api describe automations.post` | The authoritative request shape, every trigger/action/destination type and filter, for the installed API version |
| Public catalogs | `GET /v1/public/automations/{catalog,triggers/catalog,actions/catalog}` | Templates and type lists without auth |
| Docs | `https://docs.polylane.com/remediation/automations` (+ `/triggers`, `/actions`, `/destinations`, `/templates`; raw markdown at `/raw/...md`) | Concepts, examples, filter semantics |
| Template shapes | `polylane automation catalog --output json` | Full bodies to crib from |
| Attachable skills | `polylane skill list` | Slugs for `--tool` |

## The Shape

```
trigger(s) ──▶ [optional delay] ──▶ agent run (instructions + tools) ──▶ actions ──▶ destinations
```

- **Triggers** — typed events: `alert`, `cron`, `webhook`, `github.*`, `<provider>.deployment`, `slack.message`, `polylane.*` (issue.triaged, change_record.created, …). Platform triggers (`cron`, `webhook`, `polylane.*`) always work; provider triggers need the matching integration connected.
- **Instructions** — a plain-English job description the agent executes.
- **Tools** — Polylane skills (by slug) the agent may load during the run.
- **Actions** — side-effects the agent may apply: open issues, comment/merge/submit PRs, roll back deployments, queue autofixes, hand off to external coding agents.
- **Destinations** — where the result is delivered: `email`, `slack`, `webhook`.

**Modes** gate actions and destinations alike: `always` fires on every completed run; `smart` only when the run is judged noteworthy — except failures, which always deliver to destinations. Prefer `smart` for high-impact actions (merges, rollbacks).

**Every run is a thread** — the full transcript is inspectable. Execution states: `pending` → `delayed` → `running` → `completed` / `failed` / `skipped`.

## Constraints Worth Knowing

- Up to **10 triggers** per automation; each type at most once — except `cron` and `webhook`, which can repeat.
- `openIssue` respects the workspace's daily issue limit; plan-limit rejections are HTTP 426.
- Slack destinations need the Slack integration; webhook destinations time out after 10 s, and non-2xx records the delivery as failed.
- Rollback actions and their strategies are provider-specific — check `api describe` for the exact strategy names before writing one.

## Template or Custom?

```
├─ A catalog entry matches as-is → polylane automation from-template <slug>
├─ Close but too broad → crib its body (catalog --output json), narrow the trigger, create custom
└─ Nothing matches → polylane automation create (flags or --body-file)
```

Instantiated templates become fully editable automations.

## CLI Surface

```bash
polylane automation catalog                        # browse templates
polylane automation from-template <slug>           # instantiate
polylane automation create \
  --name "Triage Datadog alerts" \
  --trigger '{"type":"alert","filters":{"sources":["datadog"],"severities":["critical"]}}' \
  --instructions "Correlate the alert with recent deploys and open an issue with the findings." \
  --tool investigate-errors \
  --action '{"type":"openIssue","mode":"smart","defaultSeverity":"high"}' \
  --delay 600000                                   # let a deploy settle before judging it

polylane automation trigger <id>                   # manual run
polylane automation executions <id>                # then: execution <id> <execution-id>, rerun
```

`--trigger` / `--action` / `--destination` take JSON (repeatable), or a bare type for filterless ones (`--trigger webhook`). `--tool` attaches a skill by slug (repeatable). `--body-file` passes a full JSON body (`-` = stdin); flags layer on top. Every flag: `polylane automation create --help`.

## Authoring Checklist

Work through every item; the automation is done when a manual run has produced the intended outcome.

1. **Catalog first** — only go custom when nothing fits.
2. **Scope the trigger** — filter by environment, source, severity, or repository; an unfiltered trigger runs on everything. Prefer `polylane.issue.triaged` over raw `alert` when the automation should act only on confirmed problems.
3. **Instructions read like a runbook** — what to investigate, what evidence to gather, what a good outcome looks like.
4. **Attach only the skills the job needs.**
5. **Gate risky actions with `smart` mode**, and add a `--delay` on deploy-adjacent triggers.
6. **Wire a destination** — results nobody sees are results nobody acts on.
7. **Test with a manual run** — `automation trigger`, inspect the execution's thread, iterate on the instructions until the run does what the user asked.
