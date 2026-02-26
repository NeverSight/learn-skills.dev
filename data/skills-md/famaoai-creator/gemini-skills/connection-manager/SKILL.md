---
name: connection-manager
description: Manages secure connections to external tools (AWS, Slack, Jira, Box). Validates credentials in the Personal Tier and injects them into the execution context.
status: implemented
category: Utilities
last_updated: '2026-02-13'
tags:
  - cloud
  - communication
  - gemini-skill
---

# Connection Manager

This skill is the "Keymaster" of the ecosystem. It centralizes authentication to prevent credential sprawl.

## Capabilities

### 1. Credential Validation

- Checks if required config files exist in `knowledge/personal/connections/`.
- Verifies format correctness (JSON schema check).

### 2. Environment Injection

- Reads the private JSON configs and exports them as environment variables (e.g., `SLACK_BOT_TOKEN`, `JIRA_API_TOKEN`) for the duration of the session.

### 3. Connection Diagnostics

- Performs a "Ping" test for configured services to verify that tokens are active and permissions are correct.

## Usage

- "Check my connection status for all configured tools."
- "Inject Slack credentials for the `slack-communicator-pro` skill."

## Knowledge Protocol

- **Strict Confidentiality**: Never outputs actual token values to logs or console. Only reports "Connected" or "Failed".
- Refers to `knowledge/connections/setup_guide.md`.
