---
name: parallel-review
description: Run every code reviewer in parallel over a local diff and merge their findings into one ranked list. Use when the user asks for a review of uncommitted changes, says "quick review", or after significant code changes; and when another skill needs the local-diff review (`done` runs it as its review step).
---

# Parallel code review

I run every reviewer at once over the local diff and merge what they find into one ranked list. Fast, and no reviewer sees another one work, so the findings stay independent.

## Workflow

### Step 1: Determine Scope

- When the user specifies files, I review those files.
- Otherwise I review all unstaged and staged changes through `git diff HEAD`.
- I pin the comparison base before dispatch. When the caller supplies a merge-base SHA, as `done` does, I use it. Otherwise I resolve `git merge-base HEAD origin/<default branch>`, reading the default from `gh repo view --json defaultBranchRef`. Reviewers need it as context to tell base-branch behavior from behavior that earlier commits on this branch introduced. It never widens the review target, which stays the Step 1 scope.
- When a prior convergence artifact exists, I invoke `converge-reviews` with the current baseline, diff hash, paths, request, and planned roster and lenses before I dispatch. I reuse an unchanged result. When it returns `continue`, I dispatch only the invalidated coverage it names. I apply any other result without starting another review round.

### Step 2: Build the roster, then dispatch

I name the roster first, then launch every member in parallel with the Agent tool.

Members 1-3 below are `subagent_type` values, and I pass them to the Agent tool as-is. Member 4 is a skill-running agent. `/web-interface-guidelines` and `/rams` are skills, not agent types, so they cannot go as `subagent_type`. I dispatch a `general-purpose` agent that invokes them instead.

I size the roster to the diff before I name it. `done` runs this skill after every task, so an unsized roster charges a one-line fix what a rewrite costs. I measure the Step 1 scope with `git diff --shortstat HEAD -- <paths>` when files were specified, or bare `git diff --shortstat HEAD` when they were not.

- One file and under roughly 50 changed lines, or the user asked for a quick review, then the roster is `pr-review-toolkit:code-reviewer` alone and the rest of this step does not apply.
- Anything larger builds the roster from the members below.

A re-review after fixing findings covers the fix delta, never the whole diff again, and I size it by that delta.

Always on the roster:

1. Code Review Agent with `subagent_type: "pr-review-toolkit:code-reviewer"`.
2. CodeRabbit Review Agent with `subagent_type: "coderabbit:code-reviewer"`.

I add to the roster when the condition holds:

3. Silent Failure Hunter with `subagent_type: "pr-review-toolkit:silent-failure-hunter"`. I add it when the diff touches error handling, try-catch, or fallback logic.
4. UI Review Agent with `subagent_type: "general-purpose"`. I add it when the diff touches frontend or UI code. I prompt it to invoke `/web-interface-guidelines` and `/rams` against the diff and return their merged findings.

The shared prompt, plus the per-agent lens, reads "Review these changed files for bugs, logic errors, and adherence to project CLAUDE.md conventions: [files]. The review target is [scope diff command] only, the Step 1 scope or the fix delta. The comparison base, [merge-base SHA], is context for the product-intent check alone: `git show [merge-base SHA]:<file>` is what the base branch has."

Every reviewer also carries the product-intent instruction. When a finding's fix would change observable behavior that already exists on the base branch, meaning at the pinned merge-base rather than in this branch's earlier commits, the reviewer adds a `product-intent` tag to it and reports what it found: whether a test asserts the current behavior, whether a comment or doc explains it, and which commit introduced it per `git blame` or `git log -S`, including "found nothing". Reviewers report tagged findings at their real severity and do not fix them.

I state the roster before dispatching. It is the checklist Step 3 merges against.

### Step 3: Merge

The merge is not done while any reviewer on the roster is outstanding. I account for every member by name, reported or failed and re-dispatched.

1. I merge all findings, collapsing duplicates across reviewers. A `product-intent` tag on any source finding survives the collapse, and its evidence carries into the merged finding.
2. I assign each merged finding a stable ID from its file, enclosing symbol, normalized defect class, and defect-instance fingerprint. I derive the fingerprint from the smallest stable semantic code anchor, such as a callee, accessed field, branch label, or data-flow endpoints, plus the violated invariant. When two defects still share an anchor, I extend it with the nearest distinct semantic parent or operand. I normalize incidental formatting, literals, and reviewer wording, and I exclude raw line numbers. I merge only when all four parts match, and I preserve every source reviewer. The caller owns these IDs and their dispositions. I do not create a shared finding-ID authority.
3. Rank: Critical > Serious > Moderate > Minor, then present one traceable list. A `product-intent` tag rides alongside the severity and never lowers it. The tag is binding: no agent fixes a tagged finding without the user's approval, and no agent drops or downgrades it when handing the list on.
4. I invoke `converge-reviews` with the originating request, local baseline and current diff hash, reviewed paths, roster and lenses, merged findings, dispositions, and prior convergence artifact. I apply its result contract, then hand the ranked list and convergence result back to the caller.
