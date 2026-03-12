---
name: things-reminders-manager
description: Manage Things reminders and todo create/update requests with a deterministic MCP workflow that prevents duplicate tasks and date mistakes. Use when users ask to add, reschedule, or correct Things reminders, especially with relative dates or potential update-vs-create ambiguity.
---

# Things Reminders Manager

Use an update-first workflow for Things reminder requests.

## Inputs

- Reminder intent:
  - create
  - reschedule
  - correct an existing task
- Scheduling phrase or absolute date/time
- Optional timezone override
- Effective settings may come from:
  - explicit user override
  - `config/customization.yaml`
  - `config/customization.template.yaml`
  - workflow defaults
- Workflow settings:
  - `timezone`
  - `defaultReminderTime`
  - `duplicatePolicy`
  - `onUpdateWithoutToken`
  - `requireAbsoluteDateInConfirmation`

## Workflow

1. Resolve the current local date/time.
   - Run `date '+%Y-%m-%d %H:%M:%S %Z %z'`.
2. Load effective settings from override, config, then defaults.
   - Use `timezone` for schedule normalization.
   - Use `defaultReminderTime` when the user gives a date without a time and the workflow needs a default time.
3. Check Things MCP readiness and auth.
   - `things_capabilities`
   - `things_auth_get_status`
   - `things_validate_token_config` before any likely update path
4. Normalize the requested schedule into an absolute date/time using the effective `timezone`.
5. Search candidate open tasks before creating anything new.
   - Prefer `things_find_todos`
   - Fall back to `things_read_todos` when needed
6. Apply `duplicatePolicy`.
   - `update-first`: update on a single clear correction/reschedule match, otherwise create or disambiguate
   - `ask-first`: stop when a plausible duplicate exists and ask the user to choose
   - `always-create`: skip update matching and create a new task unless the user explicitly asked to modify an existing one
7. Apply `onUpdateWithoutToken` if the chosen path requires an update and token access is unavailable.
   - `block-and-report`: stop with `action=blocked`
   - `ask-to-create-duplicate`: ask whether to create a new task instead
8. Execute the selected create or update path.
   - create: `things_add_todo`
   - update: `things_update_todo`
9. Confirm the result using `requireAbsoluteDateInConfirmation`.
   - When `true`, confirm in absolute form with timezone.

## Output Contract

- Return:
  - `action`: `created`, `updated`, or `blocked`
  - task title
  - normalized absolute schedule
  - blockers, when present
- Confirm dates in absolute form with timezone in user-visible output.

## Guardrails

- Never assume relative dates without resolving the current local date.
- Never silently create a duplicate when update intent is clear.
- Never claim mutation success without tool confirmation.
- If an update requires token access and token access is missing, block and report the exact blocker.

## References

- `references/customization.md`
- `references/mcp-sequence.md`
- `references/config-schema.md`
- `references/automation-prompts.md`
