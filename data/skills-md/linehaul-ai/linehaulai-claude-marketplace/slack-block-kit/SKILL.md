---
name: slack-block-kit
description: Build Slack Block Kit UIs for messages, modals, and Home tabs. Use when creating Slack notifications, interactive forms, bot responses, app dashboards, or any Slack UI. Covers blocks (Section, Actions, Input, Header), elements (Buttons, Selects, Date pickers), composition objects, and the slack-block-builder library.
keywords: [slack, ui, block-kit, messaging, interactive-components]
---

# Slack Block Kit

Expert guide for building Slack UIs with Block Kit.

## Overview

Block Kit is Slack's UI framework for creating rich, interactive messages, modals, and Home tabs. It uses a JSON-based structure with three main components:

- **Blocks**: Layout containers (Section, Actions, Input, Header, etc.)
- **Elements**: Interactive components (Buttons, Selects, Date pickers)
- **Composition Objects**: Text, options, and confirmations

## Surfaces

Block Kit works on three surfaces:

| Surface | Max Blocks | Use Cases |
|---------|------------|-----------|
| Messages | 50 | Notifications, bot responses, channel posts |
| Modals | 100 | Forms, confirmations, multi-step workflows |
| Home tabs | 100 | App dashboards, user-specific content |

## Quick Start

### Simple Message

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "New Order Received"
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Order ID:*\n#12345"
        },
        {
          "type": "mrkdwn",
          "text": "*Customer:*\nJohn Doe"
        }
      ]
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "View Order"
          },
          "style": "primary",
          "action_id": "view_order",
          "value": "12345"
        }
      ]
    }
  ]
}
```

### Using slack-block-builder (JavaScript)

```javascript
import { Message, Blocks, Elements } from 'slack-block-builder';

