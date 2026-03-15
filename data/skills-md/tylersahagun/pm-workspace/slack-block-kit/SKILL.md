---
name: slack-block-kit
description: Format Slack messages using Block Kit for rich, interactive layouts. Apply when sending any Slack message that should look polished.
---

# Slack Block Kit Formatting Skill

This skill teaches agents to format Slack messages using Block Kit—a JSON-based UI framework for building rich, interactive messages.

## When to Apply This Skill

Apply when:

- Sending Slack messages via MCP tools
- Creating notifications, alerts, or status updates
- Building interactive messages with buttons or menus
- Formatting EOD/EOW reports for Slack
- Any message that should look professional

## MCP Tools

**Server:** `composio-config` (Composio)
**Tool:** `SLACK_SEND_MESSAGE`

```json
{
  "channel": "C12345678",
  "text": "Fallback text for notifications",
  "blocks": [ ... ]
}
```

**Important:** Always include top-level `text` as notification fallback.

---

## Architecture

```
Message Payload
└── blocks[] (layout containers, max 50)
    └── Block elements (interactive components)
        └── Composition objects (text, options)
```

---

## Block Types Quick Reference

| Type        | Use For              | Key Rules                                   |
| ----------- | -------------------- | ------------------------------------------- |
| `header`    | Titles               | 150 chars max, `plain_text` only            |
| `section`   | Main content         | 3000 chars, can have accessory              |
| `divider`   | Visual separation    | No content                                  |
| `image`     | Standalone images    | HTTPS URL required, `alt_text` required     |
| `context`   | Metadata, timestamps | Max 10 elements, renders small/muted        |
| `actions`   | Button rows, menus   | Max 25 elements                             |
| `table`     | Tabular data         | **1 per message**, max 100 rows, 20 columns |
| `rich_text` | Formatted text       | Lists, quotes, code blocks, styled text     |

---

## Table Block (NEW)

**Constraints:**

- **Only 1 table per message** (error: `only_one_table_allowed`)
- Table renders at BOTTOM of message (appended)
- Max 100 rows, 20 columns
- Cells can be `raw_text` or `rich_text`

### Basic Table

```json
{
  "type": "table",
  "column_settings": [
    { "align": "left" },
    { "align": "center" },
    { "align": "right" }
  ],
  "rows": [
    [
      { "type": "raw_text", "text": "Name" },
      { "type": "raw_text", "text": "Count" },
      { "type": "raw_text", "text": "Value" }
    ],
    [
      { "type": "raw_text", "text": "Item A" },
      { "type": "raw_text", "text": "5" },
      { "type": "raw_text", "text": "$100" }
    ]
  ]
}
```

### Column Settings

| Property     | Type    | Description                                |
| ------------ | ------- | ------------------------------------------ |
| `align`      | string  | `left`, `center`, or `right`               |
| `is_wrapped` | boolean | Whether to wrap long text (default: false) |

### Table with Rich Text Cells (Links, Bold)

```json
{
  "type": "table",
  "rows": [
    [
      { "type": "raw_text", "text": "Deal" },
      { "type": "raw_text", "text": "ARR" }
    ],
    [
      {
        "type": "rich_text",
        "elements": [
          {
            "type": "rich_text_section",
            "elements": [
              {
                "type": "link",
                "text": "Acme Corp",
                "url": "https://hubspot.com/deal/123"
              }
            ]
          }
        ]
      },
      {
        "type": "rich_text",
        "elements": [
          {
            "type": "rich_text_section",
            "elements": [
              { "type": "text", "text": "$50,000", "style": { "bold": true } }
            ]
          }
        ]
      }
    ]
  ]
}
```

---

## Rich Text Block

Rich text provides more flexibility than mrkdwn. Use for complex formatting needs.

### Rich Text Section (Basic)

```json
{
  "type": "rich_text",
  "elements": [
    {
      "type": "rich_text_section",
      "elements": [
        { "type": "text", "text": "Hello " },
        { "type": "text", "text": "bold text", "style": { "bold": true } },
        { "type": "text", "text": " and " },
        { "type": "text", "text": "italic", "style": { "italic": true } }
      ]
    }
  ]
}
```

### Rich Text List (Bullet/Numbered)

