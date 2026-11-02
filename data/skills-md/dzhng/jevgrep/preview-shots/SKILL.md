---
name: preview-shots
description: Open image shots (screenshots, snapshot baselines, montages, renders) in ONE macOS Preview window so the user can eyeball them. Use when the user asks to open / show / pull up / review shots in Preview or Finder, or right after producing visual artifacts the user should look at before signing off.
---

# Preview Shots

Put the review-worthy images in front of the user in a single Preview window they can flip through.

## Workflow

1. **Curate the set** — the images that answer "is this right?": the just-changed or just-blessed baselines, the integrated result, and the reference image when there's something to compare against. Don't dump every PNG in the folder; pick the smallest set that lets the user judge the change. If the user named specific shots, open exactly those.
2. **One window** — open them with a single `open -a Preview <path> <path> ...` call. One `open` invocation lands all the files in one window with a thumbnail sidebar; separate calls spawn separate windows.
3. **Caption them** — list one line per shot (what it is) so the user knows what they're flipping through.

## Rules

- macOS only (`open`); pass absolute or repo-root-relative paths.
- Order the files most-important-first; the first one is what Preview shows on open.
- Review saved PNG/GIF artifacts, not live Chrome. Exact regression capture
  should run headless by default; only open Chrome when the user explicitly asks
  for a live browser or when reproducing a headful-only bug.
- **One set at a time — never pile up windows.** Before opening a new set, close
  any open ones: `osascript -e 'tell application "Preview" to close every window'`.
- **Close on unattended proceed.** When you opened shots for a non-blocking review
  and then move on without the user's response, close Preview afterward:
  `osascript -e 'quit app "Preview"'`. An overnight autonomous run must never wake
  the user to a wall of Preview windows — at most one set open, and none once
  you've proceeded past the checkpoint.