const orderNotification = ({ orderId, customer, channel }) => {
  return Message({ channel, text: 'New Order Received' })
    .blocks(
      Blocks.Header({ text: 'New Order Received' }),
      Blocks.Section()
        .fields([
          `*Order ID:*\n#${orderId}`,
          `*Customer:*\n${customer}`
        ]),
      Blocks.Actions()
        .elements(
          Elements.Button({ text: 'View Order', actionId: 'view_order' })
            .primary()
            .value(orderId)
        )
    )
    .buildToObject();
};
```

## Blocks Reference

### Header Block

Displays large text for titles.

```json
{
  "type": "header",
  "text": {
    "type": "plain_text",
    "text": "Budget Performance",
    "emoji": true
  }
}
```

**Fields:**
- `type` (required): Always `"header"`
- `text` (required): plain_text object, max 150 chars
- `block_id` (optional): Unique identifier, max 255 chars

**Surfaces:** Messages, Modals, Home tabs

### Section Block

Most versatile block for text and accessories.

```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "*Project Update*\nThe deployment is complete."
  },
  "accessory": {
    "type": "button",
    "text": {
      "type": "plain_text",
      "text": "View Details"
    },
    "action_id": "view_details"
  }
}
```

**With Fields (two-column layout):**

```json
{
  "type": "section",
  "fields": [
    {
      "type": "mrkdwn",
      "text": "*Status:*\nApproved"
    },
    {
      "type": "mrkdwn",
      "text": "*Created:*\nDec 15, 2025"
    },
    {
      "type": "mrkdwn",
      "text": "*Priority:*\nHigh"
    },
    {
      "type": "mrkdwn",
      "text": "*Assignee:*\n<@U123ABC>"
    }
  ]
}
```

**Fields:**
- `type` (required): Always `"section"`
- `text` (optional): Text object (mrkdwn or plain_text), max 3000 chars
- `fields` (optional): Array of text objects (max 10), each max 2000 chars
- `accessory` (optional): One interactive element
- `block_id` (optional): Unique identifier
- `expand` (optional): Boolean, expand text by default

**Surfaces:** Messages, Modals, Home tabs

### Actions Block

Contains multiple interactive elements.

```json
{
  "type": "actions",
  "block_id": "approval_actions",
  "elements": [
    {
      "type": "button",
      "text": {
        "type": "plain_text",
        "text": "Approve"
      },
      "style": "primary",
      "action_id": "approve_request",
      "value": "approved"
    },
    {
      "type": "button",
      "text": {
        "type": "plain_text",
        "text": "Reject"
      },
      "style": "danger",
      "action_id": "reject_request",
      "value": "rejected"
    }
  ]
}
```

**Fields:**
- `type` (required): Always `"actions"`
- `elements` (required): Array of interactive elements (max 25)
- `block_id` (optional): Unique identifier

**Surfaces:** Messages, Modals, Home tabs

### Input Block

Collects user input (modals and Home tabs primarily).

```json
{
  "type": "input",
  "block_id": "description_input",
  "label": {
    "type": "plain_text",
    "text": "Description"
  },
  "element": {
    "type": "plain_text_input",
    "action_id": "description_value",
    "multiline": true,
    "placeholder": {
      "type": "plain_text",
      "text": "Enter a description..."
    }
  },
  "optional": true,
  "hint": {
    "type": "plain_text",
    "text": "Provide additional context"
  }
}
```

**Fields:**
- `type` (required): Always `"input"`
- `element` (required): Input element (text input, select, date picker, etc.)
- `label` (required): plain_text object, max 2000 chars
- `block_id` (optional): Unique identifier
- `hint` (optional): plain_text object, max 2000 chars
- `optional` (optional): Boolean, default false
- `dispatch_action` (optional): Boolean, dispatch block_actions on change

**Surfaces:** Modals, Messages, Home tabs

### Context Block

Displays secondary, contextual information.

```json
{
  "type": "context",
  "elements": [
    {
      "type": "image",
      "image_url": "https://example.com/avatar.png",
      "alt_text": "User avatar"
    },
    {
      "type": "mrkdwn",
      "text": "Posted by <@U123ABC> on Dec 15, 2025"
    }
  ]
}
```

**Fields:**
- `type` (required): Always `"context"`
- `elements` (required): Array of image/text elements (max 10)
- `block_id` (optional): Unique identifier

**Surfaces:** Messages, Modals, Home tabs

### Divider Block

Visual separator between blocks.

```json
{
  "type": "divider"
}
```

**Surfaces:** Messages, Modals, Home tabs

### Image Block

Displays an image.

```json
{
  "type": "image",
  "image_url": "https://example.com/chart.png",
  "alt_text": "Sales chart",
  "title": {
    "type": "plain_text",
    "text": "Q4 Sales Performance"
  }
}
```

**Fields:**
- `type` (required): Always `"image"`
- `image_url` (required*): Public URL, max 3000 chars
- `slack_file` (required*): Alternative to image_url
- `alt_text` (required): Description, max 2000 chars
- `title` (optional): plain_text object, max 2000 chars
- `block_id` (optional): Unique identifier

*One of `image_url` or `slack_file` is required

**Surfaces:** Messages, Modals, Home tabs

### Markdown Block

Displays formatted markdown (messages only).

```json
{
  "type": "markdown",
  "text": "**Important:** This is *formatted* text with `code`."
}
```

**Surfaces:** Messages only

### Rich Text Block

Structured text representation.

```json
{
  "type": "rich_text",
  "elements": [
    {
      "type": "rich_text_section",
      "elements": [
        {
          "type": "text",
          "text": "Hello ",
          "style": {
            "bold": true
          }
        },
        {
          "type": "user",
          "user_id": "U123ABC"
        }
      ]
    }
  ]
}
```

**Surfaces:** Messages, Modals, Home tabs

### Video Block

Embeds a video player.

```json
{
  "type": "video",
  "title": {
    "type": "plain_text",
    "text": "Product Demo"
  },
  "video_url": "https://example.com/video.mp4",
  "thumbnail_url": "https://example.com/thumb.png",
  "alt_text": "Product demonstration video"
}
```

**Surfaces:** Messages, Modals, Home tabs

## Elements Reference

### Button Element

Interactive button for actions.

```json
{
  "type": "button",
  "text": {
    "type": "plain_text",
    "text": "Click Me",
    "emoji": true
  },
  "action_id": "button_click",
  "value": "button_value",
  "style": "primary"
}
```

**Fields:**
- `type` (required): Always `"button"`
- `text` (required): plain_text object, max 75 chars
- `action_id` (optional): Identifier for interaction, max 255 chars
- `value` (optional): Payload value, max 2000 chars
- `style` (optional): `"primary"` (green) or `"danger"` (red)
- `url` (optional): URL to open, max 3000 chars
- `confirm` (optional): Confirmation dialog
- `accessibility_label` (optional): Screen reader text, max 75 chars

**Works with:** Section (accessory), Actions

### Static Select Menu

Dropdown with predefined options.

```json
{
  "type": "static_select",
  "action_id": "priority_select",
  "placeholder": {
    "type": "plain_text",
    "text": "Select priority"
  },
  "options": [
    {
      "text": {
        "type": "plain_text",
        "text": "High"
      },
      "value": "high"
    },
    {
      "text": {
        "type": "plain_text",
        "text": "Medium"
      },
      "value": "medium"
    },
    {
      "text": {
        "type": "plain_text",
        "text": "Low"
      },
      "value": "low"
    }
  ],
  "initial_option": {
    "text": {
      "type": "plain_text",
      "text": "Medium"
    },
    "value": "medium"
  }
}
```

**Fields:**
- `type` (required): `"static_select"`
- `action_id` (optional): Interaction identifier
- `options` (required*): Array of option objects (max 100)
- `option_groups` (required*): Grouped options (max 100 groups)
- `initial_option` (optional): Pre-selected option
- `placeholder` (optional): Placeholder text, max 150 chars
- `confirm` (optional): Confirmation dialog
- `focus_on_load` (optional): Auto-focus in modals

*One of `options` or `option_groups` required

### External Select Menu

Dropdown with dynamically loaded options.

```json
{
  "type": "external_select",
  "action_id": "customer_select",
  "placeholder": {
    "type": "plain_text",
    "text": "Search customers..."
  },
  "min_query_length": 2
}
```

**Fields:**
- `type` (required): `"external_select"`
- `action_id` (optional): Interaction identifier
- `min_query_length` (optional): Min chars before query (default 3)
- `initial_option` (optional): Pre-selected option
- `placeholder` (optional): Placeholder text

### Users Select Menu

Select workspace users.

```json
{
  "type": "users_select",
  "action_id": "assignee_select",
  "placeholder": {
    "type": "plain_text",
    "text": "Select assignee"
  },
  "initial_user": "U123ABC"
}
```

### Channels Select Menu

Select public channels.

```json
{
  "type": "channels_select",
  "action_id": "channel_select",
  "placeholder": {
    "type": "plain_text",
    "text": "Select channel"
  },
  "initial_channel": "C123ABC"
}
```

### Conversations Select Menu

Select any conversation (channels, DMs, groups).

```json
{
  "type": "conversations_select",
  "action_id": "conversation_select",
  "placeholder": {
    "type": "plain_text",
    "text": "Select conversation"
  },
  "default_to_current_conversation": true
}
```

### Multi-Select Menus

All select menus have multi-select variants:

- `multi_static_select`
- `multi_external_select`
- `multi_users_select`
- `multi_channels_select`
- `multi_conversations_select`

```json
{
  "type": "multi_users_select",
  "action_id": "team_select",
  "placeholder": {
    "type": "plain_text",
    "text": "Select team members"
  },
  "max_selected_items": 5
}
```

### Date Picker

Select a date.

```json
{
  "type": "datepicker",
  "action_id": "due_date",
  "placeholder": {
    "type": "plain_text",
    "text": "Select due date"
  },
  "initial_date": "2025-12-31"
}
```

### Time Picker

Select a time.

```json
{
  "type": "timepicker",
  "action_id": "meeting_time",
  "placeholder": {
    "type": "plain_text",
    "text": "Select time"
  },
  "initial_time": "14:30"
}
```

### Datetime Picker

Select date and time together.

```json
{
  "type": "datetimepicker",
  "action_id": "event_datetime",
  "initial_date_time": 1734307200
}
```

### Checkboxes

Multiple selection from options.

```json
{
  "type": "checkboxes",
  "action_id": "features_select",
  "options": [
    {
      "text": {
        "type": "plain_text",
        "text": "Email notifications"
      },
      "value": "email",
      "description": {
        "type": "mrkdwn",
        "text": "*Receive daily summary*"
      }
    },
    {
      "text": {
        "type": "plain_text",
        "text": "Slack notifications"
      },
      "value": "slack"
    }
  ],
  "initial_options": [
    {
      "text": {
        "type": "plain_text",
        "text": "Email notifications"
      },
      "value": "email"
    }
  ]
}
```

### Radio Buttons

Single selection from options.

```json
{
  "type": "radio_buttons",
  "action_id": "urgency_select",
  "options": [
    {
      "text": {
        "type": "plain_text",
        "text": "Urgent"
      },
      "value": "urgent"
    },
    {
      "text": {
        "type": "plain_text",
        "text": "Standard"
      },
      "value": "standard"
    }
  ],
  "initial_option": {
    "text": {
      "type": "plain_text",
      "text": "Standard"
    },
    "value": "standard"
  }
}
```

### Plain Text Input

Single or multi-line text input.

```json
{
  "type": "plain_text_input",
  "action_id": "comment_input",
  "placeholder": {
    "type": "plain_text",
    "text": "Enter your comment..."
  },
  "multiline": true,
  "min_length": 10,
  "max_length": 500
}
```

### Number Input

Numeric input with validation.

```json
{
  "type": "number_input",
  "action_id": "quantity_input",
  "is_decimal_allowed": false,
  "min_value": "1",
  "max_value": "100",
  "placeholder": {
    "type": "plain_text",
    "text": "Enter quantity"
  }
}
```

### URL Input

URL input with validation.

```json
{
  "type": "url_text_input",
  "action_id": "website_input",
  "placeholder": {
    "type": "plain_text",
    "text": "https://example.com"
  }
}
```

### Email Input

Email input with validation.

```json
{
  "type": "email_text_input",
  "action_id": "email_input",
  "placeholder": {
    "type": "plain_text",
    "text": "you@example.com"
  }
}
```

### Rich Text Input

Formatted text input.

```json
{
  "type": "rich_text_input",
  "action_id": "content_input",
  "placeholder": {
    "type": "plain_text",
    "text": "Write your content..."
  }
}
```

### File Input

File upload (modals only).

```json
{
  "type": "file_input",
  "action_id": "attachment_input",
  "filetypes": ["pdf", "png", "jpg"],
  "max_files": 3
}
```

### Overflow Menu

Compact menu for secondary actions.

```json
{
  "type": "overflow",
  "action_id": "more_actions",
  "options": [
    {
      "text": {
        "type": "plain_text",
        "text": "Edit"
      },
      "value": "edit"
    },
    {
      "text": {
        "type": "plain_text",
        "text": "Delete"
      },
      "value": "delete"
    }
  ]
}
```

## Composition Objects

### Text Object

Used throughout Block Kit for text content.

**Plain Text:**
```json
{
  "type": "plain_text",
  "text": "Hello, world!",
  "emoji": true
}
```

**Markdown (mrkdwn):**
```json
{
  "type": "mrkdwn",
  "text": "*Bold* _italic_ ~strike~ `code` <https://example.com|link>"
}
```

### Confirmation Dialog

Confirmation before destructive actions.

```json
{
  "title": {
    "type": "plain_text",
    "text": "Confirm Delete"
  },
  "text": {
    "type": "mrkdwn",
    "text": "Are you sure you want to delete this item? This cannot be undone."
  },
  "confirm": {
    "type": "plain_text",
    "text": "Delete"
  },
  "deny": {
    "type": "plain_text",
    "text": "Cancel"
  },
  "style": "danger"
}
```

### Option Object

For select menus, checkboxes, and radio buttons.

```json
{
  "text": {
    "type": "plain_text",
    "text": "Option Label"
  },
  "value": "option_value",
  "description": {
    "type": "plain_text",
    "text": "Optional description"
  },
  "url": "https://example.com"
}
```

### Option Group

Grouped options for select menus.

```json
{
  "label": {
    "type": "plain_text",
    "text": "Group Label"
  },
  "options": [
    {
      "text": {
        "type": "plain_text",
        "text": "Option 1"
      },
      "value": "option_1"
    }
  ]
}
```

## Modal Reference

### Opening a Modal

```json
{
  "type": "modal",
  "callback_id": "feedback_modal",
  "title": {
    "type": "plain_text",
    "text": "Submit Feedback"
  },
  "submit": {
    "type": "plain_text",
    "text": "Submit"
  },
  "close": {
    "type": "plain_text",
    "text": "Cancel"
  },
  "blocks": [
    {
      "type": "input",
      "block_id": "feedback_type",
      "label": {
        "type": "plain_text",
        "text": "Feedback Type"
      },
      "element": {
        "type": "static_select",
        "action_id": "type_select",
        "options": [
          {
            "text": {
              "type": "plain_text",
              "text": "Bug Report"
            },
            "value": "bug"
          },
          {
            "text": {
              "type": "plain_text",
              "text": "Feature Request"
            },
            "value": "feature"
          }
        ]
      }
    },
    {
      "type": "input",
      "block_id": "feedback_content",
      "label": {
        "type": "plain_text",
        "text": "Description"
      },
      "element": {
        "type": "plain_text_input",
        "action_id": "content_input",
        "multiline": true
      }
    }
  ]
}
```

### Modal Fields

- `type` (required): Always `"modal"`
- `title` (required): plain_text, max 24 chars
- `blocks` (required): Array of blocks (max 100)
- `callback_id` (optional): Identifier for view_submission
- `submit` (optional): Submit button text, max 24 chars
- `close` (optional): Close button text, max 24 chars
- `private_metadata` (optional): String passed to submission, max 3000 chars
- `clear_on_close` (optional): Clear all views on close
- `notify_on_close` (optional): Send view_closed event
- `external_id` (optional): Custom identifier
- `submit_disabled` (optional): Disable submit button initially

## slack-block-builder Library

### Installation

```bash
npm install slack-block-builder
```

### Imports

```javascript
import {
  Message,
  Modal,
  HomeTab,
  Blocks,
  Elements,
  Bits,
  Md
} from 'slack-block-builder';
```

### Building Messages

```javascript
const message = Message({ channel: 'C123ABC', text: 'Fallback text' })
  .blocks(
    Blocks.Header({ text: 'Welcome!' }),
    Blocks.Section({ text: 'Hello, *world*!' }),
    Blocks.Divider(),
    Blocks.Actions()
      .elements(
        Elements.Button({ text: 'Click Me', actionId: 'click' })
          .primary()
      )
  )
  .buildToObject();
