---
name: "gitlab-webhook"
description: "GitLab webhook operations via API. ALWAYS use this skill when user wants to: (1) list/view webhooks, (2) create/update/delete webhooks, (3) configure webhook events, (4) test webhook delivery."
version: "1.0.0"
author: "GitLab-Assistant-Skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# Webhook Skill

Webhook management for GitLab using `glab api` raw endpoint calls.

## Quick Reference

| Operation | Command Pattern | Risk |
|-----------|-----------------|:----:|
| List webhooks | `glab api projects/:id/hooks` | - |
| Get webhook | `glab api projects/:id/hooks/:hook_id` | - |
| Create webhook | `glab api projects/:id/hooks -X POST -f ...` | ⚠️ |
| Update webhook | `glab api projects/:id/hooks/:hook_id -X PUT -f ...` | ⚠️ |
| Delete webhook | `glab api projects/:id/hooks/:hook_id -X DELETE` | ⚠️⚠️ |
| Test webhook | `glab api projects/:id/hooks/:hook_id/test/:trigger -X POST` | ⚠️ |
| List group hooks | `glab api groups/:id/hooks` | - |

**Risk Legend**: - Safe | ⚠️ Caution | ⚠️⚠️ Warning | ⚠️⚠️⚠️ Danger

## When to Use This Skill

**ALWAYS use when:**
- User mentions "webhook", "hook", "web hook"
- User wants to integrate GitLab with external services
- User mentions "notification", "callback", "trigger URL"
- User wants to set up CI/CD integrations or Slack notifications

**NEVER use when:**
- User wants to configure built-in integrations (use project settings)
- User wants to manage CI/CD pipelines (use gitlab-ci)
- User wants system hooks (requires admin access)

## API Prerequisites

**Required Token Scopes:** `api`

**Permissions:**
- View webhooks: Maintainer+
- Manage webhooks: Maintainer+

## Webhook Events

| Event | Flag | Description |
|-------|------|-------------|
| Push | `push_events` | Code pushed to repository |
| Tag | `tag_push_events` | Tags created/deleted |
| Merge Request | `merge_requests_events` | MR created/updated/merged |
| Issues | `issues_events` | Issue created/updated/closed |
| Notes | `note_events` | Comments on MRs/issues/commits |
| Confidential Notes | `confidential_note_events` | Confidential comments |
| Job | `job_events` | CI job status changes |
| Pipeline | `pipeline_events` | Pipeline status changes |
| Deployment | `deployment_events` | Deployment status changes |
| Wiki | `wiki_page_events` | Wiki pages created/updated |
| Releases | `releases_events` | Releases created |

## Available Commands

### List Webhooks

```bash
# List project webhooks
glab api projects/123/hooks --method GET

# List with pagination
glab api projects/123/hooks --paginate

# List group webhooks (Premium)
glab api groups/456/hooks --method GET

# Using project path
glab api "projects/$(echo 'mygroup/myproject' | jq -Rr @uri)/hooks"
```

### Get Webhook Details

```bash
# Get specific webhook
glab api projects/123/hooks/789 --method GET
```

### Create Webhook

```bash
# Basic webhook for push events
glab api projects/123/hooks --method POST \
  -f url="https://example.com/webhook" \
  -f push_events=true

# Webhook for MR and pipeline events
glab api projects/123/hooks --method POST \
  -f url="https://example.com/webhook" \
  -f push_events=false \
  -f merge_requests_events=true \
  -f pipeline_events=true

# Webhook with secret token
glab api projects/123/hooks --method POST \
  -f url="https://example.com/webhook" \
  -f push_events=true \
  -f token="my-secret-token" \
  -f enable_ssl_verification=true

# Full-featured webhook
glab api projects/123/hooks --method POST \
  -f url="https://example.com/webhook" \
  -f push_events=true \
  -f tag_push_events=true \
  -f merge_requests_events=true \
  -f issues_events=true \
  -f note_events=true \
  -f pipeline_events=true \
  -f job_events=true \
  -f token="secret" \
  -f enable_ssl_verification=true

# Webhook for specific branches only
glab api projects/123/hooks --method POST \
  -f url="https://example.com/webhook" \
  -f push_events=true \
  -f push_events_branch_filter="main"
```

### Update Webhook

```bash
# Update URL
glab api projects/123/hooks/789 --method PUT \
  -f url="https://new-url.com/webhook"

# Enable additional events
glab api projects/123/hooks/789 --method PUT \
  -f pipeline_events=true \
  -f job_events=true

# Disable event
glab api projects/123/hooks/789 --method PUT \
  -f push_events=false

# Update secret token
glab api projects/123/hooks/789 --method PUT \
  -f token="new-secret-token"

# Change SSL verification
glab api projects/123/hooks/789 --method PUT \
  -f enable_ssl_verification=false
```

### Delete Webhook

```bash
# Delete webhook
glab api projects/123/hooks/789 --method DELETE
```

### Test Webhook

