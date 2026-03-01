---
name: bloodbank-event-system
description: Use this skill when facilitating communication between different systems in the 33GOD ecosystem. Every action in the pipeline is invoked by an event published by Bloodbank. Simiarly, every result is published as an event to be consumed by any system interested in it.
---

# Bloodbank Event System

Bloodbank is the event bus for the 33GOD ecosystem. It allows different systems to communicate with each other in an event-driven manner. It's designed to facilitate loose coupling between services, enabling scalability and flexibility.

## Architecture

- Each component in the pipeline is responsible for defining its own payload using Pydantic2 and adding the definitions to Bloodbank.
- Each event consists of a payload with optional metadata. The payload is wrapped in a common envelope that includes metadata such as event type, timestamp, and source.
- RabbitMQ is used as the event bus. It handles the routing of events between producers and consumers.
- Events are immutable messages that let us know something has happened in the system. Their key always follow the pattern `<eventType>.<entity>.<past-tense-action>`, for example, `github.pr.created`.
- Events that result in a mutation are Command events. Unlike basic events, they have their own exchange and are bound to the appropriate worker queue(s). Command events follow the naming convention `<eventType>.<entity>.<action>`, for example, `github.pr.merge`.

## Infrastructure

RabbitMQ is used as the event bus. It is

### Event Inventory

The number of events in the system is always growing as new features and integrations are added. You can get a complete list of events and their payload definitions by running the Bloodbank CLI command:

```bash
bloodbank list-events # Returns a list of all events in the system

# To only list commands you can use:
bloodbank list-events --type command

# or for convenience:
bloodbank list-commands

```

To print the schema for a specific event, use:

```bash
bloodbank show [event-key]
```

## Integration with n8n Workflows

### Shell Context Independence for Execute Command Nodes

**Critical Pattern**: n8n Execute Command nodes run in subprocess environments without access to shell aliases/functions.

**Implementation Requirements**:
1. **Self-contained scripts** in `~/.local/bin/`
2. **Explicit PATH exports** in script headers
3. **No dependencies** on `.zshrc`, `.bashrc`, or shell configuration
4. **Detached execution** for long-running operations with immediate response

### jelmore CLI Integration Pattern

**jelmore** is the preferred execution primitive for LLM invocations in n8n workflows. It implements shell context independence while providing convention-based intelligence and event-driven coordination with Bloodbank.

**Why Use jelmore in n8n Workflows**:
- ✅ Shell-context-free execution (no alias dependencies)
- ✅ Immediate return with session handle (non-blocking)
- ✅ Convention over configuration (auto-infer client/MCP servers)
- ✅ Built-in iMi worktree integration
- ✅ Native Bloodbank event publishing
- ✅ Detached Zellij sessions for observability

**Execute Command Node with jelmore**:
```javascript
{
  "command": "uv run jelmore execute -f /path/to/task.md --worktree pr-{{ $json.pr_number }} --auto --json",
  "timeout": 5000
}
```

**Immediate Response (Non-blocking)**:
```json
{
  "execution_id": "abc123",
  "session_name": "jelmore-pr-458-20251103-143022",
  "client": "claude-flow",
  "log_path": "/tmp/jelmore-abc123.log",
  "working_directory": "/home/delorenj/code/n8n/pr-458",
  "started_at": "2025-11-03T14:30:22"
}
```

**Parse Response Node**:
```javascript
const output = JSON.parse($('Execute Command').json.stdout);

return {
  sessionName: output.session_name,
  attachCommand: `zellij attach ${output.session_name}`,
  executionId: output.execution_id,
  logPath: output.log_path,
  workingDir: output.working_directory
};
```

### Event-Driven Coordination Pattern

**jelmore automatically publishes lifecycle events to Bloodbank**, enabling event-driven workflow orchestration:

**Execution Lifecycle Events**:
```
jelmore.execution.started   → Task begins
jelmore.execution.progress  → Periodic status updates
jelmore.execution.completed → Task finished successfully
jelmore.execution.failed    → Task encountered error
```

**Workflow Integration Pattern**:

```
┌─────────────────────────────────────────────┐
│  n8n Workflow (Execute Command Node)        │
│  - Triggers jelmore execution               │
│  - Gets immediate response with handle      │
│  - Continues to next node                   │
└─────────────────┬───────────────────────────┘
                  │
                  │ (event: jelmore.execution.started)
                  ▼
┌─────────────────────────────────────────────┐
│  Bloodbank Event Bus                        │
│  - Routes events to subscribers             │
│  - Persists event history                   │
└─────────────────┬───────────────────────────┘
                  │
                  │ (subscribe to lifecycle events)
                  ▼
┌─────────────────────────────────────────────┐
│  n8n Webhook Trigger (Separate Workflow)    │
│  - Listens for jelmore.execution.completed  │
│  - Processes results                        │
│  - Triggers next phase                      │
└─────────────────────────────────────────────┘
```

**Example Multi-Phase Workflow**:

