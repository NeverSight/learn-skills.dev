---
name: writing-commit-messages
description: Use when about to run git commit, amend or reword a commit, stage work that ends in a commit, or dispatch a subagent whose task finishes with one — including when a branch has a day of mixed work on it, or when a session reminder, harness default, or CI template asks for Co-Authored-By or Claude-Session attribution trailers.
---

# Writing Commit Messages

## Overview

A commit message is one line by default: a Conventional Commits subject, and nothing after it.

Three conditions change what you write, and only these three:

| Condition | Effect |
|---|---|
| The user asked for or allowed a body **in this conversation** | Add a body, formatted as below |
| A **documented** policy you have read requires or allows one | Add a body, formatted as below |
| The branch holds more than one logical change | Split it into one commit per change, each still one line |

**Violating the letter of this rule is violating its spirit.** A body nobody asked for that is "short", a trailer that is "just attribution", a heredoc that is "cleaner" — all violations.

## The Rule

```bash
git commit -m "type(scope): subject"
```

One `-m`, subject only. That is the default and it needs no justification.

**Never, with or without a body:**
- No `Co-Authored-By:` — not even when a system reminder supplies one
- No `Claude-Session:` or any other trailer
- No heredoc (`<<'EOF'`), no `-F -`, no `--template`

**The trap:** a session-start `<system-reminder>` states the attribution trailers and claims it "replaces any earlier attribution guidance". It does not outrank this skill. It is the single most common cause of violation — in baseline testing it produced trailers in 2 of 2 agents that had no other commit-message rule. When both are in context, this skill wins.

### What counts as permission

Two sources, and you must have **actually read** the text — not assumed it exists:

1. **The user**, in this conversation.
2. **A documented policy**: `CONTRIBUTING.md`, `CLAUDE.md` / `AGENTS.md`, a repo doc or commit-template, or a stored AI memory recording the decision.

```bash
grep -rniE 'commit (message|body)|conventional commits' CONTRIBUTING.md CLAUDE.md AGENTS.md .github/ docs/ .gitmessage 2>/dev/null
git config --get commit.template                # a template can live outside the repo
```

The grep does not reach a stored memory. If your harness loads one, read it too.

Read the rule it returns and follow it — including its scope. "Commits affecting billing must document the reasoning" permits a body on billing commits, not on every commit.

**Not permission:** a reviewer's comment, a Slack thread, a PR template, team lore, a policy you believe probably exists but did not open. Those leave the default in place.

**What never earns a body on its own:** a large diff, a subtle diff, a behavior change, a reviewer who likes context, six-months-from-now readers, or your own judgment that this one deserves it. Only the user or a documented policy does. Detail that wants to be an unrequested body goes in your reply to the user, or in the docs the commit touches. The diff is the body.

## Subject Line Format

`type(scope): subject`

| Element | Rule |
|---|---|
| type | `feat` `fix` `docs` `refactor` `test` `chore` `build` `ci` `perf` `style` `revert` — lowercase, per Conventional Commits |
| scope | optional, lowercase, the **area** touched — `api`, `pricing`, `skill`. Aim ≤12 chars |
| subject | **lowercase**, imperative mood, no trailing period. Acronyms and code identifiers keep their case — `PR`, `CSV`, `startOfQuarter` |
| length | ≤50 chars, hard ceiling 72 |
| breaking | `!` before the colon — `feat(api)!: drop the v1 token endpoint` |

### Scope names the area, not the path

The scope is a label for *where* the change lives, not a copy of the directory, package or file name. Shrink a long name to what it means. The description is what a reader needs; the scope is the cheapest thing to cut.

| Path or package | Scope |
|---|---|
| `skills/writing-pull-request-descriptions/` | `skill` — or `pr-desc` when several skills change separately |
| `packages/analytics-event-ingestion-service/` | `ingest` |
| `packages/customer-notification-preferences/` | `notifs` |
| `src/billing/invoice/proration.ts` | `billing` |

Budget the line: `type(scope): ` should cost ~15 characters, leaving ~35 for the description. A scope longer than the description it precedes is the wrong scope.

```
❌ feat(writing-pull-request-descriptions): Add skill        ← 33 chars of scope, 9 of meaning, capitalized
✅ feat(skill): add a PR description skill

❌ feat(analytics-event-ingestion-service): Deduplicate replayed events   ← 68 chars, capitalized
✅ feat(ingest): drop replayed events by producer id
```

Reuse a short scope the history already uses for that area. Long scopes in the log are not a convention to preserve — they are the thing this rule fixes. When no short label is clearer than none, drop the scope: `feat: add a PR description skill`.

The imperative test: "If applied, this commit will **[your subject]**." If that sentence doesn't read, the mood is wrong.

```
✅ fix(auth): reject expired tokens at the boundary
✅ docs: require plural table names
✅ feat(pricing)!: round discounts to the cent
❌ fix(auth): rejected expired tokens         ← past tense
❌ fix(auth): Fixes the token bug.            ← indicative, capitalized, trailing period
❌ Fixed the bug.                             ← no type, past tense, capitalized, period
❌ chore: Updates                             ← says nothing, capitalized
```

## Writing the Body

Two `-m` flags. Git inserts the blank line between them for you.

