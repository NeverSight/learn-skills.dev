---
name: contributions-implement
description: >
  Implement a chosen contribution in a fork of an open-source project: verify the user's fork
  already exists (stop and ask the user to fork if it does not), strictly follow the upstream
  repository's conventions (CONTRIBUTING.md, AGENTS.md, CLAUDE.md, PR template, commit and
  sign-off format), work on a branch of the fork without opening any fork PR, write
  equivalence-first tests, run the upstream CI/CD checks locally before pushing (the fork will
  not run them), sign commits per the upstream DCO/CLA convention, and post the PR body — built
  from the upstream PR template — in a markdown pasteable format on the Multica issue. In review
  iterations (the PR is already open and a maintainer left review comments), address only the
  explicit requests on the same fork branch and post a pasteable PR comment per PR in the same
  fenced-markdown format; PR discussions — replies, resolutions, ambiguous asks — are left for
  the humans. Use whenever a Multica issue asks to "work on the contribution", "implement
  <candidate> in <owner/repo>", "prepare the branch for <repo>", "turn the scouted contribution
  into a PR-ready diff", or to "address the review comments on <PR>" — even if the issue only
  names the target repo and the change to make.
license: Apache-2.0
metadata:
  author: mmontes11
  version: "1.4"
compatibility: Requires the multica CLI, a local toolchain for the target repo's language, and GitHub access (GitHub MCP tools and the authenticated gh CLI) to both the upstream repo and the user's fork.
allowed-tools: Read, Grep, Bash(multica:*), Bash(gh:*), Bash(git:*)
---

# Implement a contribution in a fork

One contribution per run. The run's **Multica issue** names the target repository (owner/repo) and
the change to make. There are two shapes. In the **initial run**, the deliverables are a
**pushed branch in the user's fork** and a **Multica comment carrying a pasteable PR body** that
follows the upstream PR template; no PR is opened anywhere — the user opens the upstream PR after
validating the branch. In a **review iteration** (the PR is already open and maintainers left
review comments), the deliverable is a push to the **same fork branch** plus a **pasteable PR
comment** per PR on the Multica issue — and the PR discussion itself stays with the humans.

## Scope

- **In:** verify the fork; read the upstream conventions; tests first; implement; run the upstream
  CI checks locally; commit with the correct sign-off; push the fork branch; write the PR body;
  in review iterations, address the explicit review comments on the same branch and write the
  pasteable PR comment; post the deliverable comment.
- **Out (hard):** creating the fork, opening a PR against the fork, opening a PR against upstream,
  merging anything, force-pushing, replying to or resolving PR review threads, editing the PR
  body, or deciding what an unresolved discussion means.

## Hard gate: the fork must already exist

