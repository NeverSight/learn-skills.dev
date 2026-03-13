---
name: tracekit-alerts
description: Set up alerting rules and notification channels in TraceKit for errors, performance degradation, and availability monitoring. Covers dashboard setup, API-based rules, Slack integration, and a starter kit of recommended alerts. Use when the user asks about alerts, notifications, error spikes, latency monitoring, or uptime.
---

# TraceKit Alerts

## When To Use

Use this skill when the user asks to:
- Set up alerts or notifications in TraceKit
- Get notified on errors or error spikes
- Monitor latency or performance degradation
- Detect error spikes automatically
- Set up uptime monitoring
- Configure Slack notifications for errors
- Create alerting rules via API or the dashboard
- Manage alert fatigue or notification routing

## Non-Negotiable Rules

1. **Never hardcode API keys or webhook URLs** in code or config files. Use `TRACEKIT_AUTH_TOKEN` env var for API access.
2. **Always include a test notification step** after setting up a channel to verify delivery.
3. **Always recommend starting with the starter kit** before customizing — it provides sensible defaults for the most common scenarios.

## Prerequisites

- Any TraceKit SDK (backend or frontend) must be installed and sending data to the dashboard.
- For Slack integration: Slack workspace admin access (or permission to approve the TraceKit app).
- If no SDK is set up yet, complete the appropriate SDK skill first (see `tracekit-apm-setup` skill).

## Detection

Before applying this skill, check the project:

1. **Check for any TraceKit SDK** in the project — scan `package.json`, `go.mod`, `requirements.txt`, `composer.json`, `pom.xml`, `.csproj`, or `Gemfile`.
2. **If no SDK detected**, redirect to the `tracekit-apm-setup` skill to install an SDK first. Alerts need data flowing into TraceKit before they can trigger.
3. **Alerts are SDK-agnostic** — no SDK-specific configuration needed. Alerts operate on data already in the dashboard.

## Step 1: Set Up Notification Channel (Dashboard)

Start with Slack (the most common integration), then optionally add other channels.

### Slack Channel Setup

1. Navigate to `https://app.tracekit.dev/settings/channels`.
2. Click **Add Channel** > **Slack**.
3. Click **Add to Slack** — this opens the Slack OAuth flow.
4. Authorize the TraceKit app in your Slack workspace.
5. Select the target channel (e.g., `#engineering-alerts`).
6. Click **Send Test Notification** to verify the connection.
7. Confirm the test message appears in your Slack channel.

### Other Notification Channels

TraceKit supports additional channels — set them up the same way via Settings > Channels:

- **Email:** Enter one or more email addresses. No external app approval needed.
- **Webhook:** Provide a URL that accepts POST requests with JSON payload. Useful for custom integrations (e.g., Zapier, internal tools).
- **PagerDuty:** Enter your PagerDuty integration key. Alerts create PagerDuty incidents with appropriate severity.

For most teams, start with Slack and add others as needed.

## Step 2: Starter Kit — Recommended Alerts

Create these 4 alerts to cover the most common monitoring scenarios. Each alert has been tuned for sensible defaults that avoid alert fatigue while catching real issues.

### Alert 1: Error Spike

Detects sudden increases in error volume compared to the rolling baseline.

| Setting | Value |
|---------|-------|
| **Name** | Error Spike |
| **Metric** | Error count |
| **Condition** | Exceeds 5x rolling average |
| **Time window** | 5 minutes |
| **Channel** | Slack `#engineering-alerts` |
| **Severity** | Critical |

**How to create:**
1. Navigate to `https://app.tracekit.dev/alerts/rules`.
2. Click **Create Rule**.
3. Select metric: **Error count**.
4. Set condition: **Exceeds 5x baseline** with a **5-minute** window.
5. Select channel: your Slack channel.
6. Set severity: **Critical**.
7. Save and activate.

### Alert 2: P95 Latency

Catches performance degradation before it impacts most users.

| Setting | Value |
|---------|-------|
| **Name** | P95 Latency |
| **Metric** | Transaction P95 response time |
| **Condition** | Exceeds 2000ms |
| **Time window** | 10 minutes |
| **Channel** | Slack `#engineering-alerts` |
| **Severity** | Warning |

**How to create:**
1. Navigate to `https://app.tracekit.dev/alerts/rules`.
2. Click **Create Rule**.
3. Select metric: **Transaction P95**.
4. Set condition: **Threshold > 2000ms** with a **10-minute** window.
5. Select channel: your Slack channel.
6. Set severity: **Warning**.
7. Save and activate.

### Alert 3: Uptime Drop

Detects availability drops by monitoring successful request rate.

| Setting | Value |
|---------|-------|
| **Name** | Uptime Drop |
| **Metric** | Successful request rate |
| **Condition** | Falls below 99.5% |
| **Time window** | 15 minutes |
| **Channel** | Slack + Email (critical) |
| **Severity** | Critical |

**How to create:**
1. Navigate to `https://app.tracekit.dev/alerts/rules`.
2. Click **Create Rule**.
3. Select metric: **Successful request rate (%)**.
4. Set condition: **Below 99.5%** with a **15-minute** window.
5. Select channels: both your Slack channel and an email address.
6. Set severity: **Critical**.
7. Save and activate.

### Alert 4: New Error Type

Catches new bugs immediately by alerting on error messages never seen before.

| Setting | Value |
|---------|-------|
| **Name** | New Error Type |
| **Metric** | First occurrence |
| **Condition** | Error message not previously seen |
| **Time window** | Immediate |
| **Channel** | Slack `#engineering-alerts` |
| **Severity** | Warning |

