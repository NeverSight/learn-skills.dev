---
name: qa-checklist
description: Read the diff for a change and produce a short, manual QA checklist to run against the deployed app — only the behaviour this change actually touched, written as plain-English steps a person can click through. Use when the user asks for a "QA checklist", "manual test plan", "what should I test", "smoke test steps", or how to verify a change by hand after deploy.
---

# Manual QA checklist from a diff

Produce a short checklist a human can click through in the **deployed app** to confirm
this change works. The reader is a person with a browser and a test account — not a
developer reading code. Every step must be something they can do and observe through
the UI (or, rarely, an email inbox / API client if the change only surfaces there).

This is not a regression suite and not a code review. Cover only what **this diff
changed**, plus the one or two adjacent flows most likely to break as a side effect.
If the checklist grows past ~10 steps, it's too broad — cut it back to what the change
actually touched.

## 1. Get the diff

Default to comparing the current branch against `main`; respect any base, commit range,
or PR the user names instead.

```
git fetch origin
git diff origin/main...HEAD --stat     # overview
git diff origin/main...HEAD            # read the whole diff
```

Use `...` (merge-base) so you see only what this branch adds. Where the diff alone is
ambiguous, open the touched files — you need to understand the user-visible behaviour,
not just the lines that moved.

## 2. Translate code changes into user-visible behaviour

For each change, ask: **"what would a user see or do differently because of this?"**
That question decides what goes on the checklist.

- **Controllers / routes / pages** — the pages and actions to exercise. New route → visit
  it; changed store/update logic → submit the form and check the result.
- **Validation & authorization** — the *failure* paths are QA steps too: submit the
  invalid input and confirm the inline error; try the action as a user who shouldn't be
  allowed and confirm it's blocked.
- **Frontend components** — the interactions to click: toggles, modals, optimistic
  updates, empty states, flash messages.
- **Feature flags** — if behaviour is gated (e.g. Pennant), include checking both sides:
  flag on shows the feature, flag off hides it cleanly. Say how to identify a flagged
  account if the diff makes that clear.
- **Emails / notifications / jobs** — trigger the action, then check the observable
  result (email arrives, notification appears). Skip anything with no observable surface.
- **Migrations / data changes** — only if they change what users see (e.g. a renamed
  field on a page). Running migrations belongs in a deploy checklist, not here.

Skip entirely: refactors with no behaviour change, test-only changes, CI/tooling, code
style. If the whole diff is like that, say so — "nothing to QA manually" is a valid
answer.

## 3. Write the checklist

Output a single markdown checklist. Rules:

- **Plain English, imperative steps** — "Open a feedback item and click the 👍 reaction",
  not "Verify ReactionController@store persists the reaction". Never reference class
  names, routes-as-code, or files.
- **Each step pairs an action with the expected result**: *do X — you should see Y.*
- **Order steps as a walkthrough**, so a person can do them top to bottom in one session
  without backtracking (set up state first, then exercise it, then check side effects).
- **Note required preconditions up front** in one line if any exist: a second test
  account, a feature flag enabled, an existing record to act on.
- Keep it to roughly **5–10 checkboxes**. One step per behaviour, not per code path.

Format:

```markdown
## QA checklist — <one-line summary of the change>

**Before you start:** <preconditions, or omit this line>

- [ ] <action> — <expected result>
- [ ] ...
```

End with nothing else — no summary of the diff, no code commentary.
