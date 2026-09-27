---
name: pr-triage
description: >-
  Triages open GitHub pull request comments, review threads, merge conflicts,
  and CI workflow failures, empirically verifying reviewer claims before
  proposing a structured action plan. Use when asked to triage or address PR
  comments, review feedback, merge conflicts, or failing CI checks on a GitHub
  pull request, or when invoked via /pr-triage. Don't use for multi-repo PR
  cleanup sweeps (use pr-cleanup), initial adversarial code review (use
  pr-review), or Google3 Piper changelist triage (use cl-triage).
---

# GitHub PR Triage (`/pr-triage`)

## Quick Start

```bash
# Triage the active PR for a target repository checkout or worktree:
kscripts pr-triage --dir /path/to/target-repository

# Target a specific PR number or GitHub URL:
kscripts pr-triage --dir /path/to/target-repository --pr 123

# Reply to a comment and resolve a review thread:
kscripts pr-triage resolve --dir /path/to/target-repository <thread_id> <comment_id> "<reply_body>"

# Post an optional top-level reply, optionally dismiss a stale CHANGES_REQUESTED review, and re-request review:
kscripts pr-triage re-request --dir /path/to/target-repository <reviewer_login> [--comment "<reply_body>"] [--dismiss <review_database_id> -m "<reason>"]
```

## When to use this skill

- Use this skill when asked to address review comments, pull request feedback,
  or debug failing CI/CD runs on a GitHub pull request in an interactive,
  single-pass manner.
- This skill MUST be activated when the user asks you to "look at comments on my
  PR", "address comments/reviews", "fix the build/checks", or provides a PR
  URL/branch and asks you to fix it.

## 🧠 Critical Mindset: Reviewer Feedback is NOT Gospel

- **Reviewers make mistakes**: Do NOT assume any reviewer — whether an automated
  AI bot like Gemini Code Assist or a human engineer — is infallible. AI review
  bots frequently hallucinate syntax limitations, suggest outdated patterns, or
  misunderstand broader repository architecture.
- **Treat Severity Badges as Unverified External Claims**: Bot-generated
  severity tags (such as `![critical]` or `![security-high]`) are unverified
  external claims, NOT confirmed system diagnostics or compiler errors. Never
  blindly trust badges.
- **Mandatory Pre-Edit Empirical Verification Gate**: Before editing code for
  any reviewer comment claiming a syntax error, compilation failure, or type
  issue, the agent MUST run static analysis (`dart analyze`) on the **unmodified
  existing codebase** first.
  - If `dart analyze` returns **0 issues**, the reviewer's claim is empirically
    false. The item MUST be classified as
    `👎 Disagree (Hallucinated Syntax/Compile Error)` and NO code changes may be
    made for that item.
- **You have the execution advantage**: External reviewers inspect static code,
  whereas you can execute live compilers, static analyzers (`dart analyze`), and
  test suites (`dart test`). Always empirically test claims before accepting
  them.
- **You are free to disagree**: If a reviewer's claim is technically wrong, if
  their suggestion introduces compiler warnings or regressions, or if the
  existing code is already optimal, mark it as `👎 Disagree`. Explain your
  technical rationale in the triage report and propose NO code changes for that
  item.

## How to use this skill (The Workflow)

- **NEVER GUESS Target PR or Branch**: If the target PR number or branch is not
  explicitly provided by the user, and the current git workspace state is on a
  trunk branch (`main`/`master`), in detached HEAD state, or matches multiple
  open PRs, **DO NOT GUESS**. The agent MUST pause execution and explicitly ask
  the user (using `ask_question` or chat) to clarify which PR or branch to
  target before taking action.

1. **Run `kscripts pr-triage`**: Execute `kscripts pr-triage` (or the bare
   `pr-triage` shim) in your shell tool (`run_command` / `Bash`). Pass `--dir`
   (or `-C`) to specify the target repository or worktree directory:

   ```bash
   kscripts pr-triage --dir <path-to-target-repository>
   ```

   _Note_: If you need to target a specific PR or URL, also pass `--pr`:

   ```bash
   kscripts pr-triage --dir <path-to-target-repository> --pr <pr-number-or-url>
   ```

   **Save the exact, untruncated stdout of this command** as a new markdown
   artifact named `raw_triage_output.md` in the artifacts directory (preserving
   the `> [!IMPORTANT] Reviewer Dropped from Queue` block and all review/thread
   IDs).

