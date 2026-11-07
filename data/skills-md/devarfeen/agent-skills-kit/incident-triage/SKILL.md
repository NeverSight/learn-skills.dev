---
name: incident-triage
disable-model-invocation: true
description: "Triage an incident or outage from evidence: timeline, ranked causes, mitigations, one note. Read-only, never touches production; not log reads. Staging fixes: /staging-fix; local: /diagnosing-bugs."
metadata:
  version: "0.2.2"
---

# incident-triage

incident-triage turns scattered incident evidence into a ranked, checkable picture fast, so the owner can decide what to do. It writes one incident note and proposes; the owner acts, and any code fix enters the normal factory path.

## Inputs

- **Evidence** — alerts, error messages, logs, graphs, screenshots, user reports, timestamps. The user supplies it. None → ask for the first alert and when it fired; nothing else blocks starting.
- **Environment** — production, staging, or local. Production → work only from pasted evidence.
- **Staging inspection approval** — this session's explicit approval plus the SSH access to use, for read-only checks (logs, `SELECT`s, container and env state). No approval → no staging access.
- **Recent changes** — merged PRs and deploys in the window: `gh pr list --state merged --base <branch> --search "merged:>=<start>" --json number,title,mergedAt,mergeCommit` and `gh run list --branch <branch> --json workflowName,conclusion,createdAt,headSha`. These read GitHub, not the environment.

## Rules

- **Production is never accessed.** No SSH, server commands, prod database, files, logs, env, or dashboards reached by the agent. If the next decisive fact lives in production, name the exact query or log line and ask the owner to run it and paste the result — ideally one sanitized failing request with its timestamp or request ID plus the matching app log lines.
- **Staging is read-only and approved.** Inspect staging only within this session's approval. Any mutating step — restart, rollback, config edit, data fix — is proposed to the owner, never run.
- **Propose mitigations, never apply them.** Every mitigation names who runs it, its expected effect, its risk, and how to undo it. Rollbacks go through a revert PR via `/staging-fix` for staging, or the owner's own process for production.
- **Hypotheses carry evidence both ways.** Each cause lists what supports it, what argues against it, and the one check that would confirm or kill it. Rank by evidence, not by how familiar the cause sounds.
- **A suspected breach changes the path.** Signs of unauthorized access, data exposure, or a leaked secret → tell the owner at once to start their security process, keep attack detail out of the note, and never test the exploit.
- **Time-box the first answer.** Give a first ranked picture within the first pass of evidence; refine as answers arrive instead of waiting for completeness.
- **Facts and guesses stay apart.** Timeline entries are observed facts with a source; inference goes in hypotheses.
- Redact before anything leaves the session: replace tokens, keys, cookies, session IDs, passwords, emails, and customer identifiers in quoted evidence with `<redacted>`, keeping only the lines that show the fault.
- **Zero attribution.** No co-author, AI, or tool attribution in the note or any output.
- Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`GLOSSARY-MAP.md` at repo root; legacy `CONTEXT-MAP.md`), else the repo root.
- Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.

## Workflow

### 1. Fix the window

Establish first-bad time, last-known-good time, and what is affected (users, routes, jobs, PROJECT-CODEs) from the evidence. Unknown start → use the earliest alert and say so.

### 2. Build the timeline

Merge evidence, merged PRs, and deploy runs into one ordered timeline, each line with time, event, and source. A deploy or merge shortly before first-bad is a lead, not a verdict.

### 3. Rank causes

List 2–4 hypotheses in the format from Rules, most-supported first. Include at least one that isn't a recent change — a shared dependency, a third-party provider, traffic or data shape, or an expired certificate, token, or quota. When several services fail together, rank the shared dependency first. For each, name the confirming check and whether the agent can run it (code reading, `gh`, approved staging) or the owner must.

### 4. Run the checks you can

Read the suspect diffs, the code paths in the stack traces, and approved staging evidence. Update the ranking as each check returns; drop a hypothesis only on evidence.

### 5. Propose mitigations and the fix path

Order mitigations from least to most invasive. When a recent merged change caused it, trace why its checks passed — the `agentic-qa`, `risk-review`, and `deploy-watch` markers on its PR — and suggest `/qa-escape` on its issue so the class is recorded. Then name the fix path: a ticket for `/factory` at `BUILDING`, `/staging-fix` for a staging-only fault, or owner action for production.

### 6. Write the note

Write `<artifacts-root>/specs/incidents/<YYYY-MM-DD>-<slug>.md`:

```
# Incident: <one-line symptom>

Zero attribution: never add or leave co-author, AI, or tool attribution in this note.
Status: investigating | mitigated | resolved — owner: <name>
Severity: SEV1–4 (owner confirms)
Window: <first-bad> → <now or resolved> · Impact: <who, what>

## Timeline
- 14:02 first 5xx alert on /checkout (Datadog alert, pasted)
- 13:55 PR #87 merged to staging; deploy run 9912 success (gh)
- — gap: 14:32–14:47 unknown

## Hypotheses
1. Credit-note query times out under load — for: trace shows 30s in InvoiceTotal; against: started before #87; check: owner runs EXPLAIN on prod replica

## Mitigations (owner decides)
- Revert #87 via PR — effect: removes new query; risk: loses fix for #418; undo: re-merge

## Open questions
```

Append to the same note as the incident develops; never create a second note for one incident. When status becomes `resolved`, append `## Resolution`: the confirmed cause and the evidence that confirmed it, contributing factors in blameless wording ("the check did not", not "X forgot"), and follow-ups each with an owner.

## Output

The note path, then at most 3 bullets: top hypothesis with its confirming check, the recommended first mitigation and who runs it, and the one question for the owner. Close with the `Suggested next skills (optional)` footer, 1–3 items: `/staging-fix`, `/diagnosing-bugs`, or `/factory` with the fix ticket.

## Completion criteria

- [ ] The note exists at the stated path and every timeline line names its source
- [ ] Every hypothesis has for, against, and one confirming check with who runs it
- [ ] Every mitigation names owner, effect, risk, and undo
- [ ] No server, production system, or staging write was touched by this run — only reads within approval