The fork is created by the **user**, never by you. Before any other work, verify a fork of the
upstream repo exists under the user's account (e.g. `gh api repos/<user>/<repo>` returning `fork:
true`, or the fork metadata via the GitHub MCP tools). If it does not exist, **stop immediately and
ask the user to fork the repo** — do not fork it yourself and do not start other work before the
fork is there. A fork you create silently is not the same deliverable: the user chose to own the
fork relationship.

## Procedure

1. **Read the upstream conventions before writing any code.**
   - Agent-facing docs at the root — `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md` (whichever exist) —
     plus the issue and PR templates (`.github/PULL_REQUEST_TEMPLATE*`) and any contribution or
     AI-PR policy in the tracker.
   - Commit conventions (Conventional Commits or otherwise), DCO vs CLA, and the CI expectations:
     which commands the upstream workflows run, and which tool versions are pinned (Makefile
     `make lint` targets, `.golangci.yml`, workflow `go-version`, etc.).
   - The code style of the exact files you will touch: naming, error handling, test framework, and
     existing helpers to reuse rather than reinvent.
   If upstream forbids fully AI-generated PRs, or requires a CLA the user has not signed, record it
   and stop — do not push on.
2. **Prepare the branch.** Clone or fetch the fork. Base the new branch on the **upstream default
   branch** (fetch upstream explicitly; do not assume the fork's head is current). Name it
   `feature-<short-name>` or `fix-<short-name>` — never a generic agent-generated branch name.
3. **Tests first, equivalence first.** Before changing behavior, add tests for the paths the change
   touches — especially branches that have no coverage today. Run them against the **unmodified**
   code: they must pass unmodified. A test that only passes after the change proves the new
   structure works; a test that passed before proves the behavior is the same, which is what a
   reviewer needs to trust a refactor.
4. **Implement the change.** One logical change, minimal diff — no unrelated refactors, renames,
   deletions, or formatting tweaks. Match the repo's conventions from step 1 exactly.
5. **Run the upstream CI/CD checks locally, before pushing.** The fork will not run upstream
   CI/CD, so nothing else will. Reproduce what the upstream workflows run: the build, the package's
   test suite (with race/sanitizer flags where the repo uses them), and the repo's lint target with
   the **pinned tool versions** (a lint pass on a newer linter is not the same evidence). Reproduce
   what the upstream workflows run, no more: flags they do not use (an added `-race`, a sanitizer)
   are slower evidence, not better, and a repo-wide build is unnecessary when the package's test
   run already compiles the touched package and its dependencies. Run each checkpoint **once**, as
   a single chained shell command (baseline pass on the unmodified code; final pass after the
   change) — re-run only the specific check that failed. Read the actual terminal output and
   confirm it is green; do not assume success from a quiet exit.
6. **Commit with the correct sign-off.** Respect the upstream sign-off convention: for DCO repos,
   sign with the user's identity so the commit carries `Signed-off-by: Name <email>`
   (`git commit -s`). Never change the git identity for the task, and never commit secrets.
   Commits must never carry a `Co-Authored-By` trailer — not one crediting the agent, the
   platform, or any tool: those identities have no CLA, and upstream CI that checks the CLA
   fails on them. The agent platform can append such a trailer automatically when the commit
   is made, so verify the message after committing (`git log -1 --format=%B`), and if a
   `Co-authored-by:` line is present, rewrite it out of the last commit **before pushing**:

   ```sh
   git update-ref HEAD "$(git commit-tree "HEAD^{tree}" -p HEAD^ -m "$(git log -1 --format=%B | grep -v '^Co-authored-by:')")"
   ```

   Do not `git commit --amend` for this: amend re-runs the commit hooks and the trailer comes
   back; `commit-tree` bypasses them.
7. **Re-read the diff, then push.** Review the generated diff for scope creep, then push the branch
   to the fork's origin. **Do not open a PR against the fork** — a fork PR shows up in the
   upstream's PR timeline and pollutes it with updates the maintainers will never review. The
   pushed branch alone is the deliverable.
8. **Write the PR body from the upstream PR template.** Use the **target repo's own template
    exactly**: its sections, headings, and checkboxes, in the template's order. Do not import
    sections from another repo's template — the body's structure is whatever the target repo
    defines. Fill in what it does, the motivation (linked to the upstream issue if one exists),
    and the exact testing commands with their results (in the template's testing section if it
    has one). Then append the AI disclosure note at the end, after the template's sections.

    The note is a **must-have, not optional**: the PR body must acknowledge that the change was
    drafted with AI assistance **and** that a human reviewed it before the PR was submitted. Both
    halves are required — the AI disclosure and the human review. Example wording (from
    kubernetes-sigs/external-dns PR #6846 — adapt to the repo's tone if needed):

    > Note: this change was drafted with AI assistance and reviewed locally before submission.

    Never drop the note, and never claim a human review that did not happen.
9. **Post the deliverable comment** on the Multica issue
    (`multica issue comment add <issue-id> --content-file <path>`). It must carry:
    - The branch name and the fork URL with a link to the branch diff.
    - The verification summary: the exact commands run (tests, lint, CI-equivalent checks) and
      their results.
    - The PR **title and body in a fenced markdown block**, pasteable as-is for the upstream PR.
      The user will copy the block's content straight into the upstream PR form, so the **PR
      title is the first line inside the fence**, followed by a blank line and the body in the
      format defined by the **target repo's own PR template** — its sections, headings, and
      checkboxes verbatim, in the template's order — with the exact testing commands and their
      results (in the template's testing section if it has one), and the AI disclosure note
      appended at the end after the template's sections. The fence is the one constant across
      repos; the body's structure is never assumed, only read from the target repo's template.
      **Never render the PR body as live markdown in the comment** — rendered headings, bold
      titles, and checkbox widgets cannot be copied back into the template, which defeats the
      purpose of the deliverable. It must appear verbatim inside a ` ```markdown ` fence. For
      several PRs in one comment, label each section (e.g. `### 1. <title>`) with its branch
      and commit, and put one fenced block per PR. Shape of the deliverable:

      ````markdown
      ### 1. `refactor(scope): <title>`

      ```markdown
      refactor(scope): <title>

      <the target repo's PR template sections, verbatim and in order>

      <testing commands and their results, if the template has no section for them>

      Note: this change was drafted with AI assistance and reviewed locally before submission.
      ```
      ````
    - A closing line: **no PR was opened anywhere — the branch sits in the fork, and opening the
      upstream PR is the user's call.**