```json
{
  "type": "rich_text",
  "elements": [
    {
      "type": "rich_text_section",
      "elements": [{ "type": "text", "text": "Features shipped:" }]
    },
    {
      "type": "rich_text_list",
      "style": "bullet",
      "elements": [
        {
          "type": "rich_text_section",
          "elements": [{ "type": "text", "text": "HubSpot integration" }]
        },
        {
          "type": "rich_text_section",
          "elements": [{ "type": "text", "text": "Mobile improvements" }]
        }
      ]
    }
  ]
}
```

### Rich Text Quote

```json
{
  "type": "rich_text",
  "elements": [
    {
      "type": "rich_text_quote",
      "elements": [
        {
          "type": "text",
          "text": "This is really going to change how we work."
        }
      ]
    }
  ]
}
```

### Rich Text Element Types

| Type        | Properties                      | Use For                  |
| ----------- | ------------------------------- | ------------------------ |
| `text`      | `text`, `style`                 | Plain/styled text        |
| `link`      | `url`, `text`, `style`          | Clickable links          |
| `user`      | `user_id`, `style`              | @mentions                |
| `channel`   | `channel_id`, `style`           | #channel links           |
| `usergroup` | `usergroup_id`, `style`         | @group mentions          |
| `emoji`     | `name`, `unicode`               | Emoji                    |
| `date`      | `timestamp`, `format`           | Formatted dates          |
| `broadcast` | `range` (here/channel/everyone) | @here/@channel/@everyone |

### Text Style Object

```json
{
  "style": {
    "bold": true,
    "italic": true,
    "strike": true,
    "code": true
  }
}
```

---

## Block JSON Structures

### Header Block

```json
{
  "type": "header",
  "text": {
    "type": "plain_text",
    "text": ":rocket: Header Text Here",
    "emoji": true
  }
}
```

### Section Block

```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "*Bold* and _italic_ text with <https://example.com|links>"
  }
}
```

### Section with Accessory (Button)

```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "Your meeting has been processed."
  },
  "accessory": {
    "type": "button",
    "text": { "type": "plain_text", "text": "View", "emoji": true },
    "url": "https://app.askelephant.com/meetings/123",
    "action_id": "view_meeting"
  }
}
```

### Section with Fields (Two-Column Layout)

```json
{
  "type": "section",
  "fields": [
    { "type": "mrkdwn", "text": "*Status:*\nComplete" },
    { "type": "mrkdwn", "text": "*Duration:*\n45 min" },
    { "type": "mrkdwn", "text": "*Attendees:*\n4 people" },
    { "type": "mrkdwn", "text": "*Priority:*\nHigh" }
  ]
}
```

**Rules:** Max 10 fields, each max 2000 chars.

### Divider Block

```json
{
  "type": "divider"
}
```

### Image Block

```json
{
  "type": "image",
  "image_url": "https://example.com/chart.png",
  "alt_text": "Q4 revenue chart"
}
```

### Context Block

```json
{
  "type": "context",
  "elements": [
    {
      "type": "mrkdwn",
      "text": ":clock1: Posted at <!date^1706451200^{date_short_pretty} at {time}|Jan 28, 2026>"
    }
  ]
}
```

### Actions Block

```json
{
  "type": "actions",
  "block_id": "actions_1",
  "elements": [
    {
      "type": "button",
      "text": { "type": "plain_text", "text": "Approve", "emoji": true },
      "style": "primary",
      "action_id": "approve_btn",
      "value": "approved"
    },
    {
      "type": "button",
      "text": { "type": "plain_text", "text": "Reject", "emoji": true },
      "style": "danger",
      "action_id": "reject_btn",
      "value": "rejected"
    }
  ]
}
```

**Button styles:** `primary` (green), `danger` (red), or omit for default gray.

---

## mrkdwn Syntax (NOT Standard Markdown!)

### Text Formatting

| Format        | Syntax         | Example            |
| ------------- | -------------- | ------------------ |
| Bold          | `*text*`       | `*important*`      |
| Italic        | `_text_`       | `_emphasis_`       |
| Strikethrough | `~text~`       | `~deleted~`        |
| Code          | `` `code` ``   | `` `function()` `` |
| Code block    | ` ```code``` ` | Multi-line         |
| Quote         | `>text`        | Indented           |

### Links and Mentions