```bash
# Test push event
glab api projects/123/hooks/789/test/push_events --method POST

# Test MR event
glab api projects/123/hooks/789/test/merge_requests_events --method POST

# Test tag push event
glab api projects/123/hooks/789/test/tag_push_events --method POST

# Test note event
glab api projects/123/hooks/789/test/note_events --method POST

# Test issues event
glab api projects/123/hooks/789/test/issues_events --method POST
```

## Webhook Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `url` | string | Webhook endpoint URL (required) |
| `token` | string | Secret token for validation |
| `push_events` | boolean | Trigger on push |
| `push_events_branch_filter` | string | Branch filter for push events |
| `tag_push_events` | boolean | Trigger on tag push |
| `merge_requests_events` | boolean | Trigger on MR events |
| `issues_events` | boolean | Trigger on issue events |
| `confidential_issues_events` | boolean | Trigger on confidential issues |
| `note_events` | boolean | Trigger on comments |
| `confidential_note_events` | boolean | Trigger on confidential notes |
| `pipeline_events` | boolean | Trigger on pipeline events |
| `job_events` | boolean | Trigger on job events |
| `deployment_events` | boolean | Trigger on deployments |
| `wiki_page_events` | boolean | Trigger on wiki changes |
| `releases_events` | boolean | Trigger on releases |
| `enable_ssl_verification` | boolean | Verify SSL certificate |

## Common Workflows

### Workflow 1: Set Up Slack Notifications

```bash
# Create webhook for Slack
glab api projects/123/hooks --method POST \
  -f url="https://hooks.slack.com/services/T00/B00/XXX" \
  -f push_events=true \
  -f merge_requests_events=true \
  -f pipeline_events=true \
  -f enable_ssl_verification=true
```

### Workflow 2: Set Up CI Trigger

```bash
# Webhook to trigger external CI
glab api projects/123/hooks --method POST \
  -f url="https://ci.example.com/trigger" \
  -f push_events=true \
  -f tag_push_events=true \
  -f token="ci-trigger-token" \
  -f push_events_branch_filter="main"
```

### Workflow 3: Audit All Webhooks

```bash
# List all webhooks with details
glab api projects/123/hooks --paginate | \
  jq -r '.[] | "ID: \(.id)\n  URL: \(.url)\n  Events: push=\(.push_events), mr=\(.merge_requests_events), pipeline=\(.pipeline_events)\n  SSL: \(.enable_ssl_verification)\n"'
```

### Workflow 4: Migrate Webhook to New URL

```bash
# 1. Get current webhook config
glab api projects/123/hooks/789 | jq

# 2. Update URL
glab api projects/123/hooks/789 --method PUT \
  -f url="https://new-service.example.com/webhook"

# 3. Test the webhook
glab api projects/123/hooks/789/test/push_events --method POST
```

### Workflow 5: Set Up Deployment Notifications

```bash
# Webhook for deployment events only
glab api projects/123/hooks --method POST \
  -f url="https://deploy-tracker.example.com/webhook" \
  -f push_events=false \
  -f deployment_events=true \
  -f token="deploy-secret"
```

### Workflow 6: Disable All Non-Essential Events

```bash
hook_id=789

# Keep only push and MR events
glab api projects/123/hooks/$hook_id --method PUT \
  -f push_events=true \
  -f merge_requests_events=true \
  -f tag_push_events=false \
  -f issues_events=false \
  -f note_events=false \
  -f job_events=false \
  -f pipeline_events=false
```

## Webhook Payload

GitLab sends JSON payloads with event data. Key fields:

### Push Event Payload
```json
{
  "object_kind": "push",
  "ref": "refs/heads/main",
  "before": "abc123...",
  "after": "def456...",
  "commits": [...],
  "project": {...}
}
```

### MR Event Payload
```json
{
  "object_kind": "merge_request",
  "event_type": "merge_request",
  "object_attributes": {
    "iid": 1,
    "title": "...",
    "state": "opened",
    "action": "open"
  }
}
```

## Validating Webhooks

Use the secret token to validate webhook authenticity:

```bash
# In your webhook handler, verify the X-Gitlab-Token header
# matches the token you configured
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Webhook not firing | Event not enabled | Check event flags |
| 403 Forbidden | Not maintainer | Need Maintainer+ role |
| SSL verification failed | Invalid certificate | Use `enable_ssl_verification=false` or fix cert |
| Webhook URL unreachable | Network/firewall issue | Verify URL is accessible from GitLab |
| Test returns error | Endpoint error | Check your webhook handler logs |
| Too many requests | Webhook loop | Verify handler doesn't trigger events |

## Best Practices

1. **Use HTTPS**: Always use secure URLs for webhooks
2. **Set secret token**: Validate webhooks with a secret token
3. **Enable only needed events**: Reduce noise and processing
4. **Handle failures gracefully**: GitLab retries failed deliveries
5. **Monitor webhook health**: Check recent deliveries in GitLab UI
6. **Use branch filters**: Limit push events to relevant branches

## Related Documentation

- [API Helpers](../shared/docs/API_HELPERS.md)
- [Safeguards](../shared/docs/SAFEGUARDS.md)
- [Quick Reference](../shared/docs/QUICK_REFERENCE.md)
- [GitLab Webhooks API](https://docs.gitlab.com/ee/api/projects.html#hooks)
