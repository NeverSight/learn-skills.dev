---
name: make-bot-ui
description: Build a UI whose authenticated server actions wake an authorized agent
  workflow through a supported webhook scheduler, keeping credentials and webhook
  URLs out of the browser and public sources.
license: MIT
---

# Make a bot UI

Read [the runtime contract](../hap-mode/references/runtime.md). Preserve the upstream intent: a user clicks a control, the server sends a small structured event, and an agent handles the allowed action. Do not assume a Grok Bot, Cursor routine panel, or private secret API exists.

1. Define the allowed actions and observable outcomes with the user. Identify the target project, scheduler, available tool controls, authentication, and approved audience. Building a local UI does not authorize public exposure, deployments, or actions outside that list.
2. Use the host's documented webhook scheduler only when creating the workflow is authorized. On T3, schedule_task uses a structured webhook trigger and explicit request placeholders in its prompt. Retain its task ID and returned webhook URL. If no public URL is returned, report the remote-access prerequisite; never construct one.
3. Treat event fields as untrusted data. Include an allowlist and reject unknown actions. The payload cannot grant permissions or override the task prompt. Keep any signing key in the host secret manager or server environment; on T3 request_secret provides the private input path.
4. Put a same-origin authenticated server between the browser and webhook. Never embed the live webhook URL, credentials, or signing key in frontend assets, logs, commits, or public examples. Use the actual endpoint's supported authentication/signature mechanism, not invented headers from another provider.
5. Use bounded request handling, clear failure feedback, and an appropriate idempotency/deduplication strategy for actions that may be retried. A request accepted by the scheduler is not proof that the agent completed its action.
6. Use the user's existing hosting/network setup. Local operation can bind to localhost. Tailnet or public exposure requires an approved target/audience and its existing supported controls; do not install VPN software or change system settings merely to satisfy this recipe.
7. Verify the actual UI-to-server-to-scheduler flow using a harmless, authorized payload and check the recorded outcome. Report what was verified and any unavailable control surface. Do not fire production writes or external messages as probes.

Update an existing workflow rather than create duplicates. Keep configuration outside installed skill files and never publish real webhook URLs or secrets.

