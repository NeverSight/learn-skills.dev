---
name: implement
description: "Implement a piece of work based on a spec or set of tickets. Use when asked to implement, or when an orchestrator delegates a ticket."
---

Implement the work described by the user in the spec or tickets.

Use /tdd where possible, at pre-agreed seams. With no one to agree them with, choose the seams yourself and name them in your report.

Run typechecking regularly (when the project has a typechecker), single test files regularly, and the full test suite once at the end.

Once done, review the work at the depth the delegating agent sets: none, one light pass of your own, or /code-review. With no delegating agent, use /code-review.

Before you report, stop everything you started: dev servers, preview and browser tabs, background commands and watchers. Name anything you leave running on purpose in your report, with the reason. In zsh, split a list with `${=VAR}` or an array, and run a formatter only on a file list you've checked isn't empty: with none, it waits on stdin forever.

Never run `rm -rf`: move what's no longer needed (a temporary folder, a throwaway script) into the gitignored `.scratch/` with `mv`.

Commit your work to the current branch, unless the agent that delegated the work to you commits it.
