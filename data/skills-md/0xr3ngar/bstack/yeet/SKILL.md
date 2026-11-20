---
name: yeet
description: Open a draft PR and work through the user's review comments. Once ready for review, explain feedback and wait for direction. Trigger on "yeet".
disable-model-invocation: true
license: MIT
compatibility: "Requires Git, an authenticated GitHub CLI, and repository push access. The PR diagram needs GitHub CLI 2.102 or newer for image attachments, headless Chrome or another browser screenshot tool, and internet access."
---

# Yeet

Push the current work, open a draft PR, and work through the user's comments until they are satisfied. When the user marks the PR ready for review, switch to explaining feedback and recommending what to address.

## Prepare the change

Inspect the branch, base, diff, and worktree. Include only work in scope and preserve unrelated changes. Use a feature branch when needed. Never force-push a shared default branch.

Run checks appropriate to the change and resolve failures it introduced. If GitHub access is missing, finish local preparation and report the specific access needed.

Use Conventional Commits with an imperative subject, `type(scope): summary`, without a trailing period. Follow configured commit signing, including when rewriting commits. Do not silently fall back to unsigned commits when signing fails.

After the subject, use Linux-style git trailers only. Add `Assisted-by: Vendor:model` for models known to have contributed; do not invent model identities. Preserve authorship and existing trailers when amending.

## Open the draft

Find the branch's existing PR before creating one. Open new PRs in draft and preserve an existing PR's status. The user decides when to mark it ready. Follow an explicit request for a different status.

Match the title to the main commit subject. Then write the description as described below.

## Write the description

The description is short enough to read in ten seconds. It has these parts, in this order, with no headings:

1. One or two sentences that state the problem and what the PR changes.
2. A hand-drawn diagram of the change.
3. One or two sentences under the diagram that say what it shows.
4. For a change the user can see, before and after screenshots in a two-column table.

Leave out checklists, test plans, file lists and summaries of the diff. Mention a testing limit only when it changes the reviewer's decision. If the repository has a PR template with required sections, keep its sections and fill each one this briefly.

Write the title and the body in plain words and short sentences, in the active voice. Cut filler, chatbot phrases and metaphors.

### Draw the diagram

Copy the [diagram template](assets/diagram.html) to a scratch folder outside the repository. Set `WIDTH`, `HEIGHT` and `SHAPES` for this change; the template lists the shape kinds. Draw what changed: the flow, the structure, or before and now. Keep it to about ten shapes.

Put only short labels in the drawing, never sentences, because small handwriting is hard to read on GitHub. Show text examples, such as old and new messages, in a Markdown table in the body.

Take a screenshot in a window of `WIDTH` by `HEIGHT`. With Chrome:

```bash
"<chrome>" --headless=new --hide-scrollbars --force-device-scale-factor=2 \
  --window-size=<WIDTH>,<HEIGHT> --virtual-time-budget=5000 \
  --screenshot=<scratch>/diagram.png "file://<scratch>/diagram.html"
```

Look at the image. Fix text that leaves its box and shapes that overlap, then take it again.

### Attach the images

Reference each image in the body by its local path, then upload it in the same command. GitHub CLI replaces the path with the uploaded address:

```bash
gh pr edit <number> --body-file <scratch>/body.md \
  --attach "<scratch>/diagram.png#What the diagram shows"
```

In `body.md`, write a Markdown image whose address is the local path of the file, here `<scratch>/diagram.png`. Do not commit images to the repository or to a separate branch.

When the scope of the PR changes, update the sentences, draw the diagram again and replace the image. If no screenshot tool is available, open the PR without the diagram and tell the user that it is missing.

## Report the draft

Tell the user the draft is open and ready for their comments. Include the link and current check status, then begin watching for feedback. This notification does not mark the PR ready on GitHub.

## While the PR is a draft

Identify the requesting user's review account from established context. If it is unknown, ask for the account while completing the draft. Do not assume the PR author, authenticated account, or any collaborator is that person. Accept feedback from another review tool only when its source is attributable to the user.

Watch PR conversation comments, submitted reviews, and inline threads, including replies and edits. Act on the user's feedback within the task's scope without asking them to repeat it in chat. Explain comments from other people or bots and recommend whether to address them; wait for the user's direction before acting on those comments.

Read the full thread and inspect the code before changing it. Fix the issue, run affected checks, and push the change. Give the user a verdict and a draft reply. Explain any disputed finding or blocked fix. Post or resolve only when the user asks for that action.

Tell the user what changed and keep watching for their next comments. Repeat until they mark the PR ready, close it, or ask you to stop.

## Once the PR is ready for review

Explain new feedback to the user in plain language. State what the reviewer means, whether the code supports the finding, and whether you recommend fixing it now, deferring it, or leaving the code as it is.

Wait for the user's decision before editing, pushing a review fix, replying, or resolving a thread. This applies to all reviewers, including the requesting user. Follow an explicit instruction to handle a particular finding, then verify and report the result.

## Keep the loop accurate

Inspect the host's available PR event subscriptions, listeners, and wake tools first. Use an existing subscription or register one for this PR through the supported mechanism, then confirm it is active. Prefer event delivery to a polling loop. Subscribe to comments, reviews, and PR state changes where supported; fetch the current PR and thread when an event arrives.

Poll only for events the host cannot deliver, with bounded waits while the session runs. Track the PR, comment IDs and edits, and the last processed state so reconnecting does not repeat completed work. Fetch feedback received while you were fixing the previous batch.

Recheck the PR's draft status before starting a fix and before pushing or resolving threads. If it became ready, pause pending review changes and present them for the user's decision. If it returns to draft, resume the draft workflow. Stop on merge or closure, or when the user asks.

Report CI failures. Fix failures caused by your draft changes and recheck the final commit. After the PR is ready, explain failures and recommend a fix before proceeding unless the user already authorized that work.

Check the available tools and subscription status before declaring automatic listening unavailable. If neither event delivery nor continued polling is possible, explain the specific limitation and how to resume. Report a listener as active only after confirming it. On an access failure, preserve your place and report the blocker instead of silently abandoning the loop.

Marking a PR ready does not authorize merging it. Merge only when explicitly authorized and the repository's requirements are satisfied.
