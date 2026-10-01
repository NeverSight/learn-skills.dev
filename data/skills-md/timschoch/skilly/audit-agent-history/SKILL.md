---
name: audit-agent-history
description: Mine the user's own agent session logs per model and per harness, count failure modes, and propose the top three as hazard rules. Use when the user asks to audit, review or mine agent history, session logs or transcripts for mistakes, failure modes or corrections, or asks why an agent keeps doing X.
---

# Audit agent history

Rules written from guesses miss. Rules written from counted corrections in the user's own logs hit. This skill counts, then proposes at most three lines for `bundles/workflow/rules/workflow-hazards.md`, plus the consumer overlay pairs worth hoisting into their hub rule.

## Where the logs live

Verify each path with `ls` first. Skip what is absent, say so in the report.

| Harness | Path | Shape |
| --- | --- | --- |
| Claude Code | `~/.claude/projects/<project-slug>/*.jsonl` | one file per session, one JSON message per line; `type` is `user` or `assistant`; `cwd` names the repo; assistant lines carry `model` (`claude-fable-5`, `claude-opus-5`) |
| Codex | `~/.codex/sessions/<yyyy>/<mm>/<dd>/rollout-*.jsonl` | one file per session; first line `type: session_meta` with `cwd`; later lines carry `model` (`gpt-5.6`) |

The project slug is the repo path with `/` replaced by `-`: `/Users/x/repo/skilly` becomes `-Users-x-repo-skilly`.

## Scope

Ask for, or default:

- repos: which `cwd` values; default all
- window: default 30 days, by file mtime or `timestamp`
- models: default all seen

Run the whole audit in one subagent. It is deep reasoning over many logs. Raw logs never enter the main context, see [principle-guard-the-context-window](.agents/skills/principle-guard-the-context-window/SKILL.md). The subagent returns the report only.

## Method

1. **Count sessions and user messages** per model and harness. Both are denominators for step 4.
2. **Find corrections**: a user message that follows an assistant action and reverses it. Match on `no`, `don't`, `stop`, `I said`, `why did you`, `undo`, `revert`, `not what I asked`, `I didn't ask`. Read the two messages before each hit to drop false positives (a `no` that answers a question is not a correction).
3. **Classify** each correction into one mode from [references/failure-modes.md](references/failure-modes.md). One mode per correction. Unmatched goes to `other` with a two-word label.
4. **Count** per model per mode. Normalise: `corrections / user messages * 100`. Raw counts favour the model used most.
5. **Quote** two real examples for each of the top three modes: the assistant action and the user's correction. Redact secrets and every path under the home directory (`~/...`).
6. **Interrogate one bad thread.** Open the worst session in its own agent with the same model and ask: what gave the indication this was right, which line in the rule file or `CLAUDE.md` was outdated, where was the request misread first. Record the answer under the mode it explains.
7. **Interrogate one slow thread.** Take the session with the most tool calls per user message. Group its tool calls into categories (orientation reads, repeated reads, checks, edits, verification). Mark the groups that changed nothing about the result as useless.
8. **Collect overlay pairs.** In each repo in scope, read `.claude/rules/*.local.md`. These hold the bad/good pairs consumers wrote under a synced rule, see `.claude/rules/workflow-writing-standards.md`. A pair that appears in two or more repos, or matches a top-three mode, is a hoist candidate for the rule it extends.

## Output

Report table, one row per model and mode, sorted by per-100 descending:

```
| mode | model | count | per 100 messages | example |
```

Then a `## Proposed hazards` block. At most three rules in the format of `bundles/workflow/rules/workflow-hazards.md`: one numbered line, `Never` plus the action, then the reason. Each rule carries one bad and one good example from the logs.

```
1. Never kill a process by port number alone. Two harness instances share a port range; the audit found four kills of the running session in two days. Bad: `kill $(lsof -t -i:3000)`. Good: `ps -o pid,command | grep <name>`, then kill the one pid.
```

Then a `## Hoist candidates` block: one line per overlay pair, naming the repo, the rule file and item it extends, and the pair verbatim.

Then hand-off:

- Show the report and both blocks to the user. Stop.
- On sign-off, edit the rule files under `bundles/workflow/rules/` in the hub repo (`timschoch/skilly`) only. Never in a consumer repo: the rule syncs from the hub and the next sync overwrites a local edit. Hoisted pairs go under the item they extend; the consumer then deletes them from its `.local.md`.

## References

- [references/failure-modes.md](references/failure-modes.md): the modes, the log signal for each, one example
