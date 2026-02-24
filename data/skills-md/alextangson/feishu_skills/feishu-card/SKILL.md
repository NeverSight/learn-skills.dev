---
name: feishu-card
description: Build and send Feishu interactive message cards (buttons, selects, status indicators). Handles card callback events from WebSocket. Use when sending morning briefings, alerts, confirmations, or any message that benefits from user interaction via buttons instead of text replies.
---

# Feishu Interactive Card

Build, send, and handle callbacks for Feishu interactive message cards. Cards replace plain text messages for any communication that benefits from structured layout or user actions (buttons, selects).

## When to Use

- Morning briefings (confirm/adjust/add task buttons)
- Evening reviews (acknowledge/defer buttons)
- Alert notifications (auto-fix/ignore/escalate buttons)
- Skill test results (listen/retest/mark-stable buttons)
- Any yes/no or multi-choice confirmation
- Status updates that need acknowledgment

## Sending a Card

### API

```
POST /open-apis/im/v1/messages?receive_id_type=chat_id
```

```json
{
  "receive_id": "<chat_id>",
  "msg_type": "interactive",
  "content": "<card_json_string>"
}
```

**Critical**: The `content` field must be a **JSON string** (stringified JSON), not a raw object.

### Card Structure

```json
{
  "config": { "wide_screen_mode": true },
  "header": {
    "title": { "tag": "plain_text", "content": "Card Title" },
    "template": "blue"
  },
  "elements": [
    { "tag": "div", "text": { "tag": "lark_md", "content": "**Bold** and `code` supported" } },
    { "tag": "hr" },
    { "tag": "action", "actions": [
      { "tag": "button", "text": { "tag": "plain_text", "content": "Confirm" }, "type": "primary", "value": { "action": "confirm" } },
      { "tag": "button", "text": { "tag": "plain_text", "content": "Adjust" }, "type": "default", "value": { "action": "adjust" } }
    ]}
  ]
}
```

### Header Templates (Colors)

| Template | Color | Use For |
|----------|-------|---------|
| `blue` | Blue | Normal briefings, info |
| `green` | Green | Success, completed |
| `red` | Red | Alerts, failures |
| `orange` | Orange | Warnings, degraded |
| `purple` | Purple | Special, creative |
| `turquoise` | Teal | Skill/tech results |
| `grey` | Grey | Low priority, FYI |

### Supported Elements

| Element | Tag | Purpose |
|---------|-----|---------|
| Rich text | `div` + `lark_md` | Markdown-like content |
| Divider | `hr` | Visual separator |
| Action buttons | `action` + `button` | Clickable actions |
| Select menu | `action` + `select_static` | Dropdown selection |
| Note/footer | `note` | Small gray footer text |
| Column set | `column_set` | Multi-column layout |
| Image | `img` | Inline image |

### `lark_md` Syntax

Feishu's `lark_md` tag supports a subset of Markdown:
- `**bold**`, `*italic*`, `~~strikethrough~~`
- `[link text](url)`
- `<at id=ou_xxx>name</at>` for mentions
- Newlines: use `\n` within the string

## Card Templates

### Morning Briefing Card

See [references/card-morning-briefing.json](references/card-morning-briefing.json) for the full template.

Structure:
1. Header: date + greeting (template: blue)
2. Section 1: Anomalies (red text if any, green "No anomalies" if clear)
3. Section 2: Today's action queue (numbered list with priority tags)
4. Section 3: Action buttons (Confirm / Adjust / Add Task)
5. Footer: generation timestamp

### Alert Card

See [references/card-alert.json](references/card-alert.json) for the full template.

Structure:
1. Header: alert type + service name (template: red)
2. Body: What happened, impact assessment
3. Action buttons (Auto-fix / Ignore / Escalate)

### Skill Test Result Card

See [references/card-skill-test.json](references/card-skill-test.json) for the full template.

Structure:
1. Header: skill name + pass/fail (template: green/red)
2. Body: Test metrics, pass count, details
3. Action buttons (Retest / Mark Stable / Archive)

### Confirmation Card

Generic yes/no card. Use for any binary decision.

```json
{
  "header": { "title": { "tag": "plain_text", "content": "Confirmation Required" }, "template": "orange" },
  "elements": [
    { "tag": "div", "text": { "tag": "lark_md", "content": "**Question**: Description of what needs confirming" } },
    { "tag": "action", "actions": [
      { "tag": "button", "text": { "tag": "plain_text", "content": "Yes, proceed" }, "type": "primary", "value": { "action": "confirm", "context": "unique_id" } },
      { "tag": "button", "text": { "tag": "plain_text", "content": "No, cancel" }, "type": "danger", "value": { "action": "cancel", "context": "unique_id" } }
    ]}
  ]
}
```

## Handling Callbacks

> **STATUS (2026-02-10)**: WebSocket currently does NOT subscribe to `card.action.trigger` events. Buttons on cards are display-only for now. Use the **text fallback** approach below until card callback support is added.

### Current Approach: Text Fallback

Since card button clicks cannot be received yet:
1. Include clear text instructions in the card footer: "Reply '确认' to confirm, '调整' to adjust, '加任务' to add"
2. User replies with a text message → AI agent receives via `im.message.receive_v1` (works today)
3. Parse the text reply to determine the action

### Future: Full Card Callbacks (when `card.action.trigger` is supported)

When user clicks a button on a card, Feishu sends a callback event via WebSocket.

The callback arrives as a `card.action.trigger` event containing:
- `action.value`: The `value` object from the button definition
- `operator.open_id`: Who clicked
- `token`: For response verification

Callback processing:
1. Parse `action.value` to determine what was clicked
2. Execute the corresponding action (e.g., mark today-actions as confirmed)
3. **Update the original card** to reflect the new state (e.g., change button to "Confirmed" checkmark)
4. Optionally send a brief follow-up message

Use the `PATCH /open-apis/im/v1/messages/:message_id` API to update the card content after a button click.

## Best Practices

- **One primary action**: Each card should have one obvious primary button (type: `primary`) and secondary options
- **Value context**: Always include enough context in button `value` to reconstruct what the button is about (e.g., date, task_id)
- **Concise content**: Cards are for quick scanning. Keep text short. Use `lark_md` formatting for emphasis.
- **No walls of text**: If content is long, summarize in card and link to a Feishu doc for details
- **Template colors**: Match the header color to the sentiment (red=alert, green=success, blue=info)

## Dependencies

- Feishu IM API (POST messages with `msg_type: interactive`)
- WebSocket connection (receives `card.action.trigger` events)
- See `FEISHU_API_HANDBOOK.md` API #4 for interactive card details

## Integration Points

- `daily-briefing` skill: Sends briefing as card instead of plain text
- `ops-rhythm` skill: Evening review uses card format
- `n8n-ops` skill: Alerts sent as red cards
- `skill-lab` skill: Test results sent as cards
- `feishu-sync` skill: Triggers sync after card confirmation
