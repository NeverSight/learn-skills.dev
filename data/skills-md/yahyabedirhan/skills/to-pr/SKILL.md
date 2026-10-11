---
name: to-pr
description: Open a pull request or rewrite its description, with a one-sentence why, reviewer notes, and a visual change outline. Use whenever a pull request is opened or its description changes.
---

# Describe a Pull Request

Create or update the pull request for the current task with a concise description that helps a reviewer understand why the change exists and the shape of the implementation.

## Workflow

1. Read the description template:

   `Read({SKILLBASE}/references/pr_description_template.md)`

2. Identify or create the pull request:
   - Check the current branch for a PR with `gh pr view --json url,number,title,state,baseRefName,headRefName 2>/dev/null`.
   - If no PR exists, inspect `git status --short --branch` and the commits on the current branch.
   - Commit task-related changes when needed, push the branch with an upstream, and create a PR for it. Follow the repository's git safety protocol.
   - Ask the user to select a PR only when the current branch has no relevant work and there is no safe current-branch PR to create.

3. Gather only the context needed to explain the change:
   - Read the ticket and any relevant task artifacts.
   - Read the complete PR diff and enough surrounding code to understand behavior and ownership.
   - Use `gh pr view` to collect PR metadata and changed files.
   - Read `{SKILLBASE}/references/show-me.md` for the visual-outline conventions used in the PR body.

4. Write the PR description using the template:
   - Keep **Why the change** to exactly one sentence.
   - Keep **Special things to note** to 1-3 bullets. Prioritize reviewer warnings, migrations, compatibility constraints, deliberate omissions, or surprising decisions. Write `- None.` when there are no special considerations.
   - Make **Change outline** a compact, `/show-me`-inspired structural view rather than prose or a file-by-file changelog.
   - Include only the views that help explain this PR:
     - SQL table and endpoint contract changes, plus pseudocode for business logic.
     - key data structure / type changes
     - A shallow file tree showing changed responsibilities.
     - React component tree changes, including important hooks, state, and package boundaries.
     - Call-tree, call-stack, control-flow, or data-flow changes.
   - Prefer `diff` blocks when showing changes to an existing shape. Show the complete target shape when most of it is new or diff notation would obscure ownership or order.
   - Keep each view focused on what a reviewer needs. Omit categories that did not change.
   - End with **Things to be aware of**, the last section, for what lies outside "what changed": decisions you made alone, surprises, what's not in the PR, and follow-ups, each marked as a ticket, a todo for the maintainer, or nothing needed. Keep its four lines, writing `None.` after an empty one, so the reader knows it was considered. **Special things to note** stays about the change itself.
   - Link a ticket the PR finishes with `Closes #n`, but a ticket still waiting for the maintainer to try it (QA) with `Refs #n`, so the merge doesn't close it first.
   - optionaL: if you are aware of a ticket id/url, or related plan/document urls, or other relevant links, include them in the header, otherwise omit the header

5. Save and publish the description:
   - Save it to `.scratch/pr-{number}/description.md`: `.scratch/` is gitignored, and GitHub holds the published description, so saving or rewriting it leaves nothing to commit.
   - Update the PR with `gh pr edit {number} --body-file {output-path}`.
   - Confirm the update succeeded.

6. Report completion:
   - Read `{SKILLBASE}/references/describe_pr_final_answer.md`.
   - Respond using that final answer template with the PR URL, the saved description path, and a concise list of changed files.
   - Give each changed file two review links, built from the PR's head commit as it stands after your push (`gh pr view {number} --json url,headRefOid,files`), so an updated PR links its new head. Take `{owner}/{repo}` from the PR `url`:
     - **Final version:** `https://github.com/{owner}/{repo}/blob/{headRefOid}/{path}`, where GitHub renders Markdown.
     - **Diff:** `{pr_url}/files#diff-{hash}`, where `{hash}` is the SHA-256 of the path (`printf %s '{path}' | shasum -a 256`, or `sha256sum` on Linux).
   - When many files changed, link the key ones and list the rest by path.

Always read and follow `{SKILLBASE}/references/pr_description_template.md`. Do not expand the PR body beyond that template.

Write as one human talking to another: avoid jargon and slang, and use simple, coherent, concise language.

Name an issue or pull request by its title, never by its number alone: `#12 Add login`, not `#12`. This holds in the title, the body and anything you tell the user.
