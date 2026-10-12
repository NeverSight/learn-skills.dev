---
name: pr-flow-diagram
description: Render a PR's control flow as an interactive lane diagram. Use when asked to diagram, visualise, or produce a flow lens for a pull request or branch diff.
---

# PR flow diagram

Turn a PR diff into a flow document and render it with this skill's
renderer under `scripts/`. Read `references/flow-doc.md` for the schema;
this file is just the workflow. Paths below are relative to this skill's
directory (the one holding this file). The scripts need only Node 20+; the
workflow uses the GitHub CLI (`gh`).

## Steps

1. **Read the PR.** `gh pr view <number> --json number,title,headRefOid,url`
   for the header fields, then `gh pr diff <number>` (and the changed-file list
   via `gh pr view <number> --json files`) to understand the change.
2. **Decide the flows before writing any JSON.** List every distinct entry
   point the diff touches -- the things that kick a path off: a request, a
   mutation, a job pickup, a webhook, a subscription, a migration. Each one
   is its own flow; the page's picker switches between them. Getting this
   wrong is the usual failure, in both directions:
   - Two paths that start at different steps are two flows even when they
     share most of their files. A read served from cache and the write that
     invalidates it are the canonical pair -- one flow with both origins
     jammed in reads as a forked mess, and the reviewer can't tell which
     half they're looking at.
   - A single path that fans out mid-way (a branch, a retry, an error
     route) is still one flow -- `next` labels carry the branch.
   Two or three flows is typical for a real PR. One flow is correct only
   when the change genuinely has one entry point; say so in its summary
   rather than padding the document.
3. **Author the flow JSON.** Top level
   `{schema: 1, pr: {number, title, headSha, repo}, flows: [...]}` with
   `headSha` = `headRefOid` and `repo` = the `owner/name` from the PR's
   `url`, which turns each step's file into a link at the PR's head.
   Judgement calls:
   - `summary` is the one sentence a reviewer reads when they pick the flow:
     say what the path proves or where it goes wrong, not what it contains.
     With several flows, make each summary say how that path differs from
     the others.
   - Lanes are the places code runs (Browser / API / Postgres / worker), in
     call order.
   - Steps reference real files from the diff (repo-relative `file`, plus
     `fn` when one function carries the step). A step with no `file` is
     infrastructure (a queue, a poll loop).
   - `inStack: true` on steps this PR adds or changes; leave it off
     pre-existing code the flow merely passes through.
   - `concern` marks where the reviewer should slow down; reuse the same
     string across related steps so they share a colour.
   - `added`/`deleted` from the diff hunks when they help signal weight.
4. **Build the page.**

   ```
   node scripts/build.mjs <doc.flow.json> <tmp>/flow-pr-<n>.html --check-files .
   ```

   That writes one self-contained HTML file; hand back its path and offer
   to open it. If you have an Artifact tool that publishes HTML pages, add
   `--artifact` and publish the file instead, with a 🧭 favicon and a title
   naming the PR (`PR <n> Flow Lens`). `--artifact` drops the document
   skeleton the tool supplies itself, and the published URL is the better
   deliverable: it opens in a browser instead of being downloaded.

   The build prints the flow count -- check it against the entry points you
   listed in step 2. Fix any validation errors (they're line items).
   `--check-files` warnings are advisory; expect them when the local
   checkout isn't on the PR's head.
5. **Offer the Mermaid version when it belongs in a conversation.**
   `node scripts/mermaid.mjs <doc.flow.json>`
   prints the same flows as Mermaid, which GitHub renders inline in a PR
   comment or issue, and which pastes into chat. It is an overview -- no side
   panel, no source links, no concern colours -- so it complements the
   page rather than replacing it. Post it with
   `gh pr comment <n> --body-file <file>` when the flows belong on the PR
   itself.

Write the JSON and HTML to a temp directory unless the user wants them
committed.