**Phase 1: PR Review Trigger (Workflow A)**
```javascript
// Execute Command Node
{
  "command": "uv run jelmore execute --config pr-review.json --var PR_NUMBER={{ $json.pr_number }} --json"
}

// HTTP Request Node (Publish Event)
{
  "method": "POST",
  "url": "http://bloodbank/events/publish",
  "body": {
    "event_type": "workflow.pr_review.triggered",
    "payload": {
      "execution_id": "{{ $json.executionId }}",
      "pr_number": "{{ $json.prNumber }}",
      "session_name": "{{ $json.sessionName }}"
    }
  }
}
```

**Phase 2: Completion Handler (Workflow B - Webhook Trigger)**
```javascript
// Webhook receives: jelmore.execution.completed event from Bloodbank
// Function Node processes result
const result = $webhook.body;

if (result.status === "success") {
  // Parse jelmore output
  const analysis = result.output;

  // Update GitHub PR with comments
  return {
    pr_number: result.context.pr_number,
    comments: analysis.review_comments,
    approved: analysis.recommendation === "APPROVE"
  };
}
```

### jelmore Configuration Patterns for n8n

**Use jelmore config files for reusable workflow patterns**. Store configs in `~/.config/jelmore/profiles/` or in your project's `.jelmore/` directory.

**Example: PR Review Config (`~/.config/jelmore/profiles/n8n-pr-review.json`)**:
```json
{
  "name": "n8n PR Review Workflow",
  "client": "claude-flow",
  "mode": "detached",
  "task": {
    "template": "/home/delorenj/code/DeLoDocs/AI/Agents/Generic/My Personal PR Review Representative.md",
    "context": {
      "pr_number": "{{ PR_NUMBER }}",
      "repository": "{{ REPO }}"
    }
  },
  "execution": {
    "strategy": "swarm",
    "max_agents": 4
  },
  "environment": {
    "worktree_resolver": "imi",
    "mcp_servers": ["github-mcp", "bloodbank-mcp"]
  },
  "observability": {
    "session_prefix": "pr-review",
    "publish_events": true,
    "event_tags": {
      "source": "n8n",
      "workflow_id": "{{ WORKFLOW_ID }}"
    }
  },
  "callbacks": {
    "on_completion": "{{ WEBHOOK_URL }}",
    "on_error": "{{ ERROR_WEBHOOK }}"
  }
}
```

**n8n Execute Command with Config**:
```javascript
{
  "command": "uv run jelmore execute --config n8n-pr-review.json --var PR_NUMBER={{ $json.pr_number }} --var REPO={{ $json.repo }} --var WORKFLOW_ID={{ $workflow.id }} --json"
}
```

### Advanced Pattern: Status Monitoring

**Optional status polling for long-running tasks**:

```javascript
// Execute Command Node (in loop with delay)
{
  "command": "uv run jelmore status {{ $json.executionId }} --json",
  "continueOnFail": true
}

// Switch Node (check status)
if (status === "running") {
  // Continue polling
} else if (status === "completed") {
  // Process results
} else if (status === "failed") {
  // Handle error
}
```

### Bloodbank Event Schema for jelmore

**Event: `jelmore.execution.started`**
```json
{
  "event_type": "jelmore.execution.started",
  "timestamp": "2025-11-03T14:30:22Z",
  "payload": {
    "execution_id": "abc123",
    "client": "claude-flow",
    "worktree": "/home/delorenj/code/n8n/pr-458",
    "session_name": "jelmore-pr-458-20251103-143022",
    "config": {
      "model_tier": "balanced",
      "max_agents": 4
    }
  },
  "metadata": {
    "source": "jelmore",
    "tags": {
      "workflow_id": "n8n_workflow_123"
    }
  }
}
```

**Event: `jelmore.execution.completed`**
```json
{
  "event_type": "jelmore.execution.completed",
  "timestamp": "2025-11-03T14:45:38Z",
  "payload": {
    "execution_id": "abc123",
    "status": "success",
    "duration_seconds": 916,
    "output": {
      "summary": "...",
      "artifacts": ["..."]
    }
  }
}
```

### Legacy Pattern (Pre-jelmore)

**Example Execute Command Node Configuration (Custom Scripts)**:
```javascript
{
  "command": "/home/delorenj/.local/bin/workflow-script task-123",
  "timeout": 5000  // Returns immediately with session info
}
```

**Observability Pattern**:
- Scripts spawn detached Zellij sessions for long-running operations
- Return unique session identifiers immediately
- Workflow can continue while operation runs in background
- Session can be attached later for inspection

**Migration Path**: Replace custom scripts with `jelmore execute` calls to leverage convention engine, event publishing, and unified execution model.

**See Also**:
- `ecosystem-patterns` skill - jelmore architecture and usage patterns
- `/home/delorenj/code/jelmore/CLI.md` - Complete jelmore CLI reference
- `creating-workflows` skill - Workflow patterns with jelmore integration
