---
name: telegram-bot-ux
description: Design Telegram bot journeys, onboarding, menus, button hierarchy, semantic colors, confirmation, recovery and microcopy. Use to plan or improve chat interaction flows; combine with keyboards-ui for payload implementation and Mini App design for browser screens.
---

# Telegram bot experience design

Design around the user's task, chat context and existing product language. Read
[the guide](references/guide.md) for interaction choice, button roles and recovery;
[flow patterns](references/patterns.md) for concrete screens and wording. Use
[the review template](references/review-template.md) to assess an existing flow.

## Decisions that matter

- Select chat, inline mode or Mini App from the task. Do not move a small menu
  into a browser merely to obtain arbitrary colors.
- Use `primary` for the next important action, `success` for a positive commitment,
  `danger` for destructive consequences, and the default style for ordinary
  choices, Back and Cancel. These are design recommendations; the server allows
  multiple styled buttons. Color never replaces the action label.
- A request to delete differs from confirmed deletion. Bind any confirmation to
  the current object, sender and version; do not perform the action merely because
  a previous screen displayed a red button.
- Preserve a way to leave, recover or restart a flow. Stale, unauthorized, empty,
  loading and failed states need useful next actions, not just an error code.
- Keep durable operations and displayed outcomes consistent. A timeout may leave
  an operation's result unknown; reconcile its state before offering another commit.

Use [keyboards UI](../telegram-bot-keyboards-ui/SKILL.md) for actual button fields,
callback acknowledgements and SDK support. Use [accessibility](../telegram-bot-accessibility/SKILL.md)
for labels, localization and client testing; [payments](../telegram-bot-payments-stars/SKILL.md)
for checkout truth and fulfillment. Read [sources](references/sources.md) when
checking native UI support. Test the actual journey with representative Telegram
clients; no design document certifies their rendering.
