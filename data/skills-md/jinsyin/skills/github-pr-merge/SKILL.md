---
name: github-pr-merge
description: Review and squash-merge open GitHub PRs one by one via `gh`, user deciding each. Use when user wants to review, triage, or merge open PRs, including PRs `self-improve` opened. Args `[<pr#>] [-R <owner/repo>]`.
---
# github-pr-merge

Pick PR → understand → review → user decides → merge, close Issue → next PR.

Repo: `-R <owner/repo>` if given, else current repo (`gh repo view --json nameWithOwner,defaultBranchRef`). Pass `-R` to every `gh` call.

## 1. Pick a PR

`<pr#>` arg skips step (not open → say so, go to step 5). Else:

```bash
gh pr list -R <repo> --state open --limit 200 \
  --json number,title,createdAt,author,labels,headRefName --jq 'sort_by(.createdAt)'
```

Ask via ask-user tool: 3 oldest PRs as options (`#<n> <title> · <author> · <date> · <labels>`), plus last option "List all open PRs". On that choice, print full numbered list, user picks. No open PRs → say so, go to step 5.

## 2. Understand

```bash
gh pr view <n> -R <repo> --json number,title,body,author,headRefName,headRefOid,baseRefName,isCrossRepository,mergeable,mergeStateStatus,statusCheckRollup,closingIssuesReferences,commits,files
gh pr diff <n> -R <repo>
gh issue view <i> -R <repo> --comments   # each closing Issue, plus any `#<i>` the body only mentions
```

Brief summary: problem (from Issue), what PR changes, files touched.

## 3. Review

Every layer gets a verdict: pass, or findings. A failed check is a finding; user still decides.

1. **Gate** — conflicts (`mergeable`), CI (`statusCheckRollup`), files outside PR's stated scope, commit style and `CHANGELOG.md` per repo's `CLAUDE.md`/`AGENTS.md`.
2. **Intent** — diff actually solves Issue, nothing else?
3. **Skill edits** (any `skills/**/SKILL.md` or skill resource changed) — read whole target skill on latest default branch:
   - Evidence: Issue evidence meets bar (strong once, weak ≥2), or one-off slip / project-specific fact? Rules fitted to one incident make every future load pay.
   - Duplication/conflict: already covered on default branch, or contradicts other passage/skill?
   - Minimality: smallest owning passage, growth ≤ ~20%, no restructuring, same language/tone, reasons over ALL-CAPS MUSTs.
   - `description` changed: over- or under-trigger?

**Conflicts**: merge needs a conflict-free branch, so resolve before deciding via a head-branch edit: rebase onto `origin/<base>`; `CHANGELOG.md` → keep both sides' entries in their sections; ask user about other conflicts.

**Head-branch edit** (conflict fix or requested change): same-repo only; `isCrossRepository` → report, put fixes in a PR comment, user picks other changes or reject. In scratchpad `git worktree` of head branch, edit, commit per repo conventions, `git push --force-with-lease`, remove worktree, back to step 2 (new `headRefOid`); its review is a Re-review.

## 4. Decide

Post review as PR comment — authors can't approve own PRs, so comment = review record:

- Header: `## Review`, or `## Re-review` after a head-branch edit (mark each earlier finding resolved or open). Next line `Reviewer: <model>/<effort>` (e.g. `Reviewer: claude-opus-5-5/high`) — this session's model ID and effort level (not in your context; on Claude Code read `$CLAUDE_EFFORT`), unknown → `unknown` — so readers can weigh the verdict.
- Body: verdict per layer, findings, suggested fixes.
- `gh pr comment <n> -R <repo> --body-file <f>` prints the comment URL; keep it.

Tell user briefly — Review: core findings + suggested fixes; Re-review: conclusion — ending with the full comment URL, so the record is one click away. Then ask user, options always in order Apply suggestions → Other changes → Merge → Reject (recommended one keeps its slot, not moved first); act only on user's pick:

- **Apply suggestions** — offer only while same-repo and suggested fixes unapplied (Re-review, all findings resolved → none). Pick = consent: apply as head-branch edit.
- **Other changes** — edits beyond suggested fixes: list concretely; with user consent, apply as head-branch edit. Cross-repo → all edits, fixes included, stay in PR comment; next PR.
- **Merge** — `gh pr merge <n> -R <repo> --squash --match-head-commit <reviewed-sha>`. `<reviewed-sha>` = `headRefOid` from latest step 2, so the guard refuses unreviewed commits.
- **Reject** — `gh pr edit <n> --add-label rejected`, `gh pr close <n> --comment "<reason>"`; each linked Issue: `gh issue edit <i> --add-label rejected`, close with `--reason "not planned"` + reason. Create `rejected` if missing; lets `self-improve` dedupe skip it — `no-pr` records also close not planned.

## 5. Wrap up

- After merge, check each closing Issue; still open → `gh issue close <i> --comment "Fixed by #<n>"`. Issues only mentioned (not `Closes`) → ask before closing.
- Back to step 1 for next PR until user stops.
- Loop ends (no open PRs or user stops) → auto-sync local if cwd is `<repo>` checkout (`origin` matches) on default branch, no uncommitted tracked changes (untracked OK); else just note. `git fetch origin` first — merges landed remotely, local `origin/<base>` stale. Then:
  - No local commits (`git rev-list --count origin/<base>..HEAD` = 0) → `git pull --ff-only`.
  - Local commits → `git rebase origin/<base>` (linear history), `git push`. `CHANGELOG.md` conflicts → keep both, local on top; ask on others. Push rejected → fetch, rebase, retry; never force.
