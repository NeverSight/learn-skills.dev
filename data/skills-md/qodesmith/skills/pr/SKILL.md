---
name: pr
description: Use when the user asks to put up, open, or raise a pull request. Creates it with the gh CLI and writes a description a human can read in one pass.
---

# Put up a pull request

Create the pull request with `gh pr create`.
Push the branch first if it has no remote.

Write the description for a human who has not seen the work.
Say what changed and why it changed.
Keep it short: no unnecessary verbiage, and no rambling.

Leave out the things the diff already says.
A file list, a restatement of every commit message, and a summary of your own process all cost the reader attention and give nothing back.

If the change is hard to review in one pass, say where to start reading.
That is worth more than any amount of summary.
