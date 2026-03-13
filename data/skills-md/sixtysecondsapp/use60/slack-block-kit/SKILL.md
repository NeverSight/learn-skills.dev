---
name: Slack Block Kit
description: |
  Build rich, interactive Slack messages using Block Kit for sales workflows.
  Covers meeting briefings, coaching digests, deal alerts, pipeline summaries,
  HITL approvals, and all notification types. Uses our typed builder functions
  from slackBlocks.ts with auto-truncation safety. Handles the full message
  lifecycle: compose blocks, deliver via send-slack-message, handle interactions.
  Use when building any Slack notification, alert, digest, or interactive message.
  Do NOT use for email content or in-app UI components.
metadata:
  author: sixty-ai
  version: "2"
  category: sales-ai
  skill_type: atomic
  is_active: true
  agent_affinity:
    - crm_ops
  triggers:
    - pattern: "slack message"
      intent: "build_slack_message"
      confidence: 0.90
      examples:
        - "send a slack message with meeting prep"
        - "build a slack notification for this deal"
    - pattern: "block kit"
      intent: "slack_block_kit"
      confidence: 0.92
      examples:
        - "create block kit message"
        - "format this as slack blocks"
    - pattern: "slack notification"
      intent: "slack_notification"
      confidence: 0.88
      examples:
        - "notify the team on slack"
        - "send a slack alert"
  keywords:
    - "slack"
    - "block kit"
    - "notification"
    - "blocks"
    - "slack message"
    - "digest"
    - "alert"
  required_context:
    - org_id
  inputs:
    - name: message_type
      type: string
      description: "Type: meeting_briefing, coaching_digest, deal_won, deal_lost, daily_digest, hitl_approval, etc."
      required: true
    - name: data
      type: object
      description: "Message-specific data matching the corresponding Data interface"
      required: true
  outputs:
    - name: blocks
      type: array
      description: "Slack Block Kit blocks array"
    - name: text
      type: string
      description: "Plaintext fallback for notifications and screen readers"
  requires_capabilities:
    - slack
  priority: medium
  tags:
    - slack
    - notifications
    - block-kit
    - integrations
---

## Available Context
@_platform-references/org-variables.md

# Slack Block Kit for Sales Workflows

Build rich, interactive Slack messages using our typed Block Kit abstraction layer. Every sales notification, coaching digest, deal alert, and approval request flows through this system.

## Architecture

```
Adapter/Skill → build{Type}Message(data) → SlackMessage { blocks, text }
                         ↓
              send-slack-message edge function
                         ↓
              Slack Web API (chat.postMessage)
                         ↓
              slack-interactive (button clicks)
```

**Key file**: `supabase/functions/_shared/slackBlocks.ts` (3000+ lines, 33+ builders)
**Delivery**: `supabase/functions/send-slack-message/index.ts`
**Interactions**: `supabase/functions/slack-interactive/`

## Primitive Block Builders

All builders auto-truncate to Slack limits. See `references/block-types-and-limits.md` for full constraints.

| Function | Purpose | Auto-truncation |
|----------|---------|-----------------|
| `header(text)` | Title/alert | 150 chars |
| `section(text)` | Markdown content | 2800 chars |
| `sectionWithFields(fields)` | Key-value grid (2-col) | 10 fields max |
| `sectionWithButton(text, btn, actionId, value, style?)` | Section + accessory button | |
| `sectionWithImage(text, url, alt)` | Section + image | |
| `context(elements)` | Metadata/footer | 10 elements, 1900 chars |
| `actions(buttons)` | Action buttons | 5 max (recommend 3) |
| `divider()` | Horizontal rule | |

## Message Builders (33+ types)

Each builder takes a typed `Data` interface and returns `SlackMessage { blocks, text }`.

### Core Sales Messages