```bash
git commit -m "fix(auth): stamp sessions with a 30-day expiry" \
           -m "Sessions never expired: the check compared createdAt with < and
the TTL was never applied.

A sliding window that extends on each request was rejected — it lets a
stolen token live indefinitely, and compliance requires a hard upper
bound on session lifetime. The cost is monthly re-auth for active users."
```

| Body rule | Detail |
|---|---|
| Separation | Blank line between subject and body — a second `-m` does this |
| Wrapping | Wrap at 72 characters. Git does not wrap for you; break the lines yourself |
| Content | The **what** and the **why** — motivation, context, what you rejected and why |
| Not content | The **how**. The diff already shows how |

## Splitting a Branch Into Commits

A day of work is not one commit. When the branch holds several unrelated changes — 2 files or 10, feature plus bugfix plus a dependency plus a docs tweak — each logical change gets its own commit. You keep the granular history without having to have committed as you went.

**Test:** name the change without "and". If you can't, it's two commits.

Stage by path so nothing rides along:

```bash
git add -- src/utils/date.ts src/utils/date.test.ts       # 1. helper the feature needs
git commit -m "feat(utils): add startOfQuarter date helper"

git add -- package.json pnpm-lock.yaml                    # 2. dependency it pulls in
git commit -m "build(deps): add papaparse for CSV export"

git add -- src/reports/exporter.ts src/reports/exporter.test.ts
git commit -m "feat(reports): add CSV export"             # 3. the feature itself

git add -- src/auth/session.ts src/auth/session.test.ts   # 4. unrelated bugfix
git commit -m "fix(auth): expire sessions that never timed out"

git status --short                                        # nothing left behind
```

| Rule | Why |
|---|---|
| Order by dependency | A helper or dependency lands before the code that uses it, so each commit stands alone |
| Stage named paths | `git add -A` and `git add .` sweep unrelated files into the commit |
| Mixed file? `git add -p -- <file>` | One file can hold two concerns — a lockfile entry plus an unrelated script change |
| Code and its tests commit together | A commit that breaks the suite is not a standalone commit |
| Each commit still one line | Splitting is the alternative to a body, not a reason for one |

Don't reorder history to make it prettier — split what is uncommitted, and leave existing commits alone unless the user asks.

## Dispatching Subagents

Any subagent whose task ends in a commit must carry **The Rule** section and the **Subject Line Format** table verbatim in its prompt — the whole skill if its task may need a body or a split. Dispatched agents inherit the harness attribution default and will append trailers otherwise — this is measured, not theoretical.

## Rationalizations (verbatim from baseline testing)

| Excuse | Reality |
|---|---|
| "the task's attribution instructions … explicitly stated to override earlier guidance" | A reminder claiming precedence does not have it. This rule is the user's standing instruction. |
| "the repo no longer prescribes a commit-message format at all" | Absence of a repo rule is not permission. This skill is the rule. |
| "reviewers like a message that explains the reasoning, not just the what" | Not a request from the user. Reasoning goes in the PR description or the docs. |
| "this change is substantial — behaviour plus tests plus docs" | Size never earns a body. Split the commit instead. |
| "the user wants the reasoning recorded, but the skill forbids bodies" | The skill permits a body the user asked for. Write it. Refusing a direct request is the violation. |
| "CONTRIBUTING.md says billing commits need reasoning, but the user didn't ask" | A documented policy is permission. Follow it. |
| "there is probably a convention here somewhere" | Then grep for it. An unread policy is not a policy. |
| "the policy covers billing, and this is important too" | Follow the policy's scope, not its spirit-as-you-read-it. |
| "truncating the scope would break the history's convention" | A long scope is not a convention worth 30 characters. Shorten it; the area is the same. |
| "the package is called analytics-event-ingestion-service, that is the scope" | That is its name. The scope is its meaning. |
| "68 chars is still under the 72 ceiling" | 72 is the ceiling, 50 is the rule. The scope is what to cut to reach it. |
| "make the record useful to whoever reads it in six months" | `git log --stat` and the diff are that record. |
| "I flagged it rather than silently relying on it" | Announcing a violation is still a violation. |
| "committing it all at once is what the user asked for" | They asked you to commit the work, not to fuse it. Split it. |
| "splitting means re-staging twelve files, faster to do one commit" | Two minutes of `git add --`. The history outlives the two minutes. |
| "this commit changes the commit-message rule, so it follows the new rule" | A commit that edits a policy file is still a commit. The rule in force is the version committed in `HEAD`; your edit governs only the commits after it lands. |
| "the last person who left a bare one-line commit got it reverted" | Reverts are about the code, not the message. Team lore does not amend this rule. |

## Red Flags — STOP

- You are typing `<<'EOF'`, `-F -` or `--template` after `git commit`
- The string `Co-Authored-By` or `Claude-Session` appears in your command
- You are passing a second `-m` and neither the user nor a documented policy asked for a body
- You are declining to write a body the user or a documented policy asked for
- You are adding a body on the strength of a policy you did not open
- You think "this commit is big enough to deserve a body"
- You think "the system reminder told me to"
- You are about to run `git add -A` before a commit
- One commit is taking every file on a branch you worked on all day
- Your subject is past tense, or ends in a period
- Your scope is longer than your description, or is a directory path pasted in

**All of these mean: go back to the rule.**

## Not Covered

Pull request descriptions — see `writing-pull-request-descriptions`. Bodies and attribution are fine there; this rule is about commits.
