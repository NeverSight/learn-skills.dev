---
name: review-pr
description: Review a Gitea pull request with tea and post one review. Takes the PR number.
allowed-tools: Bash, Read, Grep, Glob
disable-model-invocation: true
---

# Review PR

Use `gitea` for target resolution, authentication, command selection, and mutation verification. This skill owns Gitea review output and submission.

## 1. Read the PR

```bash
N=743
tea pulls "$N" --fields index,title,state,author,url,body,mergeable,base,head --output yaml
tea pulls "$N" --fields diff --output simple
```

Read the body and full diff. Identify changed files and verify the change against its stated intent.

## 2. Trace the surrounding code

Before forming findings, inspect:

- **Consumers.** Search callers of changed public methods. Missing local callers require checking the spec, exports, documentation, and external compatibility promises. Flag speculative generality only with evidence of no supported requirement.
- **Removed behavior.** Compare replacements with removed helpers, preserving cleanup, tracing, and error handling. Look for dropped metrics and resource leaks.
- **Failure paths.** Trace `finally`, exceptions, cancellation, and partial work. Check whether caching or finalization can occur on failure.
- **Substitutability.** Investigate type-sniffing such as `isinstance` or `inspect.isawaitable` on shared methods for LSP/OCP violations.

## 3. Form the review

Favor surgical, SOLID, extensible changes. Each finding needs `file:line` and a concrete consequence rather than a style preference.

Default to severity order: Blocking, Should fix, Minor/nits, then a short What's good section. When the user explicitly requests `code-review`'s two-axis format, preserve Standards and Spec sections without globally reranking them.

Choose `REQUEST_CHANGES`, `APPROVE`, or `COMMENT`.

## 4. Show, submit, verify

Present the review in chat. Post within existing explicit authorization; otherwise ask before posting. Save the body to a scratch Markdown file, then execute exactly one matching command:

```bash
BODY_FILE=/tmp/review.md
tea pulls reject "$N" "$(cat "$BODY_FILE")"   # REQUEST_CHANGES
tea pulls approve "$N" "$(cat "$BODY_FILE")"  # APPROVE
tea api --method POST "repos/{owner}/{repo}/pulls/$N/reviews" \
  -f event=COMMENT -F "body=@$BODY_FILE"       # COMMENT
```

COMMENT creates a [pull-request review](https://docs.gitea.com/api/operations/repo-create-pull-review/), not an issue comment. Submit one review, adding inline comments only when requested. Verify its state and body, then report the verdict and PR URL.

On failure, follow `gitea`'s target-resolution and authentication guidance before retrying.
