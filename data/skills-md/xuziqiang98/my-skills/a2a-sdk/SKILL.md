---
name: a2a-sdk
description: Comprehensive Agent2Agent (A2A) JavaScript SDK skill for building A2A-compliant agents and clients. Use when implementing or integrating @a2a-js/sdk, creating A2A servers/clients, using JSON-RPC/REST/gRPC transports, streaming task updates, handling tasks/artifacts, authentication, or push notifications.
---

# A2A JavaScript SDK Skill

## Overview

Use this skill to implement A2A-compliant servers and clients with @a2a-js/sdk, including tasks, streaming, authentication, and transport selection. Follow A2A protocol v0.3.0.

## Core Workflows

1. Select transport: JSON-RPC (default), REST, or gRPC.
2. Define an AgentCard and AgentExecutor for server implementations.
3. Use ClientFactory for client creation and message exchange.
4. Add task handling and artifacts for long-running operations.
5. Use streaming when real-time updates are required.
6. Add authentication or push notifications when needed.

## Bundled Resources

- `README.md`: Quick overview and basic usage patterns.
- `REFERENCE.md`: Full API reference and advanced features.
- `HELPERS.md`: Helper utilities and common patterns.
- `templates/server/basic-server.ts`: Minimal server template.
- `templates/server/task-server.ts`: Task-based server template.
- `templates/client/basic-client.ts`: Minimal client template.
- `templates/client/streaming-client.ts`: Streaming client template.
- `examples/authentication.md`: Authentication server/client examples.
- `examples/streaming.md`: Streaming server/client examples.

## Implementation Guidance

- Keep AgentCard fields aligned with protocol v0.3.0.
- Prefer direct message responses for simple requests.
- Use tasks for long-running work and publish status updates and artifacts.
- Use streaming for real-time task progress updates.
- Include authentication via custom user builders or authenticated transports when required.
