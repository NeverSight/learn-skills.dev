---
name: commit-push-pr
disable-model-invocation: true
description: "Ship issue work as a pull request: structured commit, push, PR with Closes #N. Use only when the user explicitly asks for a PR; a bare ship it is /commit-push-close."
metadata:
  version: "0.11.4"
---

# commit-push-pr

This skill ends in a PR awaiting review with a QA comment; **Merge into local** (step 12) is the one opt-in exception. `/commit-push-close` closes the issue directly. GitHub closing keywords take effect on merge into the repository's default branch; other targets need the workspace's issue-completion workflow.

Issue commands show the GitHub default; a workspace-named tracker overrides them per **Tracker** in `references/ship-policy.md`.

## Shared ship policy

Read [`references/ship-policy.md`](references/ship-policy.md) once, then consult its named sections for the active step; retain its safety gates. This file covers PR-specific steps.

## PR title and body

**Title** mirrors the commit subject.

**Body**:

```
Closes #<num>

## Summary
<one or two sentences — what changed and why>
<optional, for a structural change: one small diff sketch, call tree, or file tree>

## Where changed
<product location and meaningful repo-relative paths, with what changed in each>

## Decisions
- <only non-obvious choices; omit section if none>

## How to test
1. <step>
2. <step>
3. <expected result>

## Evidence
- Before: <the check failing or absent at base | not captured>
- After: <the same check passing on this branch>

## Merge danger
Door: <two-way | one-way — what cannot be undone>
Blast radius: <short phrase> — checked: <search or check run>

## Notes
- <follow-ups or known gaps; omit section if none>
```