**How to create:**
1. Navigate to `https://app.tracekit.dev/alerts/rules`.
2. Click **Create Rule**.
3. Select type: **First occurrence of new issue**.
4. Select channel: your Slack channel.
5. Set severity: **Warning**.
6. Save and activate.

## Step 3: Create Custom Alerts (Dashboard Walkthrough)

Beyond the starter kit, create custom alerts for your specific needs:

1. Navigate to `https://app.tracekit.dev/alerts/rules`.
2. Click **Create Rule**.
3. **Select metric type:**
   - Error count — total errors in a time window
   - Transaction P95/P99 — latency percentiles
   - Throughput — requests per minute
   - Successful request rate — availability percentage
   - Custom metric — any metric you send via the SDK
4. **Set conditions:**
   - Threshold (absolute value, e.g., > 100 errors)
   - Relative (compared to baseline, e.g., > 3x average)
   - Window (1 minute to 24 hours)
5. **Select notification channels** — one or more channels can be assigned.
6. **Set severity:**
   - Critical — immediate action required
   - Warning — investigate soon
   - Info — informational, no action needed
7. **Save and activate** the rule.

You can also set a **resolve notification** — TraceKit will send a follow-up message when the metric returns to normal. This reduces the need to manually check if an issue has recovered.

## Step 4: Programmatic Alerts (Dashboard and API)

For teams that manage infrastructure as code, create and manage alerts programmatically.

### Dashboard

The recommended way to manage alerts is through the TraceKit dashboard at `https://app.tracekit.dev/alerts`. The dashboard provides a full UI for creating, editing, listing, and deleting alert rules.

> **Note:** The TraceKit CLI (`tracekit`) supports `webhook create/list/delete` commands for managing webhook channels, but does **not** have `alerts` subcommands. Use the dashboard or the REST API below to manage alert rules programmatically.

### API

Create an alert rule via the REST API:

```bash
curl -X POST https://app.tracekit.dev/api/v1/alerts \
  -H "Authorization: Bearer $TRACEKIT_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Error Spike",
    "metric": "error_count",
    "threshold": {
      "type": "relative",
      "value": 5,
      "window": "5m"
    },
    "channels": ["slack:engineering-alerts"],
    "severity": "critical"
  }'
```

List all alert rules:

```bash
curl https://app.tracekit.dev/api/v1/alerts \
  -H "Authorization: Bearer $TRACEKIT_AUTH_TOKEN"
```

Update an alert rule:

```bash
curl -X PATCH https://app.tracekit.dev/api/v1/alerts/alert_abc123 \
  -H "Authorization: Bearer $TRACEKIT_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "threshold": {
      "type": "relative",
      "value": 10,
      "window": "10m"
    }
  }'
```

**Auth token scope:** The token must have `alerts:write` scope for creating and modifying alerts. Get your token from Dashboard > Settings > Auth Tokens.

## Step 5: Verification

After setting up the starter kit alerts, verify they work:

1. **Create all 4 starter kit alerts** using the dashboard walkthrough above.
2. **Trigger a test error** in your application — call an endpoint that throws an exception, or use the SDK's `captureException` method.
3. **Wait 1-2 minutes** for the error spike alert to evaluate the time window.
4. **Check your Slack channel** for the alert notification.
5. **Click the notification link** — it should take you directly to the error in the TraceKit dashboard.
6. **Verify the alert details** show the correct metric, threshold, and severity.

If the alert does not fire, see Troubleshooting below.

## Troubleshooting

### Alert not firing

- **Check alert is active:** Navigate to Alerts > Rules and verify the alert status is "Active" (not "Disabled" or "Muted").
- **Check threshold is realistic:** For testing, temporarily lower the threshold (e.g., error count > 1 instead of > 5x baseline). Your test environment may not have enough baseline data for relative thresholds.
- **Check time window:** A 15-minute window means the condition must persist for 15 minutes before firing. Use a shorter window (1-5 minutes) for testing.

### Slack not receiving notifications

- **Verify channel connection:** Go to Settings > Channels and check the Slack channel shows a green "Connected" status.
- **Send a test notification:** Click "Test" next to the channel. If the test fails, re-authorize the TraceKit app in Slack.
- **Check Slack permissions:** The TraceKit app must have permission to post to the selected channel. Try a public channel first.

### Too many alerts (alert fatigue)

- **Increase thresholds:** Error spike at 5x baseline may be too sensitive for noisy services. Try 10x.
- **Widen time windows:** A 5-minute window fires more frequently than a 15-minute window.
- **Use resolve notifications:** Enable "Send resolved" so you know when issues clear without manually checking.
- **Consolidate channels:** Route critical alerts to Slack and info alerts to email to reduce Slack noise.
- **Mute during deploys:** Use the API to temporarily mute alerts during deployment windows.

### API authentication error

- **Check auth token:** Ensure `TRACEKIT_AUTH_TOKEN` is set and the token has `alerts:write` scope.
- **Check token expiry:** Auth tokens expire after 90 days by default. Create a new token if expired.
- **Check endpoint URL:** The API base URL is `https://app.tracekit.dev/api/v1/` — ensure no trailing slash issues.

## Next Steps

Once alerting is configured, consider:
- **Distributed Tracing** — See full trace context in alert details to understand cross-service failures (see `tracekit-distributed-tracing` skill)
- **Code Monitoring** — Set live breakpoints when alerts fire to capture production state without redeploying (see `tracekit-code-monitoring` skill)
- **Releases** — Track crash-free rates per release and alert on regressions (see `tracekit-releases` skill)

## References

- Alert rules docs: `https://app.tracekit.dev/docs/alerts`
- Notification channels docs: `https://app.tracekit.dev/docs/channels`
- CLI reference: `https://app.tracekit.dev/docs/cli`
- Dashboard: `https://app.tracekit.dev`