| Type          | Syntax                              |
| ------------- | ----------------------------------- |
| URL           | `<https://example.com>`             |
| URL with text | `<https://example.com\|Click here>` |
| User mention  | `<@U12345678>`                      |
| Channel link  | `<#C12345678>`                      |
| @here         | `<!here>`                           |
| @channel      | `<!channel>`                        |

### Escape Characters

| Character | Escape As |
| --------- | --------- |
| `&`       | `&amp;`   |
| `<`       | `&lt;`    |
| `>`       | `&gt;`    |

### NOT Supported (Common Mistakes)

| Wrong         | Correct          |
| ------------- | ---------------- |
| `**bold**`    | `*bold*`         |
| `*italic*`    | `_italic_`       |
| `[text](url)` | `<url\|text>`    |
| `# Header`    | Use header block |

---

## Message Templates by Use Case

### Newsletter Template (Polished)

Use for company-wide updates, weekly digests, or announcements.

```json
{
  "text": "Paper Company Newsletter - November 12, 2019",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": ":newspaper:  AskElephant Update  :newspaper:",
        "emoji": true
      }
    },
    {
      "type": "context",
      "elements": [
        {
          "text": "*January 28, 2026*  |  Product Team",
          "type": "mrkdwn"
        }
      ]
    },
    { "type": "divider" },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": ":loud_sound: *IN CASE YOU MISSED IT* :loud_sound:"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "The *HubSpot integration* shipped last week. Customers can now sync all their meeting data to HubSpot automatically."
      },
      "accessory": {
        "type": "button",
        "text": { "type": "plain_text", "text": "Learn More", "emoji": true },
        "url": "https://docs.askelephant.com/hubspot"
      }
    },
    { "type": "divider" },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": ":calendar: |   *UPCOMING*  | :calendar:"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "`02/01` *Speaker ID V2* — Improved speaker identification\n`02/15` *Admin Onboarding* — Streamlined workspace setup"
      }
    },
    { "type": "divider" },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*FOR YOUR INFORMATION*"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": ":bulb: *Mobile app update* is now available. Make sure customers update for better recording reliability."
      }
    },
    { "type": "divider" },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": ":pushpin: Questions? Drop them in *#product-forum*"
        }
      ]
    }
  ]
}
```

### Rob Report (Revenue Team, Simple Language)

Use for CRO/revenue team updates with simplified language and customer-visible features only.

```json
{
  "text": "What's New - January 27, 2026",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "What's New - January 27, 2026",
        "emoji": true
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "Hey Revenue Team! Here's what shipped that you can use with customers right now."
      }
    },
    { "type": "divider" },
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "What's New",
        "emoji": true
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*The app runs faster now* — Pages load quicker, especially with lots of conversations.\n\n*@ mentions work better in chat* — AskElephant understands who you're talking about more reliably."
      }
    },
    { "type": "divider" },
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "What We Fixed",
        "emoji": true
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "• Notification banners showing at wrong time\n• Scrolling no longer jumps around\n• Words getting cut off in meeting details"
      }
    },
    { "type": "divider" },
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "Revenue Wins",
        "emoji": true
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Total New ARR:* $20,399 (4 deals)\n*Expansion:* $5,700 (Hadco Construction)\n*Total ARR Impact:* $26,100"
      }
    },
    { "type": "divider" },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "_All features listed are available to your team now._"
      }
    },
    {
      "type": "table",
      "column_settings": [
        { "align": "left" },
        { "align": "center" },
        { "align": "center" },
        { "align": "center" },
        { "align": "center" }
      ],
      "rows": [
        [
          { "type": "raw_text", "text": "SDR" },
          { "type": "raw_text", "text": "Convos" },
          { "type": "raw_text", "text": "Pitches" },
          { "type": "raw_text", "text": "Meetings" },
          { "type": "raw_text", "text": "ICP Held" }
        ],
        [
          { "type": "raw_text", "text": "Jamis Benson" },
          { "type": "raw_text", "text": "7" },
          { "type": "raw_text", "text": "6" },
          { "type": "raw_text", "text": "4" },
          { "type": "raw_text", "text": "2" }
        ],
        [
          { "type": "raw_text", "text": "Carter Thomas" },
          { "type": "raw_text", "text": "8" },
          { "type": "raw_text", "text": "6" },
          { "type": "raw_text", "text": "5" },
          { "type": "raw_text", "text": "1" }
        ],
        [
          { "type": "raw_text", "text": "Team Total" },
          { "type": "raw_text", "text": "18" },
          { "type": "raw_text", "text": "14" },
          { "type": "raw_text", "text": "12" },
          { "type": "raw_text", "text": "3" }
        ]
      ]
    }
  ]
}
```

