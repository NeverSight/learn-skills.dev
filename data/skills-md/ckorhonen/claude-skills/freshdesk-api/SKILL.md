---
name: freshdesk-api
description: Expert in Freshdesk helpdesk API for building integrations, extracting support data, managing tickets/contacts/companies, and automating support workflows. Use when working with Freshdesk, building helpdesk integrations, analyzing support ticket data, or creating customer support applications.
---

# Freshdesk API

## Overview

Build integrations with Freshdesk's helpdesk platform using their REST API v2. Manage support tickets, contacts, companies, agents, and automate workflows. The API supports full CRUD operations on all major resources with filtering, pagination, and embedded data.

## When to Use

- Building helpdesk integrations or support dashboards
- Extracting and analyzing support ticket data
- Automating ticket routing, assignment, or updates
- Syncing contacts/companies with CRM systems
- Creating custom reporting on support metrics
- Implementing chatbots or AI-powered support tools
- Migrating data to/from Freshdesk

## Prerequisites

### API Key Setup

1. Log into Freshdesk as an Admin
2. Click your profile picture → **Profile Settings**
3. Find your **API Key** on the right sidebar
4. Store securely (never commit to version control)

```bash
# Set environment variable
export FRESHDESK_API_KEY="your-api-key-here"
export FRESHDESK_DOMAIN="yourcompany"  # From yourcompany.freshdesk.com
```

### Required Tools

- `curl` for HTTP requests
- `jq` for JSON parsing (`brew install jq` on macOS)
- For SDKs: Python 3.6+, Node.js 14+, or Ruby 2.7+

## API Base URL

```
https://{domain}.freshdesk.com/api/v2/
```

Replace `{domain}` with your Freshdesk subdomain (e.g., `acme` for `acme.freshdesk.com`).

## Authentication

Freshdesk uses HTTP Basic Authentication with your API key as the username and `X` as the password.

### curl Example

```bash
# Using -u flag (username:password)
curl -u "$FRESHDESK_API_KEY:X" \
  "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/tickets"

# Using Authorization header
curl -H "Authorization: Basic $(echo -n "$FRESHDESK_API_KEY:X" | base64)" \
  "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/tickets"
```

### Headers

Always include:

```
Content-Type: application/json
```

## Quick Start

### Get All Tickets

```bash
curl -u "$FRESHDESK_API_KEY:X" \
  -H "Content-Type: application/json" \
  "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/tickets"
```

### Create a Ticket

```bash
curl -u "$FRESHDESK_API_KEY:X" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{
    "subject": "Support needed",
    "description": "Details of the issue...",
    "email": "customer@example.com",
    "priority": 2,
    "status": 2
  }' \
  "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/tickets"
```

### Get a Contact

```bash
curl -u "$FRESHDESK_API_KEY:X" \
  "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/contacts/12345"
```

### Search Tickets

```bash
# Search by status and priority
curl -u "$FRESHDESK_API_KEY:X" \
  "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/search/tickets?query=\"status:2 AND priority:3\""
```

## Core Endpoints

| Endpoint | Description |
|----------|-------------|
| `/tickets` | Create, list, update, delete tickets |
| `/contacts` | Manage customer contacts |
| `/companies` | Manage company/organization records |
| `/agents` | View and manage support agents |
| `/groups` | Manage agent groups |
| `/conversations` | Ticket replies, notes, forwards |
| `/time_entries` | Time tracking on tickets |
| `/surveys/satisfaction_ratings` | Customer satisfaction data |
| `/products` | Product catalog management |
| `/business_hours` | Business hours configuration |
| `/email_configs` | Email settings |
| `/sla_policies` | SLA policy management |
| `/canned_responses` | Pre-defined response templates |
| `/ticket_fields` | Custom ticket fields |

See [references/tickets-api.md](references/tickets-api.md) for detailed ticket operations.
See [references/contacts-companies.md](references/contacts-companies.md) for contact/company management.

## Rate Limits

### Limits by API Version

| Version | Limit |
|---------|-------|
| API v1 | 1000 calls/hour |
| API v2 | Per-minute, plan-based |
| Trial Plans | 50 calls/minute |

### Rate Limit Headers

Every response includes:

| Header | Description |
|--------|-------------|
| `X-Ratelimit-Total` | Total calls allowed per minute |
| `X-Ratelimit-Remaining` | Calls remaining this minute |
| `X-Ratelimit-Used-CurrentRequest` | Credits used by this request |

### Handling Rate Limits

```bash
#!/usr/bin/env bash
# Retry with exponential backoff for 429 errors

max_retries=3
retry_count=0

while [ "$retry_count" -lt "$max_retries" ]; do
  response=$(curl -s -w "\n%{http_code}" -u "$FRESHDESK_API_KEY:X" \
    "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/tickets")

  http_code=$(echo "$response" | tail -1)
  body=$(echo "$response" | sed '$d')

  if [ "$http_code" = "200" ]; then
    echo "$body"
    exit 0
  elif [ "$http_code" = "429" ]; then
    delay=$((2 ** retry_count))
    echo "Rate limited. Retrying in ${delay}s..." >&2
    sleep "$delay"
    retry_count=$((retry_count + 1))
  else
    echo "Error: HTTP $http_code" >&2
    echo "$body" >&2
    exit 1
  fi
done

echo "Max retries exceeded" >&2
exit 1
```