```

### Building Modals

```javascript
const modal = Modal({ title: 'My Form', callbackId: 'form_submit' })
  .submit('Save')
  .close('Cancel')
  .blocks(
    Blocks.Input({ label: 'Name', blockId: 'name_block' })
      .element(
        Elements.TextInput({ actionId: 'name_input' })
          .placeholder('Enter your name')
      ),
    Blocks.Input({ label: 'Priority', blockId: 'priority_block' })
      .element(
        Elements.StaticSelect({ actionId: 'priority_select' })
          .options(
            Bits.Option({ text: 'High', value: 'high' }),
            Bits.Option({ text: 'Medium', value: 'medium' }),
            Bits.Option({ text: 'Low', value: 'low' })
          )
      )
  )
  .buildToObject();
```

### Markdown Helpers

```javascript
import { Md } from 'slack-block-builder';

Md.bold('text')           // *text*
Md.italic('text')         // _text_
Md.strike('text')         // ~text~
Md.code('text')           // `text`
Md.codeBlock('text')      // ```text```
Md.link('url', 'text')    // <url|text>
Md.user('U123')           // <@U123>
Md.channel('C123')        // <#C123>
Md.emoji('smile')         // :smile:
Md.listBullet(['a', 'b']) // • a\n• b
```

### Build Methods

```javascript
// Returns JavaScript object
modal.buildToObject();

