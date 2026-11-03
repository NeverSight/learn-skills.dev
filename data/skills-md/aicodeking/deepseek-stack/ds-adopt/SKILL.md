---
name: ds-adopt
description: "Takes over an existing PR, branch or agent thread and finishes its original goal while keeping credit for the first contributors. Use when the user says take over, adopt, pick up or finish this PR, or /ds-adopt."
---

Finish someone else's work as if it were yours, but credit them for what they did.

## Steps

1. Read the source PR, branch or thread in full: description, commits, review comments and any later corrections from the user.
2. Find the real current state: the head SHA, uncommitted changes and open review findings. Treat the handoff notes as hints, not facts.
3. Write down the original goal in one sentence.
4. Choose where to work. By default, make a new branch with the original commits on it and add your fixes as separate commits. Continue in place or stack only if the user asked for it.
5. Run `ds-revive` to bring the work up to date with the base branch.
6. Fix what is needed to reach the original goal. Simplify where you can, but keep every intended behavior.
7. Verify on your own. Reproduce the original problem, then show it fixed. Run the real workflow, not only mocked tests. Record the commands and output.
8. Check the source PR again. It may have changed while you worked.
9. If a PR is wanted, file it with `ds-pr`, then watch it with `ds-watch-pr`. Use `ds-pr-comments` for any reply.
10. Report what you inherited, what you changed, how you verified it, how credit was kept and what is still open.

## Stop when

- The goal is reached, verified and reported.
- The goal is unclear, or finishing it needs a product decision. Ask the user.
- Verification fails three times in a row on the same issue. Report the blocker.

## Rules

- Keep the original Git authors and co-author trailers. Name the contributors and link the original PR in the description.
- If the PR will be squashed, keep human co-author lines in the squash message. Use verified identities only, never guessed emails.
- Do not defend the old code because it exists. Do not add unrelated features.
- Do not edit, merge or close the original PR without permission.
- State plainly what you could not verify.