### Credit System

Some operations consume multiple API credits:

- Basic request: 1 credit
- Including embedded data (`include=` parameter): +1 credit per include
- Example: `?include=requester,company` costs 3 credits total

## Pagination

### Query Parameters

| Parameter | Default | Max | Description |
|-----------|---------|-----|-------------|
| `page` | 1 | - | Page number (1-indexed) |
| `per_page` | 30 | 100 | Results per page |

### Example: Paginate Through All Tickets

```bash
page=1
while true; do
  response=$(curl -s -u "$FRESHDESK_API_KEY:X" \
    "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/tickets?page=$page&per_page=100")

  count=$(echo "$response" | jq length)

  if [ "$count" -eq 0 ]; then
    break
  fi

  echo "$response" | jq '.[] | {id, subject, status}'
  page=$((page + 1))
done
```

### Link Header

Responses include a `Link` header for navigation:

```
Link: <https://domain.freshdesk.com/api/v2/tickets?page=2>; rel="next"
```

## Filtering and Embedding

### Filter Parameters

Common filters available on list endpoints:

| Parameter | Example | Description |
|-----------|---------|-------------|
| `filter` | `new_and_my_open` | Pre-defined filter |
| `requester_id` | `12345` | Filter by requester |
| `company_id` | `67890` | Filter by company |
| `updated_since` | `2024-01-01T00:00:00Z` | Modified after date |

### Pre-defined Ticket Filters

```bash
# New and open tickets assigned to me
curl -u "$FRESHDESK_API_KEY:X" \
  "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/tickets?filter=new_and_my_open"

# All unresolved tickets
curl -u "$FRESHDESK_API_KEY:X" \
  "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/tickets?filter=all_unresolved"

# Tickets updated in last 30 days
curl -u "$FRESHDESK_API_KEY:X" \
  "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/tickets?updated_since=2024-11-01T00:00:00Z"
```

### Include (Embedding Related Data)

Embed related objects to reduce API calls:

```bash
# Include requester and company with ticket
curl -u "$FRESHDESK_API_KEY:X" \
  "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/tickets/123?include=requester,company"

# Include stats with ticket list
curl -u "$FRESHDESK_API_KEY:X" \
  "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/tickets?include=stats"
```

**Available includes for tickets**: `requester`, `company`, `stats`, `conversations`, `description`

## Search API

The Search API enables complex queries across tickets, contacts, and companies.

### Syntax

```bash
curl -u "$FRESHDESK_API_KEY:X" \
  "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/search/tickets?query=\"<query>\""
```

### Query Examples

```bash
# Tickets with specific status and priority
"status:2 AND priority:3"

# Tickets from a specific requester
"requester_email:'customer@example.com'"

# Tickets created in date range
"created_at:>'2024-01-01' AND created_at:<'2024-02-01'"

# Tickets with specific tag
"tag:'urgent'"

# Tickets assigned to specific agent
"agent_id:12345"

# Full-text search in subject and description
"~'password reset'"
```

### Search Operators

| Operator | Description |
|----------|-------------|
| `AND` | Both conditions must match |
| `OR` | Either condition matches |
| `:` | Equals |
| `:>` | Greater than |
| `:<` | Less than |
| `~` | Full-text search |

## Ticket Status and Priority Values

### Status

| Value | Status |
|-------|--------|
| 2 | Open |
| 3 | Pending |
| 4 | Resolved |
| 5 | Closed |

### Priority

| Value | Priority |
|-------|----------|
| 1 | Low |
| 2 | Medium |
| 3 | High |
| 4 | Urgent |

### Source

| Value | Source |
|-------|--------|
| 1 | Email |
| 2 | Portal |
| 3 | Phone |
| 7 | Chat |
| 8 | Mobihelp |
| 9 | Feedback Widget |
| 10 | Outbound Email |

## Error Handling

### HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response |
| 201 | Created | Resource created successfully |
| 204 | No Content | Delete successful |
| 400 | Bad Request | Check request body/params |
| 401 | Unauthorized | Verify API key |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Verify resource ID |
| 409 | Conflict | Resource already exists |
| 429 | Rate Limited | Wait and retry |
| 500 | Server Error | Retry with backoff |

### Error Response Format

```json
{
  "description": "Validation failed",
  "errors": [
    {
      "field": "email",
      "message": "It should be a valid email address.",
      "code": "invalid_value"
    }
  ]
}
```

## Webhooks

Freshdesk can send webhook notifications on ticket events. Configure webhooks in Admin → Automations → Webhooks.

### Event Types

