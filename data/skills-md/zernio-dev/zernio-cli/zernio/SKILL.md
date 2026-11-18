---
name: zernio
description: Schedule posts, manage inbox, broadcasts, sequences, and automations across 14 platforms from the CLI
version: 0.2.0
homepage: https://docs.zernio.com
tags: [social-media, scheduling, instagram, tiktok, twitter, linkedin, facebook, threads, youtube, bluesky, pinterest, reddit, snapchat, telegram]
metadata:
  env:
    - ZERNIO_API_KEY (required) - Your Zernio API key from https://zernio.com/settings/api
    - ZERNIO_API_URL (optional) - Defaults to https://zernio.com/api
---

# Zernio CLI

Schedule and publish social media posts across 13 platforms (Instagram, TikTok, X/Twitter, LinkedIn, Facebook, Threads, YouTube, Bluesky, Pinterest, Reddit, Snapchat, Telegram, Google Business) from any terminal or AI agent.

## Setup

```bash
npm install -g @zernio/cli

# Log in via browser (recommended)
zernio auth:login

# Or set your API key manually
zernio auth:set --key "sk_your-api-key"

# Verify it works
zernio auth:check
```

Or set the env var directly: `export ZERNIO_API_KEY="sk_your-api-key"`

## Core Workflow

The typical flow for scheduling a post:

```bash
# 1. See your profiles
zernio profiles:list

# 2. See connected social accounts
zernio accounts:list

# 3. Schedule a post
zernio posts:create --text "Hello world!" --accounts <accountId1>,<accountId2> --scheduledAt "2025-01-15T10:00:00Z"

# 4. Check post status
zernio posts:list --status scheduled

# 5. View analytics (requires analytics add-on)
zernio analytics:posts --profileId <profileId>
```

## Output Format

All commands output JSON by default (for AI agents and piping). Add `--pretty` for indented output.

Errors always return: `{"error": true, "message": "...", "status": 401}`

## Commands Reference

### Authentication

```bash
# Log in via browser (opens browser, creates API key automatically)
zernio auth:login

# Or with a custom device name
zernio auth:login --device-name "my-server"

# Save API key manually
zernio auth:set --key "sk_your-api-key"

# Optionally set custom API URL
zernio auth:set --key "sk_..." --url "https://custom.api.url/api/v1"

# Verify key works
zernio auth:check
```

### Profiles

```bash
# List all profiles
zernio profiles:list

# Create a profile
zernio profiles:create --name "My Brand"

# Get profile details
zernio profiles:get <profileId>

# Update profile
zernio profiles:update <profileId> --name "New Name"

# Delete profile (must have no connected accounts)
zernio profiles:delete <profileId>
```

### Accounts (Social Media Connections)

```bash
# List all connected accounts
zernio accounts:list

# Filter by profile or platform
zernio accounts:list --profileId <id> --platform instagram

# Get single account
zernio accounts:get <accountId>

# Check health of all accounts (rate limits, token expiry)
zernio accounts:health
```

### Posts

```bash
# Publish immediately
zernio posts:create --text "Hello!" --accounts <id1>,<id2>

# Schedule for later
zernio posts:create --text "Scheduled post" --accounts <id> --scheduledAt "2025-06-01T14:00:00Z"

# Save as draft
zernio posts:create --text "Draft idea" --accounts <id> --draft

# With media
zernio posts:create --text "Check this out" --accounts <id> --media "https://example.com/image.jpg"

# With title (YouTube, Reddit)
zernio posts:create --text "Description" --accounts <id> --title "My Video Title"

# List posts with filters
zernio posts:list --status published --page 1 --limit 20
zernio posts:list --profileId <id> --from "2025-01-01" --to "2025-01-31"
zernio posts:list --search "product launch"

# Get post details
zernio posts:get <postId>

# Delete a post
zernio posts:delete <postId>

# Retry a failed post
zernio posts:retry <postId>
```

### Analytics (requires analytics add-on)

```bash
# Post analytics
zernio analytics:posts --profileId <id>
zernio analytics:posts --postId <postId>
zernio analytics:posts --platform instagram --sortBy engagement

# Daily metrics
zernio analytics:daily --accountId <id> --from "2025-01-01" --to "2025-01-31"

# Best posting times
zernio analytics:best-time --accountId <id>
```

### Media

```bash
# Upload a file (returns URL for use in posts:create --media)
zernio media:upload ./photo.jpg
zernio media:upload ./video.mp4
```

## Platform-Specific Examples

### Instagram Reel
```bash
zernio media:upload ./reel.mp4
# Use the returned URL:
zernio posts:create --text "New reel!" --accounts <instagramAccountId> --media "<returned-url>"
```

### Multi-Platform Post
```bash
zernio posts:create \
  --text "Big announcement!" \
  --accounts <instagramId>,<twitterId>,<linkedinId> \
  --media "https://example.com/image.jpg" \
  --scheduledAt "2025-06-01T09:00:00Z" \
  --timezone "America/New_York"
```

### Threads + Twitter Simultaneous
```bash
zernio posts:create --text "Thoughts on AI agents..." --accounts <threadsId>,<twitterId>
```

## Supported Platforms

Instagram, TikTok, X (Twitter), LinkedIn, Facebook, Threads, YouTube, Bluesky, Pinterest, Reddit, Snapchat, Telegram, Google Business Profile.

## Error Handling

Common errors and their meaning:
- `401` - Invalid or missing API key
- `402` - Feature requires paid add-on (e.g., analytics)
- `403` - Plan limit reached or insufficient permissions
- `404` - Resource not found
- `429` - Rate limited (account in cooldown)

### Inbox (DMs, Comments, Reviews)

