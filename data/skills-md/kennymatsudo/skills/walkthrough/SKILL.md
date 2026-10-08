---
name: walkthrough
description: >-
  Walk a reader through a teammate's pull request so they understand what
  changed and why, one layer at a time: a short headline with a reading order
  first, then each part of the change before and after, then the code paths,
  with every claim cited and checked. Read-only; never reviews for bugs or
  posts to the PR. Use for "walk me through PR #123", "what did this PR
  change", "help me understand this PR", "explain this branch's changes".
  Use how for how existing code works, and review-pr for finding problems.
---

# Walkthrough

You own a reader's understanding of someone else's change. They should be able to read the first answer in under a minute and trust every line of it.

## Layers

| Layer | Covers |
|---|---|
| 1. Headline (default) | Why the PR exists, what it changes, and the order to read it in |
| 2. Parts | Each item from the reading order, before and after |
| 3. Code | Each changed path, method by method |

Answer at layer 1. "More" or "yes" means one layer down on every reading-order item; "more on X" means one layer down, on X only. For how unchanged code around the PR works, load the how skill; for the history behind code the PR didn't write, load the why skill.

## 1. Find the change

Accept a PR number or link, or a branch. With none given, use the current branch's PR.

- **A PR:** `gh pr view <pr> --json number,title,body,url,author,baseRefName,baseRefOid,headRefOid,commits,closingIssuesReferences,comments,reviews`. Fetch its head with `git fetch origin pull/<number>/head`. The base is `git merge-base <baseRefOid> <headRefOid>`, so the diff shows only the author's changes.
- **A branch with no PR:** the base is the merge base with the default branch (`git symbolic-ref --short refs/remotes/origin/HEAD`, else `origin/main`). There is no description, so the why comes from commits and tickets.

Read code at a ref with `git show <ref>:<path>` and search it with `git grep <pattern> <ref>`, so the checked-out branch never matters.

Done when you have the base and head commit hashes, the title and description, and the commit list, or have told the user what failed.

## 2. Gather the why

The why is where generated summaries go wrong most often, so take it from a source and quote or attribute it:

- The PR description, the author's own comments on the PR, and commit messages.
- Linked tickets: IDs in the title, branch, description, or commits, plus `closingIssuesReferences`. List the session's tools and look each ID up with any tool that can search a ticket tracker. Report a tracker with no matching tool as unsearched.

If no source says why, the headline says "The PR doesn't say why" and gives the closest thing it does say. Never supply a reason from the diff alone.

Done when the why is quoted with its source, or marked missing.

## 3. Sort the files

Run `python3 scripts/sort_files.py <repo-root> <base> <head>` from this skill's directory. It tags each file `renamed`, `whitespace`, `moved`, `generated`, `test`, `docs`, or `core`.

- **Mechanical** (`renamed`, `whitespace`, `moved`, `generated`): spot-check one hunk of each `moved` file to confirm it was a move. These go in one line at the end, not the reading order. Note whether tests changed alongside them; untouched passing tests back a "no behavior change" claim.
- **Reading order:** group the rest into 2 to 6 items by what they do, not by file. Put first the item the title and description are about, then what it depends on or what calls it, then tests, then docs. Tests and docs that only support one item fold into it.
- **Behavior changes:** list every change a caller or user would notice: inputs accepted, outputs and errors returned, defaults, and where a value comes from. Each goes in its reading-order item. One the description, commits, and tickets never mention goes under "Not mentioned by the author", so the reader sees the PR's whole effect.

With more than about 15 core files, spawn one read-only subagent on a mid-tier model per group, asking for the group's before and after in two sentences with `path:line` citations, and check what returns against the code.

Done when every changed file is mechanical or in an item, and every behavior change on your list is placed in an item or the unmentioned line.

## 4. Write

Write for a teammate who knows the language but not this part of the codebase.

- **Plain words.** One idea per sentence, 15 to 20 words. Swap jargon for a plain word instead of defining it. Keep the code's own names in backticks, because the reader uses them to find their place in the diff.
- **Before and after.** Describe each change as what happened before and what happens now, in terms of behavior.
- **Describe, never grade.** No "clean", "safe", "nice refactor", or "looks correct". State a change's effect as a fact and leave the judgment to the reader.
- **Cite.** Every claim about the code gets `path:LINE` or `path:START-END` from the repo root, at the head. Code the PR removed or rewrote gets `before:path:LINE`, at the base. A claim you can't cite is marked `(inferred)` with what it rests on.

**Layer 1 format**, aiming for under 250 words, not counting citations. Completeness beats the count: never cut the why, a reading-order item, or an unmentioned behavior change to fit. When over, tighten the wording instead. Start at "What and why" with nothing before it, and end at the closing line with nothing after it:

- **What and why:** three or four sentences. What the touched code does, for a reader new to it. The problem in the author's words. Then what the PR does about it.
- **Reading order:** numbered, one line per item: what it does, then its main citation.
- **Mechanical:** one line naming the renames, moves, and generated files, and whether tests changed with them.
- **Not mentioned by the author:** one line per behavior change no source mentions.
- Close with one question offering the next layer for the whole PR, and say in one line what it would add for this PR, such as "Want more detail? Next I'd go through each part before and after, who calls the changed code, and what the tests check."

**Layer 2 format**, for each item: Before, After, Who calls it (the callers of each changed function or setting, found with `git grep` at the head), and Tests (which tests cover it and what they assert).

**Layer 3 format**, for each path: a numbered call chain, one line per call: who calls what, with what, and why.

End layers 2 and 3 with the same kind of question for the next layer down. At layer 3, offer the how skill for the unchanged code around the path, or the why skill for its history.

Drop any section with nothing in it.

Done when every sentence about the code is cited or marked `(inferred)`.

## 5. Check citations

Save the draft and run `python3 scripts/check_citations.py <repo-root> <base> <head> <draft-file>` from this skill's directory. It confirms each cited line exists and counts the words. For each failure, fix the citation from the code, mark the claim `(inferred)`, or cut it.

The script can't tell whether a line supports its claim. Read each cited range with `git show <ref>:<path>` and confirm it shows what the sentence says; a signature cited for a validation rule fails. Fix or cut each mismatch, then rerun on the final text.

Done when the script prints `OK` on the text you will send, every cited range has been read against its claim, and a layer 1 answer is under 250 words or has nothing left to tighten.

**Reply:** the checked walkthrough at the requested layer, and nothing posted to the PR.
