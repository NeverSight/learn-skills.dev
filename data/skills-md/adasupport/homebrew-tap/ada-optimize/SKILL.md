---
name: ada-optimize
description: Autonomously improve an Ada AI agent with adacli — go from a failing example to measurably better performance. Drives the full loop (gather failures → build evals → diagnose → apply a fix → re-test → keep or roll back → hill-climb), then renders a Karpathy-style progress chart. Use when the user wants to improve/optimize an agent, raise resolution, fix what the agent gets wrong, or "make the agent better at X".
require-tools:
  - Bash
  - Read
  - Write
---

# Autonomously improving an Ada agent (operator → architect)

This is the self-improving loop: the manager sets the bar; you + adacli climb to it.
You **gather** the standard, **diagnose** failures, **self-edit** fixes, and **raise the bar** —
the manager approves diffs instead of authoring them. Everything below runs through `adacli`,
which is agent-native: pass `--json`, parse stdout, branch on the typed exit code
(`0` ok, `2` usage, `3` auth, `5` not-found, `6` rate-limit). Run `adacli <instance> agent-context`
once to load the full command/flag/exit-code contract.

## Start from a failing metric

If the user names a custom metric to improve ("Improve the X metric with adacli"), follow
the improvement loop in place of steps 1 to 7. If `adacli <instance> --help` lists `loop`, run
`adacli <instance> loop --json` and follow its `markdown`. adacli lists `loop` only when the
improvement loop is on for the account. If `upgrade_required` is true, tell the user to upgrade
adacli. If adacli does not list `loop`, `adacli <instance> loop --json` exits non-zero, or
`upgrade_required` is true, follow [metric-loop.md](metric-loop.md). Step 0 still applies. It stages every fix on a change set.
Run `changesets promote --yes` or `changesets set-rollout` only after the user confirms in chat.

## 0. Safety first (always)

```bash
adacli <instance> status --json                          # confirm session
adacli <instance> snapshot export -o baseline/           # rollback point — commit to git
git add baseline && git commit -m "pre-optimization baseline"
adacli <instance> testing quota --json                   # runs are metered — don't burn them in loops
```
Never run destructive ops without the user's OK. Respect read-only instances.

## 1. Gather — turn failures into evals

```bash
# Find what failed (the cohort the loop learns from)
adacli <instance> conversations search --resolution not-resolved --since 30d --all --limit 500 --json
# --all pages the whole cohort — see the canonical --all note in the adacli skill
# (also: --csat 1 2  |  --handoff  |  --handoff-reason <code>  |  --channel <id>  |  --language en)

# To reduce handoffs, rank the reasons first, then take the cohort of the top fixable one
adacli <instance> conversations handoff-reasons --since 7d --count --json
adacli <instance> conversations handoff-reasons --since 7d --handoff-reason <code> --samples 5 --with-reasoning --json
# reasoning is often null (e.g. tool_failed, system_failed): use reason_code, target, outcome and the transcript

# Turn a real failing conversation into an eval case. Every personal value is faked
adacli <instance> testing cases from-conversation <conversation-id> --json   # draft + instructions
```
Follow the draft's `instructions` to write and save each case. The same steps are in
[../ada-test-agent/test-case-from-conversation.md](../ada-test-agent/test-case-from-conversation.md).
Curate a small, high-signal set of cases — your bar. The manager decides which examples matter.

## 2. Baseline — start the hill-climb

```bash
adacli <instance> optimize start --target 90 --label "Billing AR"
adacli <instance> testing runs create --cases <ids...> --repeat 3 --json    # repeat for a stable rate
# read pass rate from the runs, then:
adacli <instance> optimize record --pass-rate <rate> --passed <p> --total <t> --change "baseline"
```

## 3. Diagnose — name the exact surface to fix

```bash
adacli <instance> conversations diagnose <conversation-id> --json
```
Returns a typed verdict: `surface` (knowledge | playbook | guidance | handoff | unknown), a `target` id,
and a `why`. **adacli names the surface; you author the fix.** Classify each failure before editing.
`handoff_reason.fix_surface` maps the recorded handoff reason to a fix. The ada-insights skill
("Why the agent hands off") is the canonical list of its values and of how a reason differs from escalation.
After the fix, re-run `conversations handoff-reasons --handoff-reason <code> --count` over a new window
and check that the count dropped.

## 4. Self-edit — apply the fix for that surface

| Surface | Fix with |
|---------|----------|
| `knowledge` | `adacli <instance> knowledge create --title ... --file ...` (or `update <id>`) |
| `guidance` | `adacli <instance> guidance create --title "..." --text "..."` (validate first: `guidance validate`) |
| `coaching` | `adacli <instance> coaching create --conversation <id> --event <bot-msg-event-id> --module response_reasoner --type reply --plan contextual_response ...` |
| `playbook` | `adacli <instance> playbooks update <id> --file ...` |
| `unknown` | Do not author a fix — the read was unverifiable (exit 22); retry the diagnose read (see the canonical exit-22 note in the `adacli` skill). If it stays `unknown`, the analytics read path is degraded — wait and retry. |

Show the manager the change (`snapshot import baseline/ --dry-run` shows what the baseline would change back) before applying.

## 5. Re-test + compare — did it help?

```bash
adacli <instance> testing runs create --cases <ids...> --repeat 3 --json
adacli <instance> testing runs compare --baseline <baseline-run-ids...> --candidate <new-run-ids...> --json
```
`compare` returns `{ summary.delta, newly_passing, regressed }` — the gradient.

## 6. Keep or roll back, and record the step

```bash
# improved → keep
adacli <instance> optimize record --pass-rate <new-rate> --change "added shared-accounts KB article"

# regressed → roll back the change, then record it as not kept
adacli <instance> snapshot import baseline/ --include knowledge --confirm   # or delete the edit
adacli <instance> optimize record --pass-rate <rate> --change "coaching attempt" --rolled-back
```

## 7. Loop until the bar is met, then visualize

Repeat 3→6, each iteration recorded. The bar only goes up — add a new failing example as a
permanent regression case whenever you find one. When done (or to report progress):

```bash
adacli <instance> optimize status --json
adacli <instance> optimize viz          # writes a self-contained hill-climb chart; open the HTML
```

## Rules

- **Evals are the engine.** Every change is validated against the eval set, kept only if it improves, rolled back otherwise. Never ship a change you didn't re-test.
- **One change per iteration** so `compare` attributes the delta correctly.
- **Quota-aware:** check `testing quota` before each run batch; use `--repeat` for stability, not for grinding.
- **The manager sets the bar.** You propose diffs and report the climb; they approve. Surface the diagnosis and the diff before applying.
- Related skills: **ada-insights** (deeper diagnosis), **ada-knowledge** (KB edits), **ada-test-agent** (eval mechanics), **ada-config-snapshot** (baseline + rollback).
