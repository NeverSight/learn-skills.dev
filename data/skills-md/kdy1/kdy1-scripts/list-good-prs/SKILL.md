---
name: list-good-prs
description: List open pull requests in the current GitHub repository that are CLEAN or UNSTABLE and have a +1 reaction from chatgpt-codex-connector[bot]. Use when the user asks for good or bot-approved PRs; this skill only reports them and never changes repository state.
---

# List Good PRs

Report the current repository's open pull requests that satisfy both of these
conditions:

- GitHub `mergeStateStatus` is exactly `CLEAN` or `UNSTABLE`.
- The pull request itself has a `+1` reaction from
  `chatgpt-codex-connector[bot]`.

Reactions on reviews, review comments, and issue comments do not qualify.

## Workflow

1. Confirm that `gh` and `jq` are installed, `gh` is authenticated, the current
   directory belongs to a Git repository, and
   `gh repo view --json nameWithOwner,url` resolves a GitHub repository.
2. Enumerate open PR numbers, then fetch each PR individually and filter the
   individual result. Do not request or filter `mergeStateStatus` from
   `gh pr list`: its aggregate results can disagree with a direct PR query.
3. For each `CLEAN` or `UNSTABLE` PR, use GitHub's issue reactions endpoint to
   fetch every page of top-level `+1` reactions. Pull requests use their PR
   number as the issue number for this endpoint. Match the actor login exactly.

   Run this read-only Bash query from the repository:

   ```bash
   set -euo pipefail

   open_pr_numbers="$(
     gh pr list --state open --limit 1000 --json number --jq '.[].number'
   )"
   good_prs=()

   if [[ -n "$open_pr_numbers" ]]; then
     while IFS= read -r pr_number; do
       eligible_pr="$(
         gh pr view "$pr_number" \
           --json number,title,url,author,headRefName,baseRefName,mergeStateStatus,isDraft,updatedAt \
           --jq 'select(.mergeStateStatus == "CLEAN" or .mergeStateStatus == "UNSTABLE")'
       )"

       if [[ -z "$eligible_pr" ]]; then
         continue
       fi

       reactions="$(
         gh api --paginate --slurp \
           -H 'Accept: application/vnd.github+json' \
           "repos/{owner}/{repo}/issues/${pr_number}/reactions?content=%2B1&per_page=100"
       )"
       has_bot_plus_one="$(
         jq -r \
           'any(.[][]; .content == "+1" and .user.login == "chatgpt-codex-connector[bot]")' \
           <<< "$reactions"
       )"

       if [[ "$has_bot_plus_one" == "true" ]]; then
         good_prs+=("$eligible_pr")
       fi
     done <<< "$open_pr_numbers"
   fi

   if ((${#good_prs[@]} > 0)); then
     printf '%s\n' "${good_prs[@]}"
   fi
   ```

4. Treat the newline-delimited JSON objects emitted after all queries succeed
   as authoritative. Include only PRs that satisfy both conditions; do not
   infer approval or mergeability from another field, review, or comment.
5. Report the repository name and result count, followed by a Markdown table
   containing:
   - linked PR number and title
   - `mergeStateStatus`
   - author login
   - base and head branches as `base ← head`
   - update time
6. If the result is empty, explicitly say that the repository has no open PRs
   that are `CLEAN` or `UNSTABLE` and have a `+1` reaction from
   `chatgpt-codex-connector[bot]`.

## Failures

- If `gh` is missing, explain that GitHub CLI is required.
- If `jq` is missing, explain that `jq` is required.
- If authentication fails, report it and suggest `gh auth login`.
- If the directory is not a Git repository, ask the user to run the skill from
  a repository or provide one explicitly.
- If no GitHub remote can be resolved, report that fact and suggest configuring
  the remote or specifying `--repo OWNER/REPO`.
- If the list query, any individual PR query, any reactions query, or `jq`
  processing fails, show the concise error and stop. Never present a failed or
  partial query as an empty or complete result.

This skill is read-only. Never merge, close, label, comment on, react to, or
otherwise modify a pull request or repository.