- Ticket created
- Ticket updated
- Agent reply
- Customer reply
- Note added
- Ticket resolved/closed

### Webhook Payload Example

```json
{
  "freshdesk_webhook": {
    "ticket_id": 12345,
    "ticket_subject": "Support needed",
    "ticket_status": "Open",
    "ticket_priority": "Medium",
    "ticket_requester_email": "customer@example.com",
    "triggered_event": "ticket_created"
  }
}
```

See [references/webhooks-automation.md](references/webhooks-automation.md) for detailed webhook setup.

## Best Practices

### Performance

1. **Use webhooks instead of polling** - React to events in real-time
2. **Batch operations** - Use bulk endpoints when available
3. **Cache static data** - Agent lists, ticket fields rarely change
4. **Use `include` parameter** - Reduce API calls by embedding data
5. **Paginate efficiently** - Use max `per_page=100` for bulk operations

### Security

1. **Store API keys in environment variables** - Never hardcode
2. **Use HTTPS only** - All API calls must use HTTPS
3. **Rotate keys periodically** - Regenerate API keys every 90 days
4. **Limit API key scope** - Use agent accounts with minimal permissions

### Reliability

1. **Implement retry with backoff** - Handle 429 and 5xx errors
2. **Check rate limit headers** - Pause before hitting limits
3. **Validate responses** - Check for error objects
4. **Log API calls** - Track usage and debug issues

### Data Handling

1. **Handle null fields** - API returns nulls, not omitted fields
2. **Parse timestamps as UTC** - Format: `YYYY-MM-DDTHH:MM:SSZ`
3. **Validate custom fields** - Check field types before submission
4. **Sanitize user input** - Prevent injection in descriptions

## SDKs and Libraries

### Official/Community SDKs

| Language | Package | Install |
|----------|---------|---------|
| Python | `python-freshdesk` | `pip install python-freshdesk` |
| Node.js | `node-freshdesk-api` | `npm install node-freshdesk-api` |
| Ruby | `freshdesk-ruby` | `gem install freshdesk` |
| PHP | Official samples | See Freshdesk docs |
| Java | Official samples | See Freshdesk docs |

See [references/sdk-examples.md](references/sdk-examples.md) for detailed code examples.

## Common Workflows

### Export All Tickets to JSON

```bash
#!/usr/bin/env bash
# Export all tickets to tickets.json

page=1
echo "[" > tickets.json
first=true

while true; do
  response=$(curl -s -u "$FRESHDESK_API_KEY:X" \
    "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/tickets?page=$page&per_page=100&include=description")

  count=$(echo "$response" | jq length)
  [ "$count" -eq 0 ] && break

  if [ "$first" = true ]; then
    first=false
  else
    echo "," >> tickets.json
  fi

  echo "$response" | jq '.[]' | paste -sd ',' - >> tickets.json
  page=$((page + 1))
  sleep 0.5  # Respect rate limits
done

echo "]" >> tickets.json
echo "Exported $((page - 1)) pages of tickets"
```

### Sync Contacts from CSV

```bash
#!/usr/bin/env bash
# Import contacts from contacts.csv (name,email,company_id)

while IFS=, read -r name email company_id; do
  curl -s -u "$FRESHDESK_API_KEY:X" \
    -H "Content-Type: application/json" \
    -X POST \
    -d "{\"name\":\"$name\",\"email\":\"$email\",\"company_id\":$company_id}" \
    "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/contacts"
  sleep 0.5
done < contacts.csv
```

### Get Ticket Metrics

```bash
# Get resolution time stats for closed tickets this month
curl -s -u "$FRESHDESK_API_KEY:X" \
  "https://$FRESHDESK_DOMAIN.freshdesk.com/api/v2/search/tickets?query=\"status:5 AND created_at:>'2024-12-01'\"" \
  | jq '[.results[] | .stats.resolved_at as $r | .created_at as $c |
    (($r | fromdateiso8601) - ($c | fromdateiso8601)) / 3600] |
    {count: length, avg_hours: (add / length)}'
```

## Resources

- [Freshdesk API Documentation](https://developers.freshdesk.com/api/)
- [API v2 Reference](https://developers.freshdesk.com/api/)
- [Webhooks Guide](https://support.freshdesk.com/support/solutions/folders/272646)
- [Rate Limits FAQ](https://support.freshdesk.com/en/support/solutions/articles/225433)
- [Python SDK](https://github.com/sjkingo/python-freshdesk)
- [Node.js SDK](https://github.com/kumarharsh/node-freshdesk)
- [Ruby SDK](https://github.com/snkrheads/freshdesk-ruby)

## Reference Files

For detailed endpoint documentation:

- [Tickets API Reference](references/tickets-api.md) - Full ticket CRUD, conversations, time entries
- [Contacts & Companies](references/contacts-companies.md) - Contact/company management
- [Webhooks & Automation](references/webhooks-automation.md) - Webhook setup and automation rules
- [SDK Code Examples](references/sdk-examples.md) - Python, Node.js, Ruby examples
