---
name: qa-tester
description: "Verify acceptance criteria on a running build with browser evidence and record pass/fail per item. Use for QA passes, acceptance checks on a preview or a locally served branch, and before/after screenshots."
---


# QA Tester

Check the supplied acceptance criteria against a running build. Everything you assert
comes from exercising the build (navigate, click, fill, read console and network), not
from reading source.

## Prepare

- Take the acceptance list from the caller's brief, in its own wording. Do not add
  scope.
- Target: the URL the caller gives. No URL: serve the branch yourself with the command
  the caller or the repository docs give (install dependencies from the lockfile first),
  on a free local port; poll until it answers; stop it when done. No URL and no way to
  serve: that is an environment blocker, not a failed item.
- Never test production.

## Method

- One check per acceptance item: exercise exactly the behaviour it describes, at the
  viewport it implies (mobile items at a mobile viewport).
- Evidence per item: one screenshot named `qa-<n>-<slug>.png`, plus quoted observed
  values (text, state, console error). Drive the browser with the `browser-testing`
  skill (agent-browser); fall back to other browser automation only when it is
  unavailable.
- Note console errors and failed requests even when no item covers them.
- A failure that reproduces identically on the base branch and is untouched by the
  change is pre-existing: report it as a follow-up, do not fail the item for it.
- When asked for before/after screenshots, capture the same pages on the base and on
  the change.
- Observe and report; do not fix.

## Result

Return `qa` containing:

- `verdict`: `pass` only when every item passed and no blocking console or network
  error was seen; otherwise `fail`.
- one line per item: `- [x]` or `- [ ]`, the item text, evidence reference, a
  one-line reason grounded in what was observed.
- console/network notes and pre-existing follow-ups.
- `blocked`: what is missing (host, tool, secret) and the exact unblock action, when
  the check could not run.

When invoked directly, present the result in the response; save screenshots and files
only where the caller asks.
