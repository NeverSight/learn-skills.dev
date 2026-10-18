---
name: merge-renovate-pull-requests
description: This skill is used to attempt to merge in pull requests opened by Renovatebot, but which are not automatically merged.
---

# Merge renovate pull requests

## When to use:

When doing routinely maintenance and when Renovatebot has created pull requests which are not automatically merged. They pull requests may not have been automatically merged because there's a major version update, the checks failed or other reasons.

## Caveats:

- Do not attempt to process pull requests which are not created by Renovatebot (username might be `renovate` and author id might be `app/renovate`).
- We should only process open pull requests.
- When updating versions with breaking changes (updating major versions or if the major version is 0) then it's very important to read and understand all the breaking changes and how to update correctly/safely. The breaking changes, and sometimes links to official documentation, can be found in the pull request description or in the changelog of the GitHub repo of the dependency to update. We should follow the official migration guides if available. If the changes are significant, affect the architecture and/or requires migrations on external systems like databases or production systems then we should leave it to the user to resolve it manually. Leave a comment in the pull request explaining this and then abort the current workflow.

## Tools:

You may use the GitHub CLI to get fetch pull requests from the GitHub repo, see results from checks etc.

## Merge exceptions:

- eslint / eslint monorepo should not be updated to >= v10 yet because they haven't patched a bug.

## Adding logs of agent merges:

1. When we want to log agent merges we append the following information to `AGENT_MERGE.md` (in the root folder of the repo).

   ```
   # {agent merge concise title}

   Date: {date and time}

   {summary of changes}

   ## Breaking changes

   {bullet list of the breaking changes; include a short description of the actual breaking changes and including links to official sources for reading more}

   ## Pull requests

   {bullet list with links to pull requests}

   {comments header and comments if there are any}

   {separator between entries, use the `---` separator}
   ```

2. Then we commit and push the changes.

# Main workflow:

- Before starting a workflow make sure:
  1. You are on the `main` branch and pull latest git changes.
  2. You have installed latest package versions (with e.g. `pnpm install`).
  3. Have created a new branch named in this format `agent-merge-{yyyy}-{MM}-{hh}-{mm}-{ss}` (replace placeholders/vars with current date in UTC) and PR with a title containing the dependencies (main ones if many) and suffixed with `(agent merge)`.
     - This is the branch/PR you will be working on during the workflow. You should not merge individual updates/commits directly into the `main` branch, but rather merge the PR into the `main` branch after all open pull requests have been processed.
- Commit often when suitable.
- Do not close processed PRs, these will automatically be handled by renovatebot once the pull request is merged in.
- Do not delete any branches.

## 1. Processing open pull requests where all checks passed:

1. Merge in open pull requests (by renovatebot) where all checks have passed.
2. Install latest package versions (with e.g. `pnpm install`).
   - Make sure we are using the latest transitive dependencies in case there are merge conflicts.
3. Run type checking, linting and build. If any of them fails, then we should fix them before proceeding.
4. Make sure the new branch is pushed, and check the results/checks in CI/GitHub workflow. If the job fails in CI, then we go back to step 3 and try again.
   - If we can't fix the errors within a reasonable amount of effort, then leave it to the user to resolve it manually. Leave a comment in the pull request explaining this and then abort the current workflow.
5. Log agent merges.

## 2. Processing open pull requests where any checks failed:

1. We should process open pull requests where any checks have failed one by one.
2. For each pull request with any failed checks (by renovatebot):
   1. Merge in the pull request.
   2. Install latest package versions (with e.g. `pnpm install`).
      - Make sure we are using the latest transitive dependencies in case there are merge conflicts.
   3. Run type checking, linting and build. If any of them fails, then we should fix them before proceeding.
   4. Push the fixes and see the results in CI/GitHub workflow. If the job fails in CI, then we go back to step 3 (for the individual pull request) and try again.
      - If the task is unresolvable (perhaps due to an open issue in the third-party dependency) then we should leave it to the user to resolve it manually. Leave a comment in the pull request explaining this and then abort the current workflow.
3. Log agent merges.

## 3. After processing all open pull requests:

1. After we have processed all open pull requests and checks are passing, then we can merge the new branch into the `main` branch.