// Returns JSON string
modal.buildToJSON();

// Returns only blocks array
modal.getBlocks();
```

## Best Practices

### Naming Conventions

- `action_id`: `{verb}_{noun}` - e.g., `submit_form`, `select_priority`
- `block_id`: `{noun}_block` - e.g., `name_block`, `options_block`
- `callback_id`: `{feature}_{action}` - e.g., `feedback_submit`

### Performance

- Keep messages under 50 blocks
- Keep modals under 100 blocks
- Use external_select for large option lists (>100 items)
- Minimize image usage in high-traffic messages

### Accessibility

- Always provide `alt_text` for images
- Use `accessibility_label` for buttons with icons
- Ensure sufficient color contrast
- Provide clear, descriptive labels

### Mobile Considerations

- Use shorter text (truncation occurs ~30 chars for buttons)
- Limit fields in Section blocks (2-3 max)
- Test in mobile Slack client
- Avoid complex nested layouts

## Common Patterns

### Notification with Actions

```javascript
Message({ channel, text: 'New request' })
  .blocks(
    Blocks.Header({ text: 'New Request' }),
    Blocks.Section()
      .fields([
        `*From:*\n${requester}`,
        `*Priority:*\n${priority}`
      ]),
    Blocks.Context()
      .elements([`Submitted ${timestamp}`]),
    Blocks.Divider(),
    Blocks.Actions()
      .elements(
        Elements.Button({ text: 'Approve', actionId: 'approve' }).primary(),
        Elements.Button({ text: 'Reject', actionId: 'reject' }).danger()
      )
  )
  .buildToObject();
