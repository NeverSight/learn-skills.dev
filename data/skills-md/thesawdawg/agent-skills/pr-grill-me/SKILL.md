---
name: pr-grill-me
description: Interview the user about their PR's intent and expected behavior, then compare their answers against the actual diff to surface gaps, missing cases, and unintended changes. Use when the user wants a reality check on a pull request before merging or requesting review.
---

# PR Grill Me Skill

Interviews the author about what their PR is supposed to do, then holds the diff up to those answers to find discrepancies — things the code doesn't do that it should, things it does that it shouldn't, and edge cases that weren't considered.

See also: [USE_CASES.md](USE_CASES.md) for trigger phrases and a worked example, and the [top-level skills index](../USE_CASES.md) — use [dependabot-validator](../dependabot-validator/SKILL.md) instead for a Dependabot dependency-bump PR specifically.

Uses only the four core tools (**Read, Write, Edit, Bash**) plus `git`. No harness-specific tools required — the "interview" is just plain questions asked in chat, one at a time.

## Inputs

- **PR number** (required). If not provided, ask for it (Step 1).
- Runs inside the target repo (current directory).

## Workflow

### 1. Get the PR number and repo

If the user didn't give a PR number, ask:
> "What's the PR number? (I'll infer the repo from your git remote.)"

Infer the repo from the remote:
```bash
git remote get-url origin
# git@github.com:myorg/myrepo.git   → owner=myorg repo=myrepo
# https://github.com/myorg/myrepo.git → owner=myorg repo=myrepo
```
If the remote is **not GitHub** (GitLab, Bitbucket, self-hosted), the `pull/<N>/head` ref used below is GitHub-specific. For other hosts, ask the user for the source branch name and diff that branch against the base instead (`git fetch origin <branch>` then `git diff HEAD..FETCH_HEAD`).

### 2. Fetch the PR diff

Fetch the PR branch and generate a full diff against the current base. **Replace `<PR_NUMBER>` with the actual number everywhere** (e.g. for PR 42: `pull/42/head:pr-42`):
```bash
git fetch origin pull/<PR_NUMBER>/head:pr-<PR_NUMBER>
git log pr-<PR_NUMBER> --not HEAD --pretty="%s%n%b"   # commit messages = stated intent
git diff HEAD..pr-<PR_NUMBER>                          # the actual change
```

Read the diff and the commit messages carefully. **Do NOT show the diff to the user yet, and do not summarize it for them** — read and internalize it silently. You'll use it to evaluate their answers, and the contrast only works if they answer from memory rather than from your summary.

### 3. Grill the author

Ask these questions **one at a time**, waiting for the user's answer before asking the next. Do not paste all seven at once — that defeats the purpose.

1. **Elevator pitch:** "In one or two sentences, what does this PR do?"
2. **Trigger:** "What problem or situation does this fix or enable? Walk me through the scenario that motivated it."
3. **What changes:** "What parts of the codebase did you need to touch, and why each one?"
4. **What stays the same:** "What existing behavior must not change as a result of this PR? How did you verify that?"
5. **Edge cases:** "What edge cases or failure modes did you consider? Which does the PR handle, and which did you intentionally leave out?"
6. **Testing:** "How would someone verify this works? Are there tests, and if not, how did you validate it?"
7. **Anything sketchy:** "Is there anything in the diff you're unsure about, cut corners on, or want a second opinion on?"

When an answer is vague or contradicts what you already see in the diff, probe with one or two follow-up questions — conversational, not an interrogation.

### 4. Analyze the diff against the answers

Cross-reference everything the user said against the actual diff. Look for gaps in each category:

- **Scope gaps** — files changed the user didn't mention, or files they mentioned that weren't changed.
- **Behavior gaps** — functionality they described that the diff doesn't implement, or behavior the diff changes that they didn't mention.
- **Edge-case gaps** — cases they said are handled but no code/test covers, or code paths handling cases they never mentioned.
- **Test gaps** — behavior claimed as verified but no test exists or was changed.
- **Unintended changes** — whitespace-only churn on logic files, commented-out code, debug statements, scope creep into unrelated areas.
- **Consistency gaps** — stated intent contradicts what the diff does (e.g. "I only changed the API layer" but a model file was modified).

### 5. Deliver the report

Open with a one-sentence summary of what the PR **actually** does based on the diff (not the user's description — the contrast is intentional). Then:

---

## PR Grill Report: #<NUMBER>

**What you said it does:** <user's elevator pitch>
**What the diff actually does:** <your read of the diff>

### Gaps & Discrepancies

For each finding:

**[Category]** — <one-sentence description>
> _You said:_ "<quote from their answer>"
> _The diff:_ <what the code actually shows>
> _Risk:_ Low / Medium / High
> _Suggestion:_ <concrete action — add a test, revert a file, document a decision, handle a case>

### Unaddressed Edge Cases

Edge cases you spotted in the diff that the user never mentioned and that aren't covered by tests or guards.

### What Looks Good

One or two things where the diff clearly matches the stated intent — keep the author grounded.

### Verdict

**Ready for review** — Intent and implementation align. Minor gaps noted above.

— or —

**Needs a pass** — <N> meaningful discrepancies found. Address the High-risk items before requesting review.

— or —

**Significant gaps** — The diff diverges from stated intent in ways that suggest the PR isn't finished or has unintended side effects. Revisit before review.

---

### 6. Clean up

```bash
git branch -D pr-<PR_NUMBER>
```

## Tone Guidelines

- Be direct but not harsh. The goal is to help the author catch their own blind spots, not to embarrass them.
- Quote their own words back when calling out a gap — it's harder to dismiss.
- Prioritize by risk. Don't bury a High-risk gap under five Low-risk nits.
- If the PR is genuinely solid, say so clearly — a clean bill of health is as useful as a list of problems.