2. **Verify Workspace State**:
   - The output shows the PR URL, title, branch, Remote Commit SHA, Local Commit
     SHA, and Sync Status (`in_sync`, `behind_remote`, `ahead_of_remote`,
     `diverged`, or `branch_mismatch`).
   - Verify that your current git branch matches the PR source branch
     (`headRefName`).
   - Check the **Sync Status**:
     - If `Sync Status` is `behind_remote`, pull the latest remote commits
       (`git pull`) before making changes.
     - If `Sync Status` is `ahead_of_remote` or `diverged`, push or sync local
       commits (`git push`).
     - Do not start making code edits while the local workspace is out of sync
       with the remote PR.
   - Check the **Mergeable Status**:
     - If `Mergeable` is `CONFLICTING` (or `mergeStateStatus` is `DIRTY`),
       `kscripts pr-triage` automatically runs `git fetch` + `git merge-tree` +
       `git log` and emits a top-level `## ⚠️ Merge Conflicts` section listing
       the conflicting files and the upstream commits on `origin/<baseRefName>`
       that introduced the clash.
     - Treat merge conflicts as a `🔥 Urgent` blocker in `pr_triage_report.md`,
       even when `Review Decision` is `APPROVED` and all CI status checks are
       passing.
     - Always resolve PR merge conflicts using a forward merge commit
       (`git fetch origin <baseRefName> && git merge origin/<baseRefName>`)
       rather than `git rebase` (since force-pushing is prohibited).

3. **Analyze Open Comments**:
   - The command lists all unresolved review threads, top-level review comments
     (overall review summaries), and general PR conversation comments.
   - Read the conversations carefully to understand what reviewers are
     requesting.
   - Focus _only_ on unresolved or actionable comments. Ignore comments marked
     as resolved unless they provide necessary context.
   - Ignore comments from the PR author themselves unless they clarify a
     reviewer's comment.

4. **Analyze CI Status & Failures**:
   - The command lists status checks (both failed and active/pending).
   - **Active/Pending CI Handling**: If any CI status checks are currently
     running or pending:
     - Inform the user and call `ask_question` to ask their preference:
       - Option 1: `(Recommended) Proceed with triaging open comments now`
       - Option 2: `Wait for active CI status checks to complete first`
     - **MANDATORY HARD BLOCK**: When CI is pending, you MUST halt execution
       after calling `ask_question`. Do NOT proceed to Step 5 (Generate a Triage
       Report) or create the `pr_triage_report.md` artifact until the user has
       answered, because final CI results might change the triage plan and
       action items.
   - **`ACTION_REQUIRED` Checks**:
     - `kscripts pr-triage` marks checks in `state: "ACTION_REQUIRED"` with
       `### ⚠️ <check_name> (ACTION_REQUIRED)` and extracts the CheckRun
       `output.summary`.
     - Distinguish `ACTION_REQUIRED` checks from actual code/test failures:
       these checks have not failed a test suite, but require a manual trigger
       comment or maintainer approval on the PR.
     - Because pushing a new commit resets `ACTION_REQUIRED` checks, **never**
       post a trigger comment before code commits are pushed. Only trigger or
       approve the check after all code fixes for the triage pass have been
       committed and pushed, or when no code changes are needed.
   - Analyze the stack traces, compile errors, or analyzer failures to
     understand why any failed checks failed.