```

### Form Modal with Validation

```javascript
Modal({ title: 'Create Task', callbackId: 'task_create' })
  .submit('Create')
  .close('Cancel')
  .blocks(
    Blocks.Input({ label: 'Task Name', blockId: 'name' })
      .element(Elements.TextInput({ actionId: 'name_input' })),
    Blocks.Input({ label: 'Assignee', blockId: 'assignee' })
      .element(Elements.UsersSelect({ actionId: 'assignee_select' })),
    Blocks.Input({ label: 'Due Date', blockId: 'due_date' })
      .element(Elements.DatePicker({ actionId: 'date_select' }))
      .optional(true)
  )
  .buildToObject();
```

### Home Tab Dashboard

```javascript
HomeTab()
  .blocks(
    Blocks.Header({ text: `Welcome, ${userName}!` }),
    Blocks.Section({ text: 'Here are your pending tasks:' }),
    Blocks.Divider(),
    ...tasks.map(task =>
      Blocks.Section({ text: `• ${task.title}` })
        .accessory(
          Elements.Button({ text: 'Complete', actionId: `complete_${task.id}` })
        )
    ),
    Blocks.Divider(),
    Blocks.Actions()
      .elements(
        Elements.Button({ text: 'New Task', actionId: 'new_task' }).primary()
      )
  )
  .buildToObject();
