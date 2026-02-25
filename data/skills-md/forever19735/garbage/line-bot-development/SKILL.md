---
name: line-bot-development
description: Build and maintain LINE messaging API integrations, handle webhook events, and implement bot commands
---

## When to use this skill

Use this skill when you need to:
- Develop or modify LINE Bot webhook handlers
- Implement new bot commands and message responses
- Handle LINE events (messages, join/leave groups)
- Integrate LINE Messaging API features
- Debug LINE Bot webhook issues
- Test bot functionality in LINE groups

## How to use it

### Core Components

#### 1. LINE Bot SDK Setup
Use the LINE Bot SDK v3 for Python:
```python
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient
from linebot.v3.webhook import WebhookHandler, MessageEvent
from linebot.v3.messaging.models import PushMessageRequest, TextMessage
from linebot.v3.webhooks import TextMessageContent, JoinEvent, LeaveEvent
```

#### 2. Environment Configuration
Required environment variables:
- `LINE_CHANNEL_ACCESS_TOKEN` - Bot access token from LINE Developers Console
- `LINE_CHANNEL_SECRET` - Channel secret for webhook verification
- `LINE_GROUP_ID` (optional) - Comma-separated group IDs for broadcasting

#### 3. Webhook Handler Pattern
```python
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except Exception as e:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # Process user messages
    pass

@handler.add(JoinEvent)
def handle_join(event):
    # Handle bot joining a group
    pass

@handler.add(LeaveEvent)
def handle_leave(event):
    # Handle bot leaving a group
    pass
```

#### 4. Message Sending
```python
# Reply to user message
messaging_api.reply_message(
    ReplyMessageRequest(
        reply_token=event.reply_token,
        messages=[TextMessage(text="Response text")]
    )
)

# Push message to group
messaging_api.push_message(
    PushMessageRequest(
        to=group_id,
        messages=[TextMessage(text="Broadcast message")]
    )
)
```

#### 5. Command Pattern
Implement commands with `@` prefix:
```python
def handle_message(event):
    text = event.message.text.strip()
    
    if text.startswith('@'):
        parts = text[1:].split()
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        if command == 'help':
            # Show help
        elif command == 'schedule':
            # Show schedule
        # ... more commands
```

### Best Practices

1. **Group Context Awareness**
   - Always extract `group_id` from events
   - Store per-group configurations separately
   - Validate group permissions before operations

2. **Error Handling**
   - Wrap webhook handlers in try-except blocks
   - Log errors for debugging
   - Send user-friendly error messages back to LINE

3. **Message Formatting**
   - Use emojis to enhance UX (🗑️, 📅, 👥, etc.)
   - Keep messages concise and scannable
   - Use line breaks for readability

4. **Testing**
   - Test commands in a dedicated LINE group
   - Verify webhook signature validation
   - Check response times (should be quick)

### Common Patterns

#### Multi-Group Support
```python
# Get group ID from event
group_id = event.source.group_id if hasattr(event.source, 'group_id') else None

# Load group-specific data
group_data = groups.get(group_id, {})
```

#### Scheduled Broadcasting
```python
from apscheduler.schedulers.background import BackgroundScheduler

def send_reminder(group_id):
    # Get group-specific schedule
    # Send reminder message
    pass

scheduler = BackgroundScheduler()
scheduler.start()
```

### Reference Links

- [LINE Developers Console](https://developers.line.biz/)
- [LINE Messaging API Documentation](https://developers.line.biz/en/docs/messaging-api/)
- [LINE Bot SDK for Python](https://github.com/line/line-bot-sdk-python)
