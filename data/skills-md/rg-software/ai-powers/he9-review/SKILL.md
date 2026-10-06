---
name: he9-review
description: "Code review / respond cycle - review a target locally (branch, uncommitted work, a commit, a range), or respond to the latest review on a PR. Use when the user asks for a review, or to respond to review feedback on a PR. Invocation text is the review target: 'branch' (default), 'worktree', 'staged', 'commit', 'range A..B', 'path p', or 'respond [PR]'."
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Perform a code review / respond cycle

Goal: improve code with a single review/respond cycle, including local maintainability refactoring where appropriate.

**Invocation.** The invocation text is the text that accompanied this skill — the words after the skill name. Read it as the **review target** (what is being reviewed). If it begins with `respond`, use the respond mode instead. A review target is distinct from a finding's `scope` in the contract (`in-touched`/`adjacent`/`project-wide`).

| target | resolved diff spec |
|--------|--------------------|
| `branch` (default, or empty) | `<base>...HEAD` — every commit on the branch, not just the latest |
| `worktree` | uncommitted work: `git diff HEAD` **plus untracked files** |
| `staged` | `git diff --cached` |
| `commit` | `git show HEAD` (the last commit; also correct for the root commit) |
| `range <A>..<B>` | the given range |
| `path <p>` | the default target restricted to a path: `(<base>...HEAD) -- <p>` |

`<base>` is the resolved `baseBranch`.

Note: `git diff` **invisibly omits untracked files**. For `worktree`, enumerate them with `git status --porcelain` and read their contents; otherwise new files are reviewed by name only.

If the invocation text is empty or does not name a target, treat it as `branch` — but if it is ambiguous, state which target you are about to use before reviewing.

**Project inputs (optional adapter).** Read `.opencode/powers.jsonc` if present; it overrides the defaults below. This skill uses: `baseBranch` (default `origin/HEAD`; if unset, ask and offer to record it), `conventions` (`openspec/conventions.md`), `specs` (`openspec/specs/*/spec.md`), `debt` (`openspec/technical-debt.md`), `tracker` (auto: configured forge MCP, else git remote host, else ask), `contract` (`he9-review-contract`). Probe for paths; if one is absent, skip that step rather than guessing. Pass the resolved inputs to the reviewer rather than making it re-derive them; `code-review-expert` documents the same defaults.

## Mode: review a target

0. **Establish the reviewing party.** This mode requires a `reviewer` subagent (see `docs/adapter.md` → "Local reviewer agent"). In a skill body, `reviewer` is prose the model acts on, not a dispatch the harness resolves — so an unavailable subagent surfaces as an ordinary turn, not an error. Handle it explicitly:

   - Check the configured subagents before reviewing. If `reviewer` is present, `REVIEWING_PARTY = reviewer` (subagent).
   - If it is absent, **stop.** Do not review yourself. Tell the user this mode needs a `reviewer` subagent, point at `docs/adapter.md` → "Local reviewer agent", and offer a self-review instead. Proceed with a self-review only if the user asks for it, and then set `REVIEWING_PARTY = self-review (not independently reviewed)`.
   - Whatever happens, **announce the party** before presenting any finding, in this form: `Reviewing party: reviewer` or `Reviewing party: self-review (not independently reviewed)`. Never present a review without it.
   - If a `reviewer` invocation fails, returns nothing usable, or you cannot confirm it ran, treat it as a failure: report which step failed and stop. Do not substitute your own review and label it as the subagent's.

1. Resolve the target to an explicit diff spec from the table. State the resolved spec before reviewing.

2. Invoke the `reviewer` subagent with this task:

   > Perform a code review of this change set: `<resolved diff spec>`. List the files included. For untracked files, read each one in full and review it as added code. If any file is out of scope or not reviewable, say so explicitly.
   >
   > Use the `code-review-expert` skill and grade findings with the `he9-review-contract` skill. Pass it the project inputs resolved above; it owns input resolution, `Not reviewed`, and the non-interactive hand-off skip, so do not restate those. Use `.opencode/powers.jsonc` (if present) for the conventions and specs to check architecture drift against.

3. Use the `receiving-code-review` skill — with the `he9-review-contract` vocabulary — to analyze the review and assign a **disposition to every finding**.

4. Produce the response in the contract's responder output format.

5. Present both in full as rendered markdown, headed by the announced reviewing party from Step 0: the review, then the response. Do not summarize or omit anything. Reports are **print-only** — do not persist them; the durable artifact is the code change and any debt entry, not the review.

6. Recommend what to address now, applying the contract's severity-to-action policy (use the table in `he9-review-contract`; do not restate it from memory). In short: P0/P1 fix before merge; P2 in touched code usually fix now unless not cheap; P2 outside touched code usually defer; P3 optional.

7. Act on the dispositions. For every `defer-debt` finding, **write a self-contained entry into the resolved `debt` document**, using that document's own item template and grading it per `he9-review-contract` → "Mapping to the debt backlog": inline the evidence, symptom, and `file:line`, because the review is not kept (the finding `id` may remain as provenance only). For `promote-issue` / `promote-change` findings, recommend the focused issue or spec change rather than creating it here — promotion is a deliberate step. `fix-now` findings are this branch's work and are not recorded.

8. Ask the user how to proceed:
   - **A**: fix all recommended issues.
   - **B**: choose issues to fix.
   - **C**: defer selected maintainability issues into the resolved `debt` document.

## Mode: respond <PR number>

1. If the invocation text carries no PR number, list the open PRs through the resolved `tracker` and ask the user to choose one.
2. Find and read the most recent review comment carrying the marker `<!-- he9-reviewer:v1 -->` (the CI reviewer stamps every review with it). If none exists, inform the user and stop.
3. Use the `receiving-code-review` skill with the `he9-review-contract` vocabulary: verify each finding, assign a disposition to every one, and emit the contract's responder output format.
4. Act on the dispositions: write every `defer-debt` finding into the resolved `debt` document as a self-contained entry (item template; inline the evidence, symptom, and `file:line`; the finding `id` may remain as provenance only), and recommend a focused issue or spec change for `promote-issue` / `promote-change` findings rather than creating it here.
5. Ask whether to fix the in-branch issues now, or defer the selected findings into the resolved `debt` document.