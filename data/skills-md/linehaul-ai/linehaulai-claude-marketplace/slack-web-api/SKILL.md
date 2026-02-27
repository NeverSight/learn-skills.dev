---
name: slack-web-api
description: Comprehensive guidance for Slack Web API operations with the Go SDK. Use when sending messages, posting to channels, creating or managing channels, retrieving user information, uploading files, composing Block Kit messages, or performing any synchronous Slack API operations.
keywords: [slack, web-api, messaging, channels, file-uploads]
---

# Slack Web API

## Core API Pattern

All Web API methods follow this pattern:

```go
result, err := api.MethodName(params...)
if err != nil {
    // Handle error (rate limits, permissions, etc.)
    return err
}
// Use result
```

## Messaging Operations

### Send Simple Text Message

```go
channelID := "C1234567890"
text := "Hello, Slack!"

_, _, err := api.PostMessage(
    channelID,
    slack.MsgOptionText(text, false),
)
```

### Send Message with Block Kit

```go
headerText := slack.NewTextBlockObject("mrkdwn", "*Deployment Complete*", false, false)
headerBlock := slack.NewSectionBlock(headerText, nil, nil)

divider := slack.NewDividerBlock()

bodyText := slack.NewTextBlockObject("mrkdwn", "Version 2.1.0 deployed successfully", false, false)
bodyBlock := slack.NewSectionBlock(bodyText, nil, nil)

_, _, err := api.PostMessage(
    channelID,
    slack.MsgOptionBlocks(headerBlock, divider, bodyBlock),
)
```

See [web-api-messaging.md](../../references/web-api-messaging.md) for comprehensive messaging patterns including threading, updates, and ephemeral messages.

## Channel Operations

### Create a Channel

```go
channelName := "project-updates"
isPrivate := false

channel, err := api.CreateConversation(channelName, isPrivate)
if err != nil {
    return err
}
fmt.Printf("Created channel: %s (ID: %s)\n", channel.Name, channel.ID)
```

### List Channels

```go
params := &slack.GetConversationsParameters{
    Types: []string{"public_channel"},
    Limit: 100,
}

channels, nextCursor, err := api.GetConversations(params)
```

See [web-api-channels.md](../../references/web-api-channels.md) for channel management, invites, and metadata operations.

## User Operations

### Get User Information

```go
user, err := api.GetUserInfo("U1234567890")
if err != nil {
    return err
}

fmt.Printf("User: %s (%s)\n", user.Profile.RealName, user.Profile.Email)
```

### List All Users

```go
users, err := api.GetUsers()
if err != nil {
    return err
}

for _, user := range users {
    fmt.Printf("- %s (%s)\n", user.Name, user.ID)
}
```

See [web-api-users.md](../../references/web-api-users.md) for user presence, profiles, and groups.

## File Operations

### Upload a File

```go
params := slack.FileUploadParameters{
    File:     "report.pdf",
    Channels: []string{"C1234567890"},
    Title:    "Monthly Report",
}

file, err := api.UploadFile(params)
if err != nil {
    return err
}
```

See [web-api-files.md](../../references/web-api-files.md) for file downloads, sharing, and multi-part uploads.

## Block Kit Integration

Block Kit allows rich, interactive messages. See [block-kit-integration.md](../../references/block-kit-integration.md) for:
- Section blocks with text, images, and accessories
- Interactive buttons and select menus
- Input blocks for forms
- Complete layout patterns

## Error Handling

### Rate Limiting

```go
_, _, err := api.PostMessage(channelID, slack.MsgOptionText(text, false))
if err != nil {
    if rateLimitErr, ok := err.(*slack.RateLimitedError); ok {
        time.Sleep(rateLimitErr.RetryAfter)
        // Retry operation
    }
    return err
}
```

### Common Error Types

- `slack.RateLimitedError` - Too many requests
- Permission errors - Missing scopes
- `channel_not_found` - Invalid channel ID
- `invalid_auth` - Token issues

## Pagination

For operations returning large result sets, use cursor-based pagination:

```go
cursor := ""
for {
    params := &slack.GetConversationsParameters{
        Cursor: cursor,
        Limit:  100,
    }

    channels, nextCursor, err := api.GetConversations(params)
    if err != nil {
        return err
    }

    // Process channels...

    if nextCursor == "" {
        break
    }
    cursor = nextCursor
}
```

See [pagination-patterns.md](../../references/pagination-patterns.md) for advanced pagination strategies.

## Common Pitfalls

- Not handling rate limits (use exponential backoff)
- Hardcoding channel/user IDs (use lookups or environment variables)
- Forgetting to escape user input in messages
- Not validating Bot Token scopes match required permissions
- Using blocking operations in high-throughput scenarios