### Daily Digest (Engineering/Product)

```json
{
  "text": "AskElephant Daily Digest",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "AskElephant Daily Digest",
        "emoji": true
      }
    },
    {
      "type": "context",
      "elements": [
        { "type": "mrkdwn", "text": ":newspaper: Thursday, January 23, 2026" }
      ]
    },
    { "type": "divider" },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*:trophy: Today's Headline*\n\n>*Dialpad Goes Live + Desktop Stability* — Another major telephony platform now integrated."
      }
    },
    { "type": "divider" },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*:sparkles: New Features*\n\n*CRM Integrations*\n• Dialpad direct integration — full telephony support\n• Dialpad event handling — deduplication and routing\n\n*Recording & Capture*\n• Desktop MP4 audio — higher quality recordings\n• Web recording visual feedback"
      }
    },
    { "type": "divider" },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*:wrench: Improvements*\n\n• Engagement page restored\n• AI description improvements\n• Query performance instrumented"
      }
    },
    { "type": "divider" },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*:bug: Bugs Fixed: 6*\n\n• Auto logout toggle restored\n• Desktop recording stop reliability\n• Mobile push notification delivery"
      }
    },
    { "type": "divider" },
    {
      "type": "section",
      "text": { "type": "mrkdwn", "text": "*:busts_in_silhouette: Team Focus*" }
    },
    {
      "type": "section",
      "fields": [
        { "type": "mrkdwn", "text": "*Eduardo*\nDialpad, desktop, mobile" },
        { "type": "mrkdwn", "text": "*Matt Noxon*\nPerformance, dataloaders" },
        { "type": "mrkdwn", "text": "*Jason*\nStripe, PostHog, analytics" },
        { "type": "mrkdwn", "text": "*Dylan*\nVoiceprint, embeddings" }
      ]
    },
    { "type": "divider" },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": ":chart_with_upwards_trend: *Stats:* 6 features | 3 improvements | 6 bugs fixed"
        },
        {
          "type": "mrkdwn",
          "text": ":rocket: *21 PRs merged* • *Eduardo leading with 10*"
        }
      ]
    }
  ]
}
```

### Deal Closed Celebration

```json
{
  "text": "Deal Closed: Acme Corp - $50,000 ARR",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": ":tada: Deal Closed!",
        "emoji": true
      }
    },
    {
      "type": "section",
      "fields": [
        { "type": "mrkdwn", "text": "*Account:*\nAcme Corp" },
        { "type": "mrkdwn", "text": "*ARR:*\n$50,000" },
        { "type": "mrkdwn", "text": "*Rep:*\n<@U12345>" },
        { "type": "mrkdwn", "text": "*Type:*\nNew Business" }
      ]
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "Closed on <!date^1706451200^{date_long}|January 28, 2026>"
        }
      ]
    }
  ]
}
```

### Approval Request (Interactive)

```json
{
  "text": "Approval Needed: Enterprise Pricing",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": ":raised_hand: Approval Needed",
        "emoji": true
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Enterprise Pricing Proposal*\nNew tier at $2,500/mo for 50+ seats."
      }
    },
    {
      "type": "section",
      "fields": [
        { "type": "mrkdwn", "text": "*Requested by:*\n<@U12345>" },
        { "type": "mrkdwn", "text": "*Deadline:*\nFeb 1, 2026" }
      ]
    },
    {
      "type": "actions",
      "block_id": "approval_actions",
      "elements": [
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "Approve", "emoji": true },
          "style": "primary",
          "action_id": "approve_proposal"
        },
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "Reject", "emoji": true },
          "style": "danger",
          "action_id": "reject_proposal"
        },
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "View Details",
            "emoji": true
          },
          "url": "https://notion.so/proposal-123",
          "action_id": "view_details"
        }
      ]
    }
  ]
}
```

### Alert/Warning