```bash
# List DM conversations
zernio inbox:conversations --platform instagram
zernio inbox:conversations --accountId <id> --status active

# Read messages in a conversation
zernio inbox:messages <conversationId> --accountId <id>

# Send a DM
zernio inbox:send <conversationId> --accountId <id> --message "Thanks for reaching out!"

# List comments across posts
zernio inbox:comments --platform instagram --since "2025-01-01"

# Get comments on a specific post
zernio inbox:post-comments <postId> --accountId <id>

# Reply to a comment
zernio inbox:reply <postId> --accountId <id> --message "Thank you!"

# Reply to a specific comment (not the post)
zernio inbox:reply <postId> --accountId <id> --message "Great point" --commentId <commentId>

# List reviews (Facebook, Google Business)
zernio inbox:reviews --minRating 1 --maxRating 3 --hasReply false

# Reply to a review
zernio inbox:review-reply <reviewId> --accountId <id> --message "Thanks for your feedback!"
```

### Contacts

```bash
# List contacts
zernio contacts:list --profileId <id>
zernio contacts:list --search "john" --tag vip --platform instagram

# Create a contact
zernio contacts:create --profileId <id> --accountId <id> --platform instagram --platformUserId <userId> --name "John Doe" --tags "vip,lead"

# Get/update/delete
zernio contacts:get <contactId>
zernio contacts:update <contactId> --name "Jane Doe" --tags "vip,customer"
zernio contacts:delete <contactId>

# List channels (platforms) for a contact
zernio contacts:channels <contactId>

# Custom fields
zernio contacts:set-field <contactId> <slug> --value "some value"
zernio contacts:clear-field <contactId> <slug>

# Bulk create from JSON file (up to 1000)
zernio contacts:bulk-create --profileId <id> --accountId <id> --platform instagram --file ./contacts.json
```

### Broadcasts

```bash
# List broadcasts
zernio broadcasts:list --profileId <id> --status draft

# Create a broadcast draft (generic message)
zernio broadcasts:create --profileId <id> --accountId <id> --platform instagram --name "Summer Sale" --message "Check out our summer deals!"

# Create a WhatsApp broadcast with template
zernio broadcasts:create --profileId <id> --accountId <id> --platform whatsapp --name "Order Update" --templateName "order_confirmation" --templateLanguage "en"

# Add recipients
zernio broadcasts:add-recipients <broadcastId> --contactIds <id1>,<id2>,<id3>
zernio broadcasts:add-recipients <broadcastId> --useSegment

# Send immediately or schedule
zernio broadcasts:send <broadcastId>
zernio broadcasts:schedule <broadcastId> --scheduledAt "2025-06-01T10:00:00Z"

# Check delivery status
zernio broadcasts:get <broadcastId>
zernio broadcasts:recipients <broadcastId> --status delivered

# Cancel
zernio broadcasts:cancel <broadcastId>
```

### Sequences (Drip Campaigns)

```bash
# List sequences
zernio sequences:list --profileId <id> --status active

# Create a sequence (steps defined in JSON file)
zernio sequences:create --profileId <id> --accountId <id> --platform instagram --name "Welcome Series" --stepsFile ./steps.json

# steps.json example:
# [
#   {"order": 1, "delayMinutes": 0, "message": "Welcome! Thanks for connecting."},
#   {"order": 2, "delayMinutes": 1440, "message": "Here are some tips to get started..."},
#   {"order": 3, "delayMinutes": 4320, "message": "Check out our latest content!"}
# ]

# Activate/pause
zernio sequences:activate <sequenceId>
zernio sequences:pause <sequenceId>

# Enroll contacts
zernio sequences:enroll <sequenceId> --contactIds <id1>,<id2>

# Check enrollments
zernio sequences:enrollments <sequenceId> --status active

# Unenroll a contact
zernio sequences:unenroll <sequenceId> <contactId>
```

### Comment-to-DM Automations

```bash
# List automations
zernio automations:list --profileId <id>

# Create: auto-DM anyone who comments "info" on a post
zernio automations:create \
  --profileId <id> --accountId <id> \
  --platformPostId <igPostId> \
  --name "Lead Magnet" \
  --keywords "info,details,link" \
  --dmMessage "Here's the link you asked for: https://example.com" \
  --commentReply "Check your DMs!"

# Trigger on ALL comments (no keywords filter)
zernio automations:create \
  --profileId <id> --accountId <id> \
  --platformPostId <igPostId> \
  --name "Engagement Boost" \
  --dmMessage "Thanks for engaging! Here's a special offer..."

# Update
zernio automations:update <automationId> --isActive false
zernio automations:update <automationId> --keywords "buy,order" --matchMode exact

# View trigger logs
zernio automations:logs <automationId> --status sent
zernio automations:logs <automationId> --status failed

# Delete
zernio automations:delete <automationId>
```

## Tips for AI Agents

- Always call `zernio accounts:list` first to get valid account IDs before creating posts
- Use `zernio accounts:health` to check if accounts are rate-limited before posting
- Post IDs from `zernio posts:create` can be used with `zernio posts:get` to check publish status
- For multi-image posts, upload each file with `zernio media:upload` first, then pass all URLs comma-separated to `--media`
- Schedule posts at least 5 minutes in the future for reliable delivery
- For inbox commands, you always need an `--accountId` to specify which social account to use
- Broadcasts and sequences work across all inbox platforms (Instagram, Facebook, Telegram, X, WhatsApp, Bluesky, Reddit)
- Comment-to-DM automations currently support Instagram and Facebook
- Use `zernio contacts:list` to get contact IDs before enrolling in sequences or adding to broadcasts
