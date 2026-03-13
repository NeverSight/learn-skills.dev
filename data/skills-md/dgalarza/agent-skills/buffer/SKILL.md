---
name: buffer
description: This skill should be used when interfacing with the Buffer social media scheduling API. It handles scheduling social media posts, checking the queue, listing channels, creating ideas, and managing Buffer accounts.
allowed-tools: Bash(curl:*), Bash(cat:*), Bash(jq:*)
---

# Buffer Social Media Scheduling

## Setup

Requires a `BUFFER_API_TOKEN` environment variable. Generate one at:
https://publish.buffer.com/settings/api

Verify the token is set before making any API calls:

```bash
if [ -z "$BUFFER_API_TOKEN" ]; then
  echo "Error: BUFFER_API_TOKEN is not set. Get your token at https://publish.buffer.com/settings/api"
  exit 1
fi
```

## API Configuration

- **Endpoint:** `https://api.buffer.com`
- **Method:** POST (all requests are GraphQL)
- **Content-Type:** `application/json`
- **Auth:** `Authorization: Bearer $BUFFER_API_TOKEN`
- **User-Agent:** `Mozilla/5.0` — required to avoid Cloudflare 403 blocks

### Curl Template

All API calls follow this pattern:

```bash
curl -s -X POST https://api.buffer.com \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BUFFER_API_TOKEN" \
  -H "User-Agent: Mozilla/5.0" \
  -d '{"query": "<GRAPHQL_QUERY>", "variables": <VARIABLES_JSON>}'
```

Always pipe through `jq` for readable output. Use `jq -e` to detect errors.

**Important:** For queries with GraphQL variables (e.g. `$input`), the shell may expand `$input` even inside single quotes. Use a temp file with `-d @file` to avoid this:

```bash
cat > /tmp/buffer_payload.json << 'EOF'
{"query": "<GRAPHQL_QUERY>", "variables": <VARIABLES_JSON>}
EOF

curl -s -X POST https://api.buffer.com \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BUFFER_API_TOKEN" \
  -H "User-Agent: Mozilla/5.0" \
  -d @/tmp/buffer_payload.json | jq .
```

Simple queries without variables can use inline `-d` directly.

## Mode Detection

Parse the user's intent to determine which operation to perform:

| Intent | Mode | Example |
|--------|------|---------|
| List organizations | `organizations` | "Show my Buffer organizations" |
| List channels | `channels` | "What channels do I have?" |
| View posts | `posts` | "Show my scheduled posts" |
| Create a text post | `create-post` | "Schedule a tweet saying..." |
| Create an image post | `create-post` | "Post this image to Instagram" |
| Save an idea | `create-idea` | "Save an idea about..." |
| Account info | `account` | "Show my Buffer account" |

Most operations require an `organizationId`. If the user hasn't specified one, fetch organizations first. If only one org exists, use it automatically.

## Mode: Get Organizations

Fetch the user's organizations. This is typically the first call needed.

```bash
curl -s -X POST https://api.buffer.com \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BUFFER_API_TOKEN" \
  -H "User-Agent: Mozilla/5.0" \
  -d '{"query": "{ account { organizations { id name ownerEmail } } }"}' | jq .
```

Store the `organizationId` from the response for subsequent calls.

## Mode: Get Channels

List channels (social media accounts) for an organization.

```bash
cat > /tmp/buffer_payload.json << 'EOF'
{"query": "query GetChannels($input: ChannelsInput!) { channels(input: $input) { id name displayName service avatar isQueuePaused } }", "variables": {"input": {"organizationId": "<ORG_ID>"}}}
EOF
curl -s -X POST https://api.buffer.com \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BUFFER_API_TOKEN" \
  -H "User-Agent: Mozilla/5.0" \
  -d @/tmp/buffer_payload.json | jq .
```

Display results in a readable format showing channel name, service (e.g., twitter, instagram, linkedin), and queue status.

## Mode: Get Posts

Query posts with filtering, sorting, and pagination.

```bash
cat > /tmp/buffer_payload.json << 'EOF'
{"query": "query GetPosts($input: PostsInput!) { posts(input: $input) { edges { node { id text status dueAt sentAt createdAt channelService externalLink } cursor } pageInfo { hasNextPage endCursor } totalCount } }", "variables": {"input": {"organizationId": "<ORG_ID>", "filter": {"status": "scheduled"}, "sort": {"field": "dueAt", "direction": "desc"}}}}
EOF
curl -s -X POST https://api.buffer.com \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BUFFER_API_TOKEN" \
  -H "User-Agent: Mozilla/5.0" \
  -d @/tmp/buffer_payload.json | jq .
```

For available filter fields (status, channelIds, date range), sort options, and pagination details, refer to `references/api-reference.md`.

## Mode: Create Text Post

Create and schedule a text post.

```bash
cat > /tmp/buffer_payload.json << 'EOF'
{"query": "mutation CreatePost($input: CreatePostInput!) { createPost(input: $input) { ... on PostActionSuccess { post { id text status dueAt } } ... on MutationError { message } } }", "variables": {"input": {"channelId": "<CHANNEL_ID>", "text": "<POST_CONTENT>", "schedulingType": "automatic", "mode": "addToQueue"}}}
EOF
curl -s -X POST https://api.buffer.com \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BUFFER_API_TOKEN" \
  -H "User-Agent: Mozilla/5.0" \
  -d @/tmp/buffer_payload.json | jq .
```

### Required Fields

- **channelId** (String!): The channel to post to
- **text** (String!): The post content

### Scheduling Options

- **schedulingType**: `automatic` (Buffer picks time) or `notification` (sends reminder)
- **mode**: Controls when the post is published (e.g., `addToQueue`, `shareNow`, `shareNext`, `customSchedule`, `recommendedTime`)
- **dueAt** (String): ISO 8601 datetime, required when mode is `customSchedule`. Example: `"2026-03-15T14:00:00Z"`