```json
{
  "text": "Alert: High API Error Rate",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": ":rotating_light: Alert: High Error Rate",
        "emoji": true
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "API error rate has exceeded 5% threshold.\n\n*Current rate:* 7.2%\n*Threshold:* 5%\n*Duration:* 15 minutes"
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "View Dashboard",
            "emoji": true
          },
          "url": "https://grafana.example.com/alerts",
          "style": "primary"
        },
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "Acknowledge",
            "emoji": true
          },
          "action_id": "ack_alert"
        }
      ]
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": ":clock1: Triggered at <!date^1706451200^{time}|2:30 PM>"
        }
      ]
    }
  ]
}
```

---

## Template Selection Decision Tree

```
What are you sending?
│
├── Update for Revenue Team (Rob, AEs, SDRs)?
│   └── Use: Rob Report Template
│       • Simple language (high school reading level)
│       • Customer-visible features only
│       • Table block for SDR metrics
│
├── Company-wide announcement?
│   └── Use: Newsletter Template
│       • Header with emoji
│       • Context with date
│       • "In Case You Missed It" section
│       • "Upcoming" with dates in backticks
│       • "For Your Information" callout
│
├── Engineering/Product digest?
│   └── Use: Daily Digest Template
│       • Headline quote block
│       • Categorized sections (Features, Improvements, Bugs)
│       • Team Focus with fields
│       • Stats in context block
│
├── Deal closed?
│   └── Use: Deal Closed Template
│       • Header with :tada:
│       • Fields for Account/ARR/Rep/Type
│       • Context with date
│
├── Need approval?
│   └── Use: Approval Request Template
│       • Actions block with Approve/Reject buttons
│       • Fields for requester/deadline
│
├── Alert/Error?
│   └── Use: Alert Template
│       • :rotating_light: emoji
│       • Current vs threshold values
│       • Acknowledge button
│
└── Tabular data?
    └── Use: Table Block (1 per message)
        • Put at END of blocks array
        • Use column_settings for alignment
        • Center numeric columns
```

---

## Block Selection Quick Guide

| Content Type       | Best Block                      |
| ------------------ | ------------------------------- |
| Title/Headline     | `header`                        |
| Main text          | `section`                       |
| Key-value pairs    | `section` with `fields`         |
| Text + button      | `section` with `accessory`      |
| Standalone image   | `image`                         |
| Row of buttons     | `actions`                       |
| Metadata/footer    | `context`                       |
| Visual break       | `divider`                       |
| Tabular data       | `table` (1 per message, at end) |
| Complex formatting | `rich_text`                     |

---

## Validation Checklist

Before sending:

- [ ] Valid JSON syntax
- [ ] Fallback `text` field at root level
- [ ] All `action_id` values unique
- [ ] Character limits respected (header: 150, section: 3000)
- [ ] Image URLs are HTTPS
- [ ] mrkdwn syntax correct (not standard Markdown)
- [ ] Max 50 blocks for messages
- [ ] Only 1 table block (if using tables)
- [ ] Table block is LAST in blocks array

---

## Common Emoji Reference

| Type     | Emojis                                                |
| -------- | ----------------------------------------------------- |
| Success  | `:white_check_mark:` `:tada:` `:rocket:`              |
| Alert    | `:warning:` `:rotating_light:` `:exclamation:`        |
| Info     | `:information_source:` `:memo:` `:newspaper:`         |
| Revenue  | `:moneybag:` `:chart_with_upwards_trend:` `:trophy:`  |
| Meetings | `:movie_camera:` `:calendar:` `:busts_in_silhouette:` |
| Dev      | `:hammer_and_wrench:` `:gear:` `:package:` `:bug:`    |
| Time     | `:clock1:` `:hourglass:` `:stopwatch:`                |
| Category | `:sparkles:` `:wrench:` `:loud_sound:` `:bulb:`       |

---

## Date Formatting

Use `<!date^TIMESTAMP^FORMAT|FALLBACK>` in mrkdwn.

| Token           | Output                           |
| --------------- | -------------------------------- |
| `{date_num}`    | 2026-01-28                       |
| `{date_short}`  | Jan 28, 2026                     |
| `{date_long}`   | Monday, January 28th, 2026       |
| `{date_pretty}` | today/yesterday/tomorrow or date |
| `{time}`        | 2:34 PM                          |
| `{ago}`         | 3 minutes ago                    |

Example:

```
<!date^1706451200^{date_short_pretty} at {time}|Jan 28, 2026>
```

---

## Testing

Recommend testing in [Block Kit Builder](https://app.slack.com/block-kit-builder) before sending.
