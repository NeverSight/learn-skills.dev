---
name: apple-apps
description: Set up reusable macOS app automation for a project, or choose between native app scripting and computer use. Use for cross-project Apple app access and workflow setup; use apple-notes or apple-reminders for individual tasks.
---

Use this skill when a project needs the Mac's app access. Notes and Reminders
have app-specific procedures; other apps use the available computer-use tool
and its current documentation until a tested app adapter exists.

1. Read [the project contract](references/project-contract.md). Bind the request
   to this Mac/user, the actual caller, the project's target and its receipt path.
   Native Notes/Reminders access does not require a shared API secret. Reference
   a project's existing credential location only when its chosen route needs one.
2. Choose the app procedure:
   - Notes: read [apple-notes](../apple-notes/SKILL.md).
   - Reminders: read [apple-reminders](../apple-reminders/SKILL.md).
   - Timeout, denied access or uncertain delivery: read
     [apple-effects-reliability](../apple-effects-reliability/SKILL.md).
   - Another app or a feature outside the scripting dictionary: use native
     computer use, with fresh accessibility state before each action. This is
     a tool route, not a claim that another app has a tested delivery adapter.
3. Prefer the project's existing transport. For a new binding, start with a
   bounded read in the intended caller context. Resolve the requested target
   before a write. Use GUI inspection for visible prompts and unsupported
   features; consult the actual CUA/Peekaboo route and permissions.
4. Finish with the requested item's readback and the project's saved receipt.
   Report access, mutation and delivery separately. A healthy app probe alone
   closes only the access check.

## Reuse

These four sibling skill folders are a portable bundle: apple-apps, apple-notes,
apple-reminders and apple-effects-reliability. On this Mac, installed skills can
be invoked from another project's session; they do not need a Penny import.
For another Mac or agent harness, copy the four complete folders into that
harness's discovered skill directory, preserving relative paths and inspecting
existing destinations before replacement. Copy skills, not tokens or receipts.
Recheck app/account availability and caller permissions on the destination.

Example: `Use $apple-reminders for project atlas to create the requested task
in the configured list, with operation ID atlas-task-123 and a local receipt.`
This is a binding example, not authorization to create that item now.