10. **Close out.** Set the issue status per the platform workflow once the deliverable is posted.

## Review iterations (the PR is already open)

When the issue or a comment asks to address maintainer review comments on a PR the user has
already opened, the branch and the PR exist — the work is a fix iteration, not a new
contribution:

1. **Read the review threads verbatim** (GitHub MCP `pull_request_read` with
   `get_review_comments`, paginated). Work from the exact comment text and suggested code, never
   a paraphrase or a summary of an earlier turn.
2. **Split the threads into explicit requests and discussions.** An explicit request is an
   instruction or a concrete suggestion block — implement it exactly. A discussion — a question,
   a "Maybe …?" proposal, a trade-off remark, a "fine as is" note — is **not** yours to answer:
   flag it in the deliverable comment for the human, and implement nothing for it unless the
   human has already decided in a comment.
3. **Never assume what a discussion resolves to.** If a thread is ambiguous, leave the code
   alone and surface the question. The human reads the thread and decides; the resolution — not
   your guess — is what a later iteration implements.
4. **Verify and push to the same fork branch.** Same evidence bar as the initial run (build,
   tests, lint with the pinned tooling, inspected output). Pushing updates the open PR in place;
   never open a new branch or a new PR for review fixes. Commits follow the step-6 sign-off
   rule — user identity, `Signed-off-by`, and no `Co-Authored-By` trailers.
5. **Post a pasteable PR comment for every PR that received new changes.** Every iteration that
   pushes new commits gets one — even if it touches only a subset of the PRs, in which case only
   those get a block. Same format rules as the pasteable PR body: a fenced ` ```markdown ` block
   per PR, pasteable verbatim into the PR conversation, never rendered live. It thanks the
   reviewer, names the new commit, and answers each explicit review comment in order with what
   was done. Flagged discussion items are listed in the Multica comment, not in the pasteable
   block, unless the human wants to put a question to the reviewer.
6. **Leave the PR to the humans.** You do not reply to, resolve, or edit review threads, and you
   do not edit the PR body or description — if a comment demands a PR-body change and you cannot
   make it, hand the exact needed edit to the human in the deliverable comment. The human pastes
   the PR comment, follows the discussion, resolves the threads, and merges.

## Conventions this run followed (beyond the steps above)

- **Toolchain pinned to the repo.** Verify the language toolchain the repo requires (e.g. the
  `go.mod`/`GOTOOLCHAIN` requirement, the linter version pinned by the Makefile or CI) before
  running anything — a green build on the wrong toolchain is false evidence.
- **Narrow reads, bounded context.** Read the narrowest slice needed — one path, one line range,
  one diff — and summarize learnings before fetching more. Never dump whole files or unpaginated
  logs into the conversation.
- **Fewer, batched calls.** In long runs the conversation is re-sent on every tool call, so the
  call count — not the commands — dominates cost. Combine independent steps into one chained shell
  command, read a range once instead of re-reading it, and never re-fetch what is already in
  context.
- **Parse-only tools for ranking and re-measuring metrics.** When the task is to rank code by a
  metric (e.g. cyclomatic complexity) or to re-measure it after a refactor, use a parse-only
  analyzer that needs no build (Go: `gocyclo -over N ./pkg/`); reserve the repo's pinned linter
  for the final package-level CI evidence, not for ranking or re-measurement.
- **Whole-function edits, not cascades.** Read the full line range of a function once, then
  replace the whole function in a single edit. Cascading many small edits is where whitespace
  mismatches and indentation damage come from.
- **Pipes hide failures.** Never pipe a verification command into `grep` or `head` when its
  success is the evidence: a failing tool still prints lines a filter can drop, and the exit
  status is lost — an empty "scan" may be a failed command, not a clean result.
- **Lightweight clones.** When managing the clone yourself, use a blobless or shallow clone
  (`git clone --filter=blob:none`, or `--depth` when full history is not needed) — history stays
  available on demand and the initial transfer is far smaller.
- **One branch per logical change.** If the work spans several independent changes, do one per
  branch and report them separately, so the user can open, sequence, or discard them independently.
- **Verification is evidence, not ritual.** Every command's real output must be inspected
  (tests passing, lint "0 issues", build silence), and the summary must quote what was run and
  what it reported — a "tests pass" claim without the command and the observed result is not a
  verification.
- **Stop at the deliverable.** The moment the branch is pushed and the comment is posted, the work
  is done. Wait for the human to validate and open the upstream PR; do not chase CI, reviews, or
  merges on your own. In review iterations the same holds for the discussion: the threads, the PR
  body, the resolutions, and the merge are the human's — your push and the pasteable PR comment
  are the entire deliverable of the iteration.