```

## Troubleshooting

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `invalid_blocks` | Malformed JSON | Validate in Block Kit Builder |
| `too_many_blocks` | Exceeds limit | Reduce to 50 (msg) or 100 (modal) |
| `invalid_element` | Wrong element in block | Check element compatibility |
| `missing_text` | Required text missing | Add text or fields to Section |

### Validation Tips

1. Use [Block Kit Builder](https://app.slack.com/block-kit-builder) to test JSON
2. Check element compatibility with blocks
3. Verify required fields are present
4. Test on mobile for display issues

## Resources

### Reference Documentation

For comprehensive guides, see the `references/` directory:

- **[blocks.md](../../references/blocks.md)** - Detailed documentation on all block types
- **[interactive-components.md](../../references/interactive-components.md)** - Complete guide to interactive elements
- **[layout-patterns.md](../../references/layout-patterns.md)** - Composition and nesting best practices
- **[surfaces.md](../../references/surfaces.md)** - Messages, modals, and home tabs deep dive

### External Resources

- [Slack Block Kit Builder](https://app.slack.com/block-kit-builder)
- [Block Kit Documentation](https://api.slack.com/block-kit)
- [slack-block-builder GitHub](https://github.com/raycharius/slack-block-builder)
- [Slack API Reference](https://api.slack.com/reference)