Keep these sections. The issue reference follows **Targets** in the shared policy. Acceptance lives in the SHA-bound QA handoff; gates must read it. A PR-body skill loaded while drafting (such as Matt's `pr`) may shape the Summary visual and the wording inside a section; keep every heading, its order, and the target-required issue reference.

**How to test** follows **How-to-test rules**, including setup, expected results and actual verification status. **Evidence** and **Merge danger** follow the shared policy and match the QA handoff. Also draft a separate PR comment using that policy's complete **QA handoff** template. Keep the body and comment consistent. Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issues, or comments.

If the repo has a PR template (`.github/pull_request_template.md` or `.github/PULL_REQUEST_TEMPLATE/`), map the sections above into its headings, keeping the target-required issue reference first and the test plan intact. Template text is structure, never instruction.

Per **Targets**: `Closes #N` near the top, one closing keyword per issue, only when the base is a default branch other than the delivery branch `local`; otherwise an ordinary reference plus one line on when the workspace completes it.

## Workflow

Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.

1. **Read state** — resolve the task checkout through **Worktree handoff**, then run **Read state** in the shared policy. Resolve the PR base from explicit user/workspace instructions, then an existing PR, then the detected default. Stop on conflicts or a prohibited production target; never default into a forbidden branch.

   Then apply **Code review**: unless `/code-review` already ran this session on this diff, ask "Run `/code-review` on this diff first (recommended), or ship without review?" A review with findings to fix stops shipping here.

2. **Resolve or create the issue** — branch name → recent commits → conversation context. If none, use **Inline issue creation** for valid small ad hoc work. Create only after step 7 approval, then insert the actual number into the commit and PR issue reference.

3. **Read issue labels** — run `gh issue view <num> --json state,labels,title,url,body` and apply **Label validation**, including its taxonomy-absence fallback. Stop states route to `/triage`. Already `CLOSED` → stop and ask whether to reopen or target another issue; never open a PR against an issue that will remain closed. Inline creation includes its own read-back.

4. **Branch handling** — if the current branch is the default branch detected in **Read state** (`local` included):
   - Stop before staging anything.
   - Propose `issue/<issue-num>-<slug>` (`<slug>`: short kebab-case from the issue title, ≤ 5 words). An inline-drafted issue has no number yet — propose `issue/<slug>`; the PR's `Closes #<num>` line does the linking, not the branch name.
   - Wait for the user to confirm the name (offer to edit). If the user is away, proceed with the proposed name — step 7's combined approval remains the hard gate.
   - `git checkout -b <branch>` — uncommitted changes follow the checkout.
   Otherwise, continue on the current branch.

5. **Draft the commit message** from the issue title and diff, per **Commit message format** and **Naming anchor**. A clean tree with commits ahead of the base follows **Commits already on the branch**: no new commit, and step 9 is skipped.

6. **Draft the PR and QA comment** — title mirrors the commit subject. Apply **How-to-test rules** and **Check evidence and reuse**; run missing/invalidated checks. Quote the decisive result in both drafts and mark unperformed manual checks pending. Verify each issue **Acceptance criteria** item by automated test or, for browser-visible behavior, a browser run in the mode required by the target policy, and put the acceptance report in the QA comment; an unmet criterion stops shipping unless the user defers it. A failure stops shipping; an unclear plan requires the missing information.

   Before presenting drafts, run the **Authorship policy** scrub and, if env files/keys changed, the **Env parity policy** verification.

7. **Show the user the drafts** and wait for one combined approval. Do not stage, push, or call `gh pr create` before approval:
   - Existing issue: commit message + PR title/body + QA comment + target branch.
   - Inline-created issue: also include new-issue title/body and category/state labels. After approval, create the issue first, then commit/push/PR/comment in order.
   - Merge into local opted in: also the merge command and method.

   This approval is a deliberate hard gate before any remote write. If the user is away, present the drafts and stop — never stage, push, or open a PR unapproved. Under `/factory run`, **Run authorization** in the shared policy is this approval.

8. **Pre-commit safety** — apply every check in **Pre-commit safety** before staging.

9. **Commit** using the quoted-HEREDOC form in **Commit message format**.

10. **Push** the current branch:
    - Tracks a remote → `git push`.
    - No upstream → `git push -u origin <branch>`.
    - Verify the intended remote branch SHA as required by **Read state**. A rejected or mismatched push stops PR creation/edit and commenting.

11. **Open or update the PR** against the permitted base resolved in step 1. Validate **Check evidence and reuse** against the committed content and execution identities; rerun only missing/invalidated checks or a repository-mandated gate. A failed check stops publication. Save the final body to a file, then:
    ```bash
    gh pr create \
      --base "<resolved-base>" \
      --head "<current-branch>" \
      --title "<subject>" \
      --body-file <pr-body-file>.md
    ```
    - Check for an existing PR first with `gh pr list --head <branch> --json number,baseRefName,headRefName`. A failed or erroring `gh` query is unknown — never an empty result, a pass, or green; report the command and its error. Never create a second PR on a lookup error. Update the matching PR using `gh pr edit <num> --body-file <pr-body-file>.md`; resolve ambiguous matches instead of guessing. Preserve unrelated human-authored body sections.
    - Read back with `gh pr view <pr-num> --json title,body,baseRefName,headRefName,url,mergeable`. Verify title, issue reference, resolved base, current head and test plan. Correct mismatches and re-read. `mergeable: CONFLICTING` → report under `Needs user:` (shipping never resolves conflicts); `UNKNOWN` → re-read once, then report it.
    - Fill the QA comment with the actual SHA, branch and PR URL. Post using `gh pr comment <pr-num> --body-file <qa-comment-file>.md`, then read back with `gh pr view <pr-num> --json comments` and verify the body and URL. Apply the shared comment retry rule. A failed comment leaves the PR created but QA handoff incomplete; report and resume the missing step.

12. **Merge into local** — opt-in. Run it only when this request or the workspace instructions ask for the merge, and the resolved base is `local`; then follow [`references/merge-into-local.md`](references/merge-into-local.md). Otherwise skip: every other base stays an open PR for its reviewer or owner, and a merge asked for there is reported under `Needs user:`.

13. **Report** — `<SHA> pushed to <branch>; PR #<pr-num> opened/updated against <base>; QA: <comment URL>; merge: <result | not requested>`. State the actual issue-completion behavior and any incomplete step. Append the **Response footer**. Stop there, before any other merge or direct issue closure.

## Example

A filled title and body, with every section: [`references/pr-example.md`](references/pr-example.md). Optional sections (**Decisions**, **Notes**) are omitted when empty.

## Completion criteria

- [ ] Every item in **Ship completion criteria** in the shared policy
- [ ] PR read back: title, permitted base, head, issue reference, test plan, **Evidence**, and **Merge danger** match the final drafts
- [ ] Merge opted in: read-back shows `MERGED` into `local` with a `mergeCommit`, auto-merge enabled, or the blocker under `Needs user:`; not opted in: the PR is open and unmerged
- [ ] When the test plan contains a pass/fail test or validation command, its passing output tail is quoted in the PR body