5. **Generate a Triage Report (Artifact)**:
   - **Prereq (Hard Gate)**: If CI status checks are active/pending, you MUST
     NOT generate this report until the user has answered the `ask_question`
     prompt from Step 4.
   - Create a markdown artifact named `pr_triage_report.md` in the artifacts
     directory (using `write_to_file` with `RequestFeedback: true` in
     `ArtifactMetadata` to render an interactive 'Proceed' button).
   - **Link to Raw Output**: Include a markdown link to the
     `raw_triage_output.md` artifact at the top of the report.
   - The report MUST group associated comments and CI failures into cohesive
     action items (you may cluster multiple related comments or failures
     together if they address the same problem).
   - For each action item/group, include:
     - **Summary of Feedback/Failure**: A concise summary of the reviewer
       comment(s) or CI failure(s), including direct markdown links back to the
       comments/checks on GitHub. When linking to comments, use a descriptive
       link that includes both the comment/review number and the GitHub username
       of the reviewer (e.g. `[Comment #1 by @reviewer_username](#)` or
       `[Review #1 by @reviewer_username](#)`).
     - **Thread & Comment/Review Identifiers (For Comments)**: Explicitly
       preserve the `Thread ID` (e.g. `PRRT_...`), `Comment ID` (e.g.
       `3438780787`), or `Review ID` (e.g. `PRR_...`) and numeric `Database ID`
       from the header in `raw_triage_output.md` under each action item so the
       resolution step has immediate access to the identifiers without extra API
       lookups.
     - **Agent Assessment (For Comments)**:
       - **Agreement Level**: A short indicator of your agreement using one of
         these categories:
         - `🔥 Urgent` (Critical fix for a crash, bug, or CI blocker; we should
           fix immediately)
         - `👍 Solid` (Good suggestion; we should implement it)
         - `🤷 Meh` (Optional nit or stylistic preference; we could address it,
           but it's low priority)
         - `👎 Disagree` (Incorrect or counter-productive suggestion; we should
           explain why and propose no action)
       - **Empirical Verification**: Output of `dart analyze` or `dart test` run
         on the unmodified codebase before accepting any fix or classifying a
         claim.
       - **Rationale**: Your technical explanation of why you agree, disagree,
         or recommend a specific direction.
     - **Planned Action**:
       - **Code / Doc Changes**: The target file name(s), specific line ranges,
         and proposed changes (explanation, code snippet/diff, or "No action
         needed").
       - **Test Plan (2-Bucket TDD Filter)**:
         - **Propose Companion Test (`test/..._test.dart` + test case summary or
           snippet)** when the accepted change fixes a bug, adds a branch/edge
           case, or alters runtime behavior.
         - **Explicitly Skip (`None — <concise reason>`)** for copy/string
           literal tweaks, symbol renames, comments/docs, or behavior-preserving
           refactors already covered by existing tests (never propose brittle
           change-detector tests).
   - Present this triage report to the user.

6. **Wait for Approval**:
   - DO NOT edit files or make changes until the user explicitly approves the
     proposed plan via the interactive 'Proceed' button (or explicit chat
     confirmation).

7. **Surgical Implementation & Verification (Red-Green TDD)**:
   - Once approved, address the comments and failures one by one.
   - **Red-Green TDD Execution**:
     - **Test First (Red)**: For action items with an approved companion test in
       **Test Plan**, write or update the test in `test/` (`*_test.dart`) first
       and run `dart test <test_file>` to confirm the new assertion fails (or
       reproduces the edge case) against the unpatched code.
     - **Implementation (Green)**: Apply the production code fix and re-run
       `dart test` to verify all new and existing tests pass.
   - **Sync PR Title & Description**: If addressing review feedback alters
     public APIs, symbol names, or architectural design, update the PR title and
     description (`cat << 'EOF' | gh pr edit <pr> --title "..." --body-file -`)
     so squash-merges do not land outdated commit messages.
   - Follow standard development workflows: run formatting (`dart format`),
     analysis (`dart analyze`), and tests (`dart test`) locally to verify fixes
     before finishing.
   - **Live Read-Only / Dry-Run Smoke Check**: After unit tests and formatters
     pass, if the patch touches a CLI, script, or query with a side-effect-free
     execution path (`--help`, `--dry-run`, `readonly`, `status`/`list`/`view`),
     auto-run it against real state when `<= 15s` and `~0` risk, or explicitly
     offer the read-only verification in Step 8 when `> 15s`.

8. **Verify Git State and Offer Unified Resolution Menu**:
   - **Check Git Status first**: Run `git status -s --untracked=no` to check
     whether uncommitted fixes or unpushed commits exist.
   - **Present Completion Options (`ask_question`)**: Use `ask_question` to
     present a unified completion menu based on the working tree and review
     state (include the `"dismiss stale CHANGES_REQUESTED review"` option
     whenever an open `CHANGES_REQUESTED` review was fully addressed by code
     fixes; promote it to `(Recommended)` when another maintainer has already
     `APPROVED` the PR):
     - **If uncommitted changes or unpushed commits exist**, offer:
       1. `(Recommended) Commit fixes, push branch, reply/resolve, and re-request review if needed`
       2. `Commit fixes, push branch, reply/resolve, dismiss stale CHANGES_REQUESTED review, and re-request review`
          _(include when an addressed `CHANGES_REQUESTED` review exists)_
       3. `Commit fixes and push branch only`
       4. `Commit fixes locally only`
       5. `Do nothing`
     - **If working tree is clean and all commits are pushed**, offer:
       1. `(Recommended) Reply/resolve and re-request review if needed`
       2. `Reply/resolve, dismiss stale CHANGES_REQUESTED review, and re-request review`
          _(include when an addressed `CHANGES_REQUESTED` review exists)_
       3. `Do nothing`
   - **Execute Selected Actions**:
     - If committing is selected, stage all modified and new files and create a
       descriptive commit.
     - If pushing is selected, run `git push`.
     - If replying, resolving, or re-requesting is selected, execute the
       `kscripts pr-triage resolve` and `kscripts pr-triage re-request` commands
       below.

## Replying, Resolving Threads, and Re-Requesting Review

For every addressed inline review thread, execute thread resolution via
`kscripts pr-triage resolve`:

```bash
# Reply to an inline comment and resolve its thread:
kscripts pr-triage resolve --dir <path-to-target-repository> <thread_graphql_id> <comment_database_id> "<your reply body>"

# Or resolve an inline thread without posting a reply:
kscripts pr-triage resolve --dir <path-to-target-repository> <thread_graphql_id>
```

### Re-Requesting Review & Dismissing Addressed `CHANGES_REQUESTED` Reviews (`kscripts pr-triage re-request`)

When a human reviewer submits any review (`COMMENTED`, `CHANGES_REQUESTED`, or
an `APPROVED` review that is later `DISMISSED` by new commits), GitHub removes
that reviewer from `reviewRequests`. Posting a comment or dismissing a review
alone does **not** put the PR back into their GitHub Review Queue
(`is:open is:pr review-requested:@me`).

However, you MUST NOT run `re-request` (`--add-reviewer`) when a reviewer's
latest state is still `APPROVED` (e.g., when no new commits were pushed, or in
repositories where `dismiss_stale_reviews` is `false`), as `--add-reviewer`
revokes their active approval.

Check whether re-requesting review is needed:

- **If no new commits were pushed in Step 8**: Rely directly on the
  `**Review Requests**` line and `> [!IMPORTANT] Reviewer Dropped from Queue`
  banner in `raw_triage_output.md` (do **not** make an extra `gh pr view` call).
- **If new commits were pushed in Step 8**: Inspect the post-push review state
  (in case `dismiss_stale_reviews` dismissed a prior approval):
  ```bash
  gh pr view <pr_number> -R <owner/repo> --json reviewDecision,latestReviews,reviewRequests
  ```

Run `kscripts pr-triage re-request` **ONLY when ALL conditions hold**:

1. The human reviewer is **not** currently listed in `reviewRequests`, **AND**
2. Their latest review state in `latestReviews` is **NOT** `"APPROVED"` (i.e.
   `COMMENTED`, `CHANGES_REQUESTED`, or `DISMISSED`), **AND**
3. You have pushed commits or posted a reply addressing their feedback since
   their review was submitted.

```bash
# Re-request review (with optional top-level reply comment):
kscripts pr-triage re-request --dir <path-to-target-repository> <reviewer_login> \
  [--comment "<top_level_reply_body>"]

# Dismiss an addressed CHANGES_REQUESTED review AND re-request review atomically
# (when selected by the user in Step 8):
kscripts pr-triage re-request --dir <path-to-target-repository> <reviewer_login> \
  [--comment "<top_level_reply_body>"] \
  --dismiss <review_database_id> \
  -m "Addressed in <short_sha> (<concise summary>); re-requesting review from @<reviewer_login>."
```

- **GitHub State-Machine Quirk (`reviewDecision` vs. `latestReviews`)**:
  Re-requesting review without `--dismiss` adds `<login>` back to
  `reviewRequests` (`🟡 Re-review Requested`) and hides `<login>` from
  `latestReviews`, while `reviewDecision` remains `"CHANGES_REQUESTED"` until
  `<login>` approves or the review is dismissed. Conversely, dismissing a review
  without `--add-reviewer` drops `<login>` from `reviewRequests`. Using
  `kscripts pr-triage re-request <login> --dismiss <id>` guarantees both run
  together.
- **Stop When Already Queued**: If `<login>` is already in `reviewRequests` and
  all their feedback is addressed on the latest commit, **STOP** — never re-run
  `re-request` and never re-triage their addressed top-level review.

## Constraints

- **Hard CI Gate**: If CI checks are running or pending, you MUST halt execution
  after calling `ask_question` in Step 4 and DO NOT proceed to Step 5 or
  generate `pr_triage_report.md` until the user responds, as pending CI results
  may alter the final triage plan.
- **CRITICAL**: You MUST NOT modify files or make any code edits to address PR
  comments or CI failures before generating a `pr_triage_report.md` artifact and
  obtaining explicit user approval on the plan.
- **VCS Authorization**: Selecting an option in `ask_question` that explicitly
  mentions committing or pushing serves as the user's explicit permission to
  perform those operations for the triage fixes. Do NOT ask for permission a
  second time if the user selects one of those options.
- **Sync Code Before Comments**: Do not post "Done" or "Fixed" comment replies
  or resolve threads on GitHub while the corresponding code fixes remain
  uncommitted or unpushed.
- Do NOT address resolved comments unless requested.
- **NO `commit --amend`**: Modifying commit history via `git commit --amend` is
  strictly prohibited. Always create new, atomic commits.
- **NO Force Pushes**: Force pushing (`git push -f` or `--force-with-lease`) is
  strictly prohibited under any circumstances.
- Always use `kscripts pr-triage` to fetch PR information instead of manual API
  calls to ensure consistency and minimize context bloat.
