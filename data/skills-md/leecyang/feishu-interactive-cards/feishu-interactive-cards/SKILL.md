---
name: feishu-interactive-cards
version: 1.0.2
description: Create and send interactive cards to Feishu (Lark) with buttons, forms, polls, and rich UI elements. Use when replying to Feishu messages and there is ANY uncertainty - send an interactive card instead of plain text to let users choose via buttons. Automatically handles callbacks via long-polling connection. Use for confirmations, choices, forms, todos, polls, or any scenario requiring user interaction in Feishu.
---

# Feishu Interactive Cards

## Core Principle

**When replying to Feishu and there is ANY uncertainty: send an interactive card instead of plain text.**

Interactive cards let users respond via buttons rather than typing, making interactions faster and clearer.

## When to Use

**Must use interactive cards:**
- User needs to make a choice (yes/no, multiple options)
- Confirmation required before action
- Displaying todos or task lists
- Creating polls or surveys
- Collecting form input
- Any uncertain situation

**Plain text is OK:**
- Simple notifications (no response needed)
- Pure data display (no interaction)
- Confirmed command results

**Example:**
- Wrong: "I deleted the file for you" (direct execution)
- Right: Send card "Confirm delete file?" [Confirm] [Cancel]

## Quick Start

### 1. Start Callback Server (Long-Polling Mode)

```bash
cd E:\openclaw\workspace\skills\feishu-interactive-cards\scripts
node card-callback-server.js
```

**Features:**
- Uses Feishu long-polling (no public IP needed)
- Auto-reconnects
- Sends callbacks to OpenClaw Gateway automatically

### 2. Send Interactive Card

```bash
# Confirmation card
node scripts/send-card.js confirmation "Confirm delete file?" --chat-id oc_xxx

# Todo list
node scripts/send-card.js todo --chat-id oc_xxx

# Poll
node scripts/send-card.js poll "Team activity" --options "Bowling,Movie,Dinner" --chat-id oc_xxx

# Custom card
node scripts/send-card.js custom --template examples/custom-card.json --chat-id oc_xxx
```

### 3. Use in Agent

When Agent needs to send Feishu messages:

```javascript
// Wrong: Send plain text
await message({ 
  action: "send", 
  channel: "feishu", 
  message: "Confirm delete?" 
});

// Right: Send interactive card
await exec({
  command: `node E:\\openclaw\\workspace\\skills\\feishu-interactive-cards\\scripts\\send-card.js confirmation "Confirm delete file test.txt?" --chat-id ${chatId}`
});
```

## Card Templates

See `examples/` directory for complete card templates:
- `confirmation-card.json` - Confirmation dialogs
- `todo-card.json` - Task lists with checkboxes
- `poll-card.json` - Polls and surveys
- `form-card.json` - Forms with input fields

For detailed card design patterns and best practices, see [references/card-design-guide.md](references/card-design-guide.md).

## Callback Handling

Callback server automatically sends all card interactions to OpenClaw Gateway. For detailed integration guide, see [references/gateway-integration.md](references/gateway-integration.md).

**Quick example:**

```javascript
// Handle confirmation
if (callback.data.action.value.action === "confirm") {
  const file = callback.data.action.value.file;
  
  // ⚠️ SECURITY: Validate and sanitize file path before use
  // Use OpenClaw's built-in file operations instead of shell commands
  const fs = require('fs').promises;
  const path = require('path');
  
  try {
    // Validate file path (prevent directory traversal)
    const safePath = path.resolve(file);
    if (!safePath.startsWith(process.cwd())) {
      throw new Error('Invalid file path');
    }
    
    // Use fs API instead of shell command
    await fs.unlink(safePath);
    
    // Update card
    await updateCard(callback.context.open_message_id, {
      header: { title: "Done", template: "green" },
      elements: [
        { tag: "div", text: { content: `File ${path.basename(safePath)} deleted`, tag: "lark_md" } }
      ]
    });
  } catch (error) {
    // Handle error
    await updateCard(callback.context.open_message_id, {
      header: { title: "Error", template: "red" },
      elements: [
        { tag: "div", text: { content: `Failed to delete file: ${error.message}`, tag: "lark_md" } }
      ]
    });
  }
}
```

## Best Practices

### Card Design
- Clear titles and content
- Obvious button actions
- Use `danger` type for destructive operations
- Carry complete state in button `value` to avoid extra queries

### Interaction Flow
```
User request -> Agent decides -> Send card -> User clicks button 
-> Callback server -> Gateway -> Agent handles -> Update card/execute
```

### Error Handling
- Timeout: Send reminder if user doesn't respond
- Duplicate clicks: Built-in deduplication (3s window)
- Failures: Update card to show error message

### Performance
- Async processing: Quick response, long tasks in background
- Batch operations: Combine related actions in one card

## Configuration

Configure in `~/.openclaw/openclaw.json`:

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "main": {
          "appId": "YOUR_APP_ID",
          "appSecret": "YOUR_APP_SECRET"
        }
      }
    }
  },
  "gateway": {
    "enabled": true,
    "port": 18789,
    "token": "YOUR_GATEWAY_TOKEN"
  }
}
```

Callback server reads config automatically.

## Troubleshooting

**Button clicks not working:**
- Check callback server is running
- Verify Feishu backend uses "long-polling" mode
- Ensure `card.action.trigger` event is subscribed

**Gateway not receiving callbacks:**
- Start Gateway: `E:\openclaw\workspace\scripts\gateway.cmd`
- Check token in `~/.openclaw\openclaw.json`

**Card display issues:**
- Use provided templates as base
- Validate JSON format
- Check required fields

## Security

**⚠️ CRITICAL: Never pass user input directly to shell commands!**

This skill includes comprehensive security guidelines. Please read [references/security-best-practices.md](references/security-best-practices.md) before implementing callback handlers.

Key security principles:
- Always validate and sanitize user input
- Use Node.js built-in APIs instead of shell commands
- Implement proper permission checks
- Prevent command injection vulnerabilities
- Use event_id for deduplication

## References

- [Security Best Practices](references/security-best-practices.md) - **READ THIS FIRST!**
- [Feishu Card Documentation](https://open.feishu.cn/document/ukTMukTMukTM/uczM3QjL3MzN04yNzcDN)
- [OpenClaw Docs](https://docs.openclaw.ai)
