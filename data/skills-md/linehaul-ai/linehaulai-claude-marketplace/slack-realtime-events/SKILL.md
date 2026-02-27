---
name: slack-realtime-events
description: Real-time event handling with Socket Mode and Events API. Use when building interactive Slack bots, handling message events, app mentions, reactions, button clicks, modal submissions, slash commands, or any event-driven Slack application functionality.
keywords: [slack, socket-mode, events-api, real-time, webhooks]
---

# Slack Real-time Events

## Socket Mode vs Events API

### Socket Mode (WebSocket)
**Use when**:
- App runs behind a firewall
- No public HTTPS endpoint available
- Development and testing
- Running on localhost

```go
import "github.com/slack-go/slack/socketmode"

client := socketmode.New(
    api,
    socketmode.OptionDebug(true),
)
```

See [socket-mode-setup.md](../../references/socket-mode-setup.md) for complete Socket Mode implementation.

### Events API (HTTP Webhooks)
**Use when**:
- Public HTTPS endpoint available
- Production cloud deployments
- Webhook-based architecture preferred

See [events-api-webhooks.md](../../references/events-api-webhooks.md) for HTTP webhook patterns.

## Socket Mode Basic Setup

```go
api := slack.New(
    os.Getenv("SLACK_BOT_TOKEN"),
    slack.OptionAppLevelToken(os.Getenv("SLACK_APP_TOKEN")),
)

client := socketmode.New(api)

go func() {
    for envelope := range client.Events {
        switch envelope.Type {
        case socketmode.EventTypeEventsAPI:
            client.Ack(*envelope.Request)
            // Handle event
        }
    }
}()

client.Run()
```

## Event Handling Patterns

### Message Events

```go
func handleMessageEvent(event *slackevents.MessageEvent, api *slack.Client) {
    // Ignore bot messages
    if event.BotID != "" {
        return
    }

    fmt.Printf("Message from %s in %s: %s\n", event.User, event.Channel, event.Text)

    // Respond
    api.PostMessage(event.Channel, slack.MsgOptionText("Got your message!", false))
}
```

### App Mention Events

```go
func handleAppMention(event *slackevents.AppMentionEvent, api *slack.Client) {
    text := strings.TrimSpace(strings.Replace(event.Text, fmt.Sprintf("<@%s>", botUserID), "", 1))

    response := processCommand(text)

    api.PostMessage(
        event.Channel,
        slack.MsgOptionText(response, false),
        slack.MsgOptionTS(event.TimeStamp), // Reply in thread
    )
}
```

### Reaction Events

```go
func handleReaction(event *slackevents.ReactionAddedEvent, api *slack.Client) {
    fmt.Printf("User %s added reaction :%s: to message %s\n",
        event.User, event.Reaction, event.Item.Timestamp)

    // React back
    api.AddReaction(event.Reaction, slack.ItemRef{
        Channel:   event.Item.Channel,
        Timestamp: event.Item.Timestamp,
    })
}
```

## Interactive Components

### Button Clicks

```go
func handleButtonClick(interaction slack.InteractionCallback, api *slack.Client) {
    action := interaction.ActionCallback.BlockActions[0]

    switch action.ActionID {
    case "approve_deployment":
        // Handle approval
        updateMessage(api, interaction.Channel.ID, interaction.Message.Timestamp, "Approved!")

    case "reject_deployment":
        // Handle rejection
        updateMessage(api, interaction.Channel.ID, interaction.Message.Timestamp, "Rejected!")
    }
}
```

### Modal Submissions

```go
func handleModalSubmission(interaction slack.InteractionCallback, api *slack.Client) {
    values := interaction.View.State.Values

    // Extract form data
    rating := values["rating_block"]["rating_select"].SelectedOption.Value
    comments := values["comments_block"]["comments_input"].Value

    // Process submission
    fmt.Printf("Feedback: %s stars - %s\n", rating, comments)

    // Acknowledge
    api.UpdateView(slack.View{}, interaction.View.ExternalID, "", interaction.View.ID)
}
```

See [interactive-components.md](../../references/interactive-components.md) for comprehensive interactive patterns.

## Slash Commands

Handle slash command invocations:

```go
func handleSlashCommand(command slack.SlashCommand, api *slack.Client) slack.Message {
    switch command.Command {
    case "/deploy":
        return slack.Message{
            Text: fmt.Sprintf("Deploying %s to %s...", command.Text, "production"),
        }

    case "/status":
        return slack.Message{
            Text: "All systems operational",
        }

    default:
        return slack.Message{
            Text: "Unknown command",
        }
    }
}
```

See [slash-commands.md](../../references/slash-commands.md) for command patterns and delayed responses.

## Event Types

Common event types to handle:

- **message** - New messages in channels
- **app_mention** - Bot mentioned in message
- **reaction_added/removed** - Message reactions
- **channel_created/renamed** - Channel lifecycle
- **team_join** - New workspace members
- **user_change** - User profile updates

See [event-types.md](../../references/event-types.md) for comprehensive event catalog.

## Connection Management

### Graceful Shutdown

```go
ctx, cancel := context.WithCancel(context.Background())
defer cancel()

go func() {
    sigChan := make(chan os.Signal, 1)
    signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)
    <-sigChan
    cancel()
}()

client.RunContext(ctx)
```

### Error Handling

```go
for envelope := range client.Events {
    switch envelope.Type {
    case socketmode.EventTypeErrorBadMessage:
        fmt.Printf("Error: Bad message - %v\n", envelope.Request)

    case socketmode.EventTypeConnectionError:
        fmt.Printf("Connection error: %v\n", envelope.Request)
    }
}
```

## Common Pitfalls

- Not acknowledging events (causes timeouts)
- Blocking in event handlers (use goroutines for long operations)
- Missing bot vs user message filtering
- Not handling reconnections in Socket Mode
- Forgetting to verify request signatures in Events API
