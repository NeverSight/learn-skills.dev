---
name: apple-notes
description: Read, find, create, append or edit Apple Notes on macOS for the requesting project, with explicit account/folder targeting and item readback. Use for native Notes tasks, not general document editing.
---

Read [the project contract](../apple-apps/references/project-contract.md) before
automated writes or binding a new project. Keep targets and receipts project-owned.

1. Resolve the requested account/folder and, for an edit, the existing note ID.
   Titles and folder names may repeat. Confirm IDs and container ancestry rather
   than choosing the first match or relying on the default account. Reuse the
   project's adapter if one exists.
2. For a new caller, run the Notes probe in
   [apple-effects-reliability](../apple-effects-reliability/SKILL.md), then read
   the actual requested folder/item. Account-count success proves reachability,
   not target access or delivered content.
3. Use bounded AppleScript for supported operations, or native computer use for
   rich content, locked notes or an unsupported feature. Read
   [Notes scripting details](references/scripting.md) when using AppleScript.
   Create only the requested note in the confirmed folder; create a missing
   folder only when the request or project policy authorizes it.
4. For append/edit, read the current body first and preserve existing content,
   attachments and formatting outside the requested change. If a full-body
   replacement cannot preserve these, use the GUI for the requested edit.
5. Read the resulting note by provider ID and confirm its account/folder and
   requested text. For marked creates, also reconcile the operation marker.
   Save the project's receipt. On uncertain output, use the reliability skill
   before repeating the write.

Completion means the requested content is visible in the correct note/target
and the receipt records that check. A script exit code, provider ID or open
window alone is not delivery verification.
