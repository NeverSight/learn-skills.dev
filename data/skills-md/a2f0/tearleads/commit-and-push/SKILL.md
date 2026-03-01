---
name: commit-and-push
description: Commit staged changes and push to the remote using conventional commits with GPG signing. Use when you need to commit and push work, create a PR if missing, and wait for Gemini review before addressing feedback.
---


# Commit and Push

Commit staged changes, push the branch, create a PR if needed, and handle initial Gemini review.

## Setup

Determine the repository for all `gh` commands:

```bash
REPO=$(./scripts/agents/tooling/agentTool.ts getRepo)
```

Always pass `-R "$REPO"` to `gh` commands.

Track these state flags during execution:

- `gemini_quota_exhausted`: Boolean, starts `false`. Set to `true` when Gemini returns its daily quota message.
- `used_fallback_agent_review`: Boolean, starts `false`. Set to `true` after running one fallback cross-agent review.
- `deferred_items`: Array of `{thread_id, path, line, body, html_url}`, starts empty. Populated by `$address-gemini-feedback` when review feedback is deferred rather than fixed on-the-fly. Pass this state to `$enter-merge-queue` for issue creation.

## Workflow

1. Check branch:
   - If on `main`, create a new branch named for the change.
   - After creating/switching, update the VS Code title:

   ```bash
   ./scripts/agents/tooling/agentTool.ts setVscodeTitle
   ```

2. Analyze changes:
   - Run `git status` and `git diff --staged` to confirm what will be committed.
   - If tooling reports actions but `git status` shows no unexpected changes, proceed without asking about generated files.

3. Commit format:
   - Follow `CLAUDE.md` commit guidelines (conventional commits, GPG signed with 5s timeout, no co-author lines, no footers).
   - **Header must be ≤ 50 characters** (enforced by commitlint `header-max-length`). The header is the entire first line: `type(scope): description`. To ensure adherence, count characters before committing. If too long, shorten the scope or description:
     - Drop the scope: `feat: add redis and garage reset scripts`
     - Abbreviate: `feat(scripts): add reset scripts` (put details in body)
     - Use a broader verb: `feat(scripts): add stack reset tooling`
   - Do not bump versions here.

4. Push:
   - Push the current branch to the remote after the commit.
   - The pre-push hook runs full builds and tests; set a long timeout and do not assume timeouts mean failure.

5. Verify push completed:
   - Before proceeding to PR creation or Gemini follow-up, verify the push actually completed:

   ```bash
   BRANCH=$(git branch --show-current)
   git fetch origin "$BRANCH"
   [ "$(git rev-parse HEAD)" = "$(git rev-parse origin/$BRANCH)" ] || echo "NOT PUSHED"
   ```

   - **Do NOT proceed to step 6 or 7 until verification passes.** Replying to Gemini with "Fixed in commit X" when X is not visible on remote creates confusion.

6. Open PR:
   - If no PR exists, create one with `gh pr create`.
   - Do not include auto-close keywords (`Closes`, `Fixes`, `Resolves`).
   - Use the Claude-style PR body format and include the evaluated agent id.
   - Avoid shell interpolation bugs in PR bodies: always build body content with a **single-quoted heredoc** and pass it via `--body-file` (or `--body "$(cat ...)"` only when no backticks/$/[] are present).

   Compute the agent id:

   ```bash
   AGENT_ID=$(basename "$(git rev-parse --show-toplevel)")
   ```

   PR body template (fill in real bullets, keep section order). Prefer this safe pattern:

   ```bash
   PR_BODY_FILE=$(mktemp)
   cat <<'EOF' > "$PR_BODY_FILE"
   ## Summary
   - <verb-led, concrete change>
   - <second concrete change if needed>

   ## Testing
   - <command run or "not run (reason)">

   ## Issue
   - #<issue-number>

   Agent: __AGENT_ID__
   EOF
   sed -i'' -e "s/__AGENT_ID__/${AGENT_ID}/g" "$PR_BODY_FILE"
   gh pr create ... --body-file "$PR_BODY_FILE"
   rm -f "$PR_BODY_FILE"
   ```

   If there is no associated issue, replace the `## Issue` section with:

   ```text
   ## Related
   - <link or short reference>
   ```

   - After creating the PR, run:
     - `./scripts/agents/tooling/agentTool.ts setVscodeTitle`
     - `./scripts/agents/tooling/agentTool.ts tagPrWithTuxedoInstance`

7. Wait for Gemini:
   - Wait 60 seconds for Gemini Code Assist to review.

8. Check for quota exhaustion:
   - Gemini quota exhaustion can happen during the initial wait OR later follow-up interactions.
   - Check all Gemini response surfaces for the quota message:

   ```bash
   ./scripts/agents/tooling/agentTool.ts checkGeminiQuota --number "$PR_NUMBER"
   ```

   Treat `quota_exhausted: true` in the JSON response as quota exhaustion.

   - If found:
     - Set `gemini_quota_exhausted=true`.
     - If `used_fallback_agent_review=false`, run one fallback cross-agent review (Codex):

     ```bash
     # Equivalent skill invocation: /cross-agent-review codex
     ./scripts/agents/tooling/agentTool.ts solicitCodexReview
     ```

     - Set `used_fallback_agent_review=true`.
     - Skip further Gemini follow-ups for this run.
     - Proceed to `/enter-merge-queue` or end the skill.

9. Address feedback:
   - If `gemini_quota_exhausted=false`, run `$address-gemini-feedback` for unresolved comments.
   - When replying to Gemini, **always tag `@gemini-code-assist`** to ensure it receives a notification.
   - Reply to Gemini with `./scripts/agents/tooling/agentTool.ts replyToGemini --number <pr> --comment-id <id> --commit <sha>` (not `gh pr review`).
   - Use `replyToComment` only for custom non-fix responses.
   - Re-run step 8 after each Gemini interaction. If quota appears later, switch to fallback immediately.
   - `$address-gemini-feedback` may populate `deferred_items` if any feedback is deferred rather than fixed on-the-fly.

10. Report state for downstream skills:
    - PR number and URL
    - Whether Gemini quota was exhausted
    - Any `deferred_items` that were collected

    If `deferred_items` is non-empty, mention that `$enter-merge-queue` will create a tracking issue with the `deferred-fix` label after merge.

## Token Efficiency (CRITICAL)

**MANDATORY**: ALL git commit and push commands MUST redirect stdout to `/dev/null`. Failure to do this wastes thousands of tokens on hook output.

```bash
# CORRECT - always use these forms
git commit -S -m "message" >/dev/null
git push >/dev/null

# WRONG - NEVER run without stdout suppression
git commit -m "message"  # Burns 1000+ tokens on pre-commit output
git push                 # Burns 5000+ tokens on pre-push output
```

**Why this is non-negotiable**:

- Husky pre-commit hooks output lint results, type-check results
- Husky pre-push hooks run full test suites and builds
- A single unsuppressed `git push` can add 5,000+ lines to context
- Errors go to stderr, which `>/dev/null` preserves