For full field definitions and enum values, refer to `references/api-reference.md`.

### Response Handling

The mutation returns a union type. Always check for both success and error:

```bash
# Check if the response contains an error
result=$(curl -s -X POST https://api.buffer.com -H "User-Agent: Mozilla/5.0" ...)
echo "$result" | jq -e '.data.createPost.message' > /dev/null 2>&1 && {
  echo "Error: $(echo "$result" | jq -r '.data.createPost.message')"
} || {
  echo "$result" | jq '.data.createPost.post'
}
```

## Mode: Create Image Post

Same as text post, but include an `assets` field with image URLs.

```bash
cat > /tmp/buffer_payload.json << 'EOF'
{"query": "mutation CreatePost($input: CreatePostInput!) { createPost(input: $input) { ... on PostActionSuccess { post { id text status dueAt } } ... on MutationError { message } } }", "variables": {"input": {"channelId": "<CHANNEL_ID>", "text": "<POST_CONTENT>", "schedulingType": "automatic", "mode": "addToQueue", "assets": {"images": [{"url": "<IMAGE_URL>"}]}}}}
EOF
curl -s -X POST https://api.buffer.com \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BUFFER_API_TOKEN" \
  -H "User-Agent: Mozilla/5.0" \
  -d @/tmp/buffer_payload.json | jq .
```

Images must be publicly accessible URLs. Multiple images can be included in the `images` array.

## Mode: Create Idea

Save an idea for later use.

```bash
cat > /tmp/buffer_payload.json << 'EOF'
{"query": "mutation CreateIdea($input: CreateIdeaInput!) { createIdea(input: $input) { ... on Idea { id content { title text services } } } }", "variables": {"input": {"organizationId": "<ORG_ID>", "content": {"title": "<IDEA_TITLE>", "text": "<IDEA_BODY>", "services": ["twitter", "linkedin"]}}}}
EOF
curl -s -X POST https://api.buffer.com \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BUFFER_API_TOKEN" \
  -H "User-Agent: Mozilla/5.0" \
  -d @/tmp/buffer_payload.json | jq .
```

For `IdeaContentInput` field details (title, text, services, tags), refer to `references/api-reference.md`.

**Note:** Tags require existing tag objects with `id` and `color` fields — fetch existing tags first before using.

## Mode: Get Account

> **Note:** The full account query (`id`, `name`, `email`, `timezone`) fails with a standard API token scope. Use Get Organizations instead to confirm account identity.

```bash
curl -s -X POST https://api.buffer.com \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BUFFER_API_TOKEN" \
  -H "User-Agent: Mozilla/5.0" \
  -d '{"query": "{ account { organizations { id name ownerEmail } } }"}' | jq .
```

## Common Workflows

### Schedule a Post

Multi-step workflow when the user wants to schedule a post:

1. **Get organizations** → extract `organizationId`
2. **Get channels** → show available channels, let user pick (or match by service name)
3. **Create post** → use selected `channelId` with the post content

If the user specifies a service (e.g., "post to Twitter"), match it against the channel's `service` field.

### Check the Queue

1. **Get organizations** → extract `organizationId`
2. **Get posts** with `filter: { status: "scheduled" }` and `sort: { field: "dueAt", direction: "asc" }`
3. Display posts grouped by date with channel info

### Brainstorm and Save Ideas

1. **Get organizations** → extract `organizationId`
2. Help the user draft idea content
3. **Create idea** with title, text, tags, and target services

## Schema Introspection

Before attempting a mutation or querying a field you're unsure about, introspect the schema first. Don't guess — the API surface is limited.

**List all available mutations:**

```bash
curl -s -X POST https://api.buffer.com \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BUFFER_API_TOKEN" \
  -H "User-Agent: Mozilla/5.0" \
  -d '{"query": "{ __schema { mutationType { fields { name } } } }"}' | jq '[.data.__schema.mutationType.fields[].name]'
```

**List all available queries:**

```bash
curl -s -X POST https://api.buffer.com \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BUFFER_API_TOKEN" \
  -H "User-Agent: Mozilla/5.0" \
  -d '{"query": "{ __schema { queryType { fields { name } } } }"}' | jq '[.data.__schema.queryType.fields[].name]'
```

**Inspect fields on a specific type:**

```bash
curl -s -X POST https://api.buffer.com \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BUFFER_API_TOKEN" \
  -H "User-Agent: Mozilla/5.0" \
  -d '{"query": "{ __type(name: \"<TYPE_NAME>\") { fields { name type { name kind } } } }"}' | jq '.data.__type.fields[]'
```

## Error Handling

### GraphQL Errors

Check for the top-level `errors` array in every response:

```bash
result=$(curl -s -X POST https://api.buffer.com ...)
errors=$(echo "$result" | jq -r '.errors // empty')
if [ -n "$errors" ]; then
  echo "GraphQL Error:"
  echo "$result" | jq '.errors[].message'
  exit 1
fi
```

### Mutation Errors

Mutations return union types. Always handle the `MutationError` variant:

```json
{
  "data": {
    "createPost": {
      "message": "Validation failed: text is required"
    }
  }
}
```

### Common Issues

- **403 Forbidden (error code 1010)**: Cloudflare is blocking the request. Always include `-H "User-Agent: Mozilla/5.0"` in every curl call.
- **401 Unauthorized**: Token is invalid or expired. Regenerate at https://publish.buffer.com/settings/api
- **Missing organizationId**: Most queries require an org ID. Fetch organizations first.
- **Invalid channelId**: Verify the channel exists and belongs to the current organization.
- **Past dueAt**: When using `customSchedule`, the `dueAt` must be in the future.
