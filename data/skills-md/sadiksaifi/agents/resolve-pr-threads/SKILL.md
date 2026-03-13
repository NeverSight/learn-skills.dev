---
name: resolve-pr-threads
description: Fetch ALL unresolved PR conversations — review threads, review body comments, and regular PR comments — then output a strict /tdd plan with atomic commits that fixes and replies to every one. Use this skill whenever the user wants to resolve, address, or fix PR review feedback, comments, threads, nitpicks, or suggestions from any reviewer (human or bot like CodeRabbit, Copilot, etc.). Triggers on phrases like "resolve PR threads", "fix PR comments", "address review feedback", "resolve conversations".
---

## Plan PR Thread Resolution

### Input (optional)

`reviewers`: string | string[] | empty

- empty → all authors
- provided → only those authors
- replies must tag actual thread/comment author `@<author>`

---

## You are in PLAN MODE

Make a plan to resolve all selected unresolved conversations.
Output plan only. Do not execute changes.

---

## Steps (planning)

### 1) Fetch ALL PR conversations

The most common failure mode is missing feedback that lives outside of "unresolved review threads." GitHub PRs have three distinct conversation surfaces. You must query all three — skipping any surface means silently ignoring real feedback.

**Surface A — Review threads (inline comments + replies)**
Fetch via `gh api` on the pull request review comments endpoint. These are inline code comments and their reply chains. Filter to threads where `isResolved == false` or where the thread has no resolution status (regular comments).

**Surface B — Review body comments**
Fetch all reviews via `gh api` on the pull request reviews endpoint. A review can have a non-empty `body` containing feedback (nitpicks, suggestions, summaries) that is NOT posted as an inline thread. These are invisible to thread-only queries. Filter to reviews whose `body` is non-empty and non-boilerplate (skip empty bodies and pure "APPROVED"/"CHANGES_REQUESTED" status-only reviews with no substantive body text).

**Surface C — PR-level comments (issue comments)**
Fetch via `gh api` on the issue comments endpoint (`/repos/{owner}/{repo}/issues/{pr_number}/comments`). These are top-level PR comments not tied to any review. Include any that contain actionable feedback.

**After fetching all three surfaces:**
- Deduplicate (a comment might appear in both a review body and as a thread)
- Apply `reviewers` filter if set
- Exclude already-resolved threads (but include everything from Surface B and C that hasn't been explicitly addressed)

**Key rule**: If a review is marked "COMMENTED" and has body text with actionable feedback, it counts — regardless of whether GitHub considers it an "unresolved thread." Bots like CodeRabbit, Copilot, Sweep, etc. often put their feedback here.

### 2) Triage (for the plan)

For each unresolved conversation decide `fix` or `reply-only`. Capture:

- conversation type: `thread` | `review-body` | `pr-comment`
- thread/comment URL or ID
- file + line (if applicable; review-body and pr-comments may not have one)
- author to tag
- 1-line summary of what's being asked

### 3) Make the plan

The plan must explicitly state:

#### Fix/commit phase (for `fix` items)

- `/tdd` per issue (RED → GREEN → REFACTOR → COMMIT)
- **Atomic rule**: 1 issue = 1 commit; no mixed commits
- Record commit hash per fixed conversation (conversation → commit mapping). The executor performs the commit, captures the hash, and substitutes it into the reply's `{{COMMIT_HASH}}` placeholder before posting.

#### Push phase

- Push once after all fix commits are completed

#### Reply/resolve phase (for ALL items: `fix` + `reply-only`)

- Reply inline on the exact thread, review, or comment
- Tag `@<author>`
- **Pre-write the reply text in the plan** (executor must not re-fetch to draft replies)
- If `fix`: reply must include the placeholder `{{COMMIT_HASH}}` where the commit SHA should go. The executor will substitute this with the actual hash after committing. Example: `"Fixed in {{COMMIT_HASH}}."` → executor posts `"Fixed in a1b2c3d."`
- If `reply-only`: concise technical answer or justification (no placeholder needed)
- Close/resolve the thread (for threads that support resolution)
- For review-body and pr-comments that can't be "resolved" via GitHub's thread resolution, reply to acknowledge and mark as addressed

#### Coverage

- Every selected unresolved conversation must appear in the plan
- No conversation omitted — threads, review body comments, and PR comments alike
- No final sweep
- No PR-wide summary comment