| Builder | Interface | Use Case |
|---------|-----------|----------|
| `buildMeetingPrepMessage` | `MeetingPrepData` | Pre-meeting briefing with attendees, deal, talking points, risks |
| `buildMeetingDebriefMessage` | `MeetingDebriefData` | Post-call summary with sentiment, talk time, action items |
| `buildDailyDigestMessage` | `DailyDigestData` | Morning standup with meetings, tasks, insights |
| `buildCoachingMicroFeedbackMessage` | `CoachingMicroFeedbackData` | Per-meeting coaching: scores, insights, recommendations |
| `buildWeeklyCoachingDigestMessage` | `WeeklyCoachingDigestData` | Weekly coaching: trends, patterns, challenge |

### Deal Lifecycle

| Builder | Interface | Use Case |
|---------|-----------|----------|
| `buildDealRoomMessage` | `DealRoomData` | Deal room creation |
| `buildDealStageChangeMessage` | `DealStageChangeData` | Pipeline movement |
| `buildDealActivityMessage` | `DealActivityData` | Activity logged |
| `buildDealWonMessage` | `DealWonData` | Win celebration |
| `buildDealLostMessage` | `DealLostData` | Loss notification + lessons |
| `buildWinProbabilityChangeMessage` | `WinProbabilityChangeData` | AI health shift |
| `buildDealSnapshotMessage` | `DealSnapshotData` | Deal health card |
| `buildDealMomentumMessage` | `DealMomentumData` | Velocity/momentum trends |

### HITL (Human-in-the-Loop)

| Builder | Interface | Use Case |
|---------|-----------|----------|
| `buildHITLApprovalMessage` | `HITLApprovalData` | Approve/reject/edit for email drafts, follow-ups, proposals |
| `buildHITLConfirmationMessage` | `HITLConfirmationData` | Checkbox confirmation |
| `buildHITLEditRequestMessage` | `HITLEditRequestData` | Suggest edits |
| `buildHITLActionedConfirmation` | `HITLActionedConfirmation` | Action completed |

### Intelligence & Alerts

| Builder | Interface | Use Case |
|---------|-----------|----------|
| `buildMorningBriefMessage` | `MorningBriefData` | Morning briefing |
| `buildStaleDealAlertMessage` | `StaleDealAlertData` | Stale deal warning |
| `buildEmailReplyAlertMessage` | `EmailReplyAlertData` | Email response alert |
| `buildAccountSignalAlert` | `AccountSignalAlertData` | Account signal |
| `buildAccountIntelligenceDigest` | `AccountDigestData` | Weekly account digest |

## Delivery via send-slack-message

The `send-slack-message` edge function accepts `message_type` + `data` and routes to the appropriate builder:

```typescript
// From an orchestrator adapter:
await fetch(`${supabaseUrl}/functions/v1/send-slack-message`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${serviceKey}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    org_id: state.event.org_id,
    user_id: state.event.user_id,
    message_type: 'coaching_digest',  // routes to builder
    data: { /* matches WeeklyCoachingDigestData */ },
  }),
});
```

**Supported message_type values**: `meeting_briefing`, `coaching_digest`, `campaign_report`

For message types not yet wired, call the builder directly and pass `blocks` to the function.

## Design Principles

See `references/sales-message-patterns.md` for complete pattern library and `references/visual-techniques.md` for score displays and progress bars.

1. **Lead with impact** — Most important number or insight first
2. **Max 3 buttons** — 1 primary (green), 1-2 secondary (gray)
3. **Fields for KPIs** — Use `sectionWithFields` for metric grids
4. **Context at bottom** — Timestamps, attribution, metadata
5. **Always set fallback text** — Screen readers and notifications use `text`
6. **Truncate before building** — Use `safeMrkdwn()`, `safeHeaderText()` helpers
7. **Dividers sparingly** — Only between distinct content groups
8. **Under 10 blocks** for routine messages, up to 20 for weekly digests

## Quality Check

Before delivering any Slack message:
- [ ] Top-level `text` field populated (accessibility + notifications)
- [ ] Header under 150 chars
- [ ] Section text under 3000 chars
- [ ] Max 3 buttons per actions block, 1 primary
- [ ] No `value` + `url` on the same button (URL buttons for external links)
- [ ] `action_id` follows convention: `{domain}_{action}_{entityId}`
- [ ] Emoji used for quick visual scanning, not as sole indicators
- [ ] Renders well on mobile (fields stack vertically)
