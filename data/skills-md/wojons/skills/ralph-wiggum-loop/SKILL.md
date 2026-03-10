---
name: ralph-wiggum-loop
description: Enterprise-grade AI-driven development workflow engine with plugin system, agent orchestration, monitoring, and complex workflow patterns. Build-verify loops that iterate until success.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: workflow
---

# Ralph Wiggum Loop - Enterprise Workflow Engine

Build powerful AI-driven development workflows that iterate until tasks succeed. Features a plugin system, agent orchestration, monitoring, and enterprise-grade workflow patterns including DAGs, state machines, and circuit breakers.

## Quick Start

```bash
# Generate a working Ralph loop with full plugin system
bash scripts/generate-ralph-loop.sh ./my-loop

cd my-loop
pip install -r requirements.txt

# Run with basic configuration
python ralph-loop.py loop --commit

# Run with custom workflow
python ralph-loop.py loop --workflow advanced.yaml --config ralph.yaml
```

## What This Skill Provides

### 1. Core Workflow Engine

**File**: `scripts/ralph-loop-example.py`

A production-ready workflow engine with:

- **State Machine Architecture**: Explicit states with transitions
- **Plugin System**: Extensible hooks for custom behaviors
- **Agent Orchestration**: Multi-agent coordination with specialized roles
- **Monitoring & Observability**: Traces, metrics, and structured logging
- **Failure Recovery**: Retry policies, circuit breakers, compensating actions
- **DAG Support**: Complex dependency graphs for parallel execution
- **Circuit Breaker**: Prevent cascade failures

### 2. Plugin System

Extend the loop without modifying core code:

```yaml
# ralph.yaml - Plugin configuration
plugins:
  - name: slack-notifier
    entry: plugins/slack.py
    hooks:
      - workflow.on_start
      - workflow.on_complete
    config:
      webhook: https://hooks.slack.com/services/...
  
  - name: custom-verifier
    entry: plugins/verifiers/security.py
    hooks:
      - phase.before_verify
      - phase.after_verify
    config:
      security_level: strict
  
  - name: metrics-exporter
    entry: plugins/metrics/prometheus.py
    hooks:
      - workflow.on_iteration
    config:
      endpoint: http://localhost:9090
```

**Available Hooks:**
- `workflow.on_start` - Loop initialization
- `workflow.on_iteration` - Each iteration start
- `workflow.on_complete` - Loop completion
- `workflow.on_failure` - Loop failure
- `phase.before_build` - Before build phase
- `phase.after_build` - After build phase
- `phase.before_verify` - Before verify phase
- `phase.after_verify` - After verify phase
- `agent.on_invoke` - Agent invocation
- `state.on_change` - State transitions

### 3. Advanced Workflow Patterns

**State Machine Workflows:**
```yaml
# advanced.yaml
workflow:
  type: state_machine
  states:
    - planning
    - building
    - verifying
    - human_review  # Human-in-the-loop
    - merging
    - complete
  
  transitions:
    - from: planning
      to: building
      condition: plan_complete
    
    - from: building
      to: verifying
      condition: build_success
      else: planning  # On failure
    
    - from: verifying
      to: human_review
      condition: verified
      else: planning  # On failure
    
    - from: human_review
      to: merging
      condition: approved
      else: planning  # On rejection
```

**DAG Workflows:**
```yaml
# Parallel execution with dependencies
workflow:
  type: dag
  
  nodes:
    - id: lint
      agent: linter
    
    - id: test
      agent: tester
      depends_on: [lint]
    
    - id: security
      agent: security_scanner
      depends_on: [lint]
    
    - id: build
      agent: builder
      depends_on: [test, security]
    
    - id: verify
      agent: verifier
      depends_on: [build]
```

**Saga Pattern:**
```yaml
# Distributed transactions with compensation
workflow:
  type: saga
  
  steps:
    - name: update_database
      action: update_schema
      compensate: rollback_schema
    
    - name: migrate_data
      action: run_migration
      compensate: rollback_data
    
    - name: deploy_api
      action: deploy
      compensate: rollback_deployment
```

### 4. Agent Orchestration

**Multi-Agent Coordination:**
```yaml
agents:
  builder:
    prompt: PROMPT-BUILDER.md
    timeout: 7200
    max_retries: 3
    retry_policy:
      strategy: exponential_backoff
      base_delay: 5s
      max_delay: 300s
    
  verifier:
    prompt: PROMPT-VERIFIER.md
    timeout: 3600
    parallel: true  # Can run in parallel
    
  planner:
    prompt: PROMPT-PLANNER.md
    timeout: 1800
    on_failure: always  # Called on any failure
    
  security_scanner:
    prompt: PROMPT-SECURITY.md
    condition: "file_contains: auth"  # Conditional invocation
```

**Agent Chains:**
```yaml
chains:
  security_pipeline:
    - security_scanner
    - dependency_checker
    - secret_detector
    
  code_quality:
    - linter
    - type_checker
    - coverage_analyzer
```

### 5. Monitoring & Observability

**OpenTelemetry Integration:**
```yaml
observability:
  provider: opentelemetry
  traces: true
  metrics: true
  logs: true
  
  exporters:
    jaeger:
      endpoint: http://localhost:16686
    prometheus:
      port: 9090
    
  dashboard:
    enabled: true
    type: grafana
    url: http://localhost:3000
```

**Metrics Collected:**
- Task duration, success/failure rates
- Agent iteration counts
- Token usage and costs
- Phase timing
- Queue depth
- Circuit breaker state

**Structured Logging:**
```json
{
  "timestamp": "2024-03-08T10:30:15Z",
  "level": "INFO",
  "trace_id": "abc123",
  "span_id": "def456",
  "event": "phase_complete",
  "phase": "build",
  "agent": "builder",
  "duration_ms": 45000,
  "success": true
}
```

### 6. Failure Recovery

**Retry Policies:**
```yaml
retry:
  default:
    strategy: exponential_backoff
    max_attempts: 3
    base_delay: 1s
    max_delay: 60s
    jitter: 0.1
  
  transient_errors:
    strategy: linear
    max_attempts: 5
    delay: 5s
    retry_on:
      - TimeoutError
      - ConnectionError
  
  critical:
    strategy: fixed
    max_attempts: 1  # No retry
```

**Circuit Breaker:**
```yaml
circuit_breaker:
  enabled: true
  failure_threshold: 5
  timeout: 300s
  half_open_max_calls: 3
  
  # Actions on state change
  on_open:
    - notify_team
    - pause_loop
  
  on_close:
    - resume_loop
```

**Compensating Actions:**
```yaml
# For saga workflows
compensation:
  on_failure:
    - action: git_reset
      args:
        hard: false
    
    - action: notify
      args:
        message: "Workflow failed, manual intervention required"
```

## Generator Script

```bash
bash scripts/generate-ralph-loop.sh [options] ./my-loop

Options:
  --template <name>      Workflow template: basic, advanced, dag, saga
  --with-plugins         Include example plugin directory
  --with-dashboard       Include monitoring dashboard config
  --with-tests           Include test suite for the loop

Examples:
  bash scripts/generate-ralph-loop.sh ./basic-loop
  bash scripts/generate-ralph-loop.sh --template dag ./data-pipeline
  bash scripts/generate-ralph-loop.sh --with-plugins --with-dashboard ./enterprise-loop
```

## Configuration

### Basic Configuration (ralph.yaml)
```yaml
# Core settings
loop:
  max_iterations: 100
  auto_commit: true
  parallel_agents: false

# Agent timeouts
timeouts:
  builder: 7200s
  verifier: 3600s
  planner: 1800s

# Simple retry
retry:
  max_attempts: 3
  delay: 5s

# Logging
logging:
  level: INFO
  file: .ralph/logs/ralph.log
```

### Advanced Configuration
```yaml
# Full enterprise configuration
project:
  name: My Enterprise Project
  description: AI-driven development workflow

# Plugin system
plugins:
  directory: ./plugins
  auto_discover: true
  
  registry:
    - name: core
      url: https://github.com/wojons/ralph-plugins
    
    - name: custom
      url: https://github.com/myorg/ralph-plugins
  
  installed:
    - name: slack-notifier
      version: ^1.0.0
      from: core
    
    - name: security-scanner
      version: ^2.1.0
      from: custom

# Workflow definition
workflow:
  type: state_machine
  
  states:
    - id: planning
      on_enter: [log_start]
      on_exit: [log_complete]
    
    - id: building
      timeout: 7200s
      on_timeout: [escalate_to_human]
    
    - id: verifying
      parallel: true
      agents: [verifier, security_scanner, linter]
      require_all: true  # All must pass
    
    - id: human_review
      type: human_in_the_loop
      timeout: 86400s  # 24 hours
      reminder_interval: 3600s
    
    - id: complete
      on_enter: [notify_success]

# Agent orchestration
agents:
  builder:
    prompt: PROMPT-BUILDER.md
    model: claude-3-opus
    temperature: 0.7
    
  verifier:
    prompt: PROMPT-VERIFIER.md
    model: claude-3-sonnet
    temperature: 0.3
    
  security_scanner:
    prompt: PROMPT-SECURITY.md
    model: claude-3-opus
    tools: [security_db, vulnerability_scanner]
    
  human_reviewer:
    type: human
    notification:
      slack: "#code-reviews"
      email: ["lead@company.com"]

# Circuit breaker
circuit_breaker:
  enabled: true
  failure_threshold: 5
  timeout: 300s

# Monitoring
observability:
  provider: opentelemetry
  
  traces:
    enabled: true
    sampling_rate: 1.0
  
  metrics:
    enabled: true
    exporters:
      - type: prometheus
        port: 9090
      
      - type: cloudwatch
        region: us-east-1
  
  logs:
    level: INFO
    format: json
    rotation:
      max_size: 100MB
      max_files: 10
  
  dashboard:
    enabled: true
    type: grafana
    config: ./grafana/dashboard.yaml

# Notifications
notifications:
  channels:
    slack:
      webhook: ${SLACK_WEBHOOK_URL}
      channel: "#builds"
    
    email:
      smtp: ${SMTP_SERVER}
      to: ["team@company.com"]
  
  events:
    on_start:
      - slack
    
    on_failure:
      - slack
      - email
    
    on_complete:
      - slack
    
    on_human_review_needed:
      - slack:
          mention: "@here"
      - email

# State management
state:
  persistence:
    type: database
    url: ${DATABASE_URL}
    
  snapshots:
    enabled: true
    interval: 60s
    retention: 30d
```

## CLI Commands

```bash
# Basic operations
python ralph-loop.py loop              # Run full workflow
python ralph-loop.py loop --commit     # Auto-commit changes
python ralph-loop.py status            # Show current status
python ralph-loop.py logs              # View recent logs
python ralph-loop.py reset             # Reset loop state

# Workflow management
python ralph-loop.py workflow list                    # List available workflows
python ralph-loop.py workflow validate <file>          # Validate workflow YAML
python ralph-loop.py workflow visualize <file>         # Generate workflow diagram
python ralph-loop.py loop --workflow custom.yaml       # Use custom workflow

# Plugin management
python ralph-loop.py plugin list                      # List installed plugins
python ralph-loop.py plugin install <name>           # Install from registry
python ralph-loop.py plugin enable <name>            # Enable plugin
python ralph-loop.py plugin disable <name>            # Disable plugin

# Monitoring
python ralph-loop.py metrics                          # Show current metrics
python ralph-loop.py traces                          # Show recent traces
python ralph-loop.py dashboard                        # Open monitoring dashboard

# Debugging
python ralph-loop.py debug --iteration 5              # Debug specific iteration
python ralph-loop.py replay --from-state <snapshot>   # Replay from state
python ralph-loop.py inspect --phase build            # Inspect phase execution
```

## Project Structure

```
my-project/
├── ralph.yaml                    # Main configuration
├── TODO.md                       # Tasks to complete
├── SPEC.md                       # Project specification
├── AGENTS.md                     # Project conventions
│
├── PROMPT-*.md                   # Agent instructions
│   ├── PROMPT-BUILDER.md
│   ├── PROMPT-VERIFIER.md
│   ├── PROMPT-PLANNER.md
│   └── PROMPT-SECURITY.md       # Custom agent
│
├── workflows/                    # Workflow definitions
│   ├── default.yaml
│   ├── ci.yaml
│   ├── release.yaml
│   └── custom/
│
├── plugins/                      # Custom plugins
│   ├── __init__.py
│   ├── slack.py
│   ├── security.py
│   └── metrics/
│       └── prometheus.py
│
├── .ralph/                       # Loop state
│   ├── loop-state.yaml
│   ├── snapshots/
│   ├── logs/
│   └── cache/
│
└── monitoring/                   # Observability config
    ├── grafana/
    ├── prometheus/
    └── jaeger/
```

## Agent Prompts

The skill includes **specialized PROMPT.md files** at the project root:

### PROMPT-BUILDER.md
Implementation agent with:
- **Mermaid charts**: Build workflow and decision trees
- **Lifecycle phases**: Discovery → Planning → Implementation → Completion
- **Standards**: Code quality, testing requirements
- **Edge cases**: What to do when stuck
- **Plugin hooks**: How to interact with plugins

### PROMPT-VERIFIER.md
Quality assurance agent with:
- **Mermaid charts**: Multi-layer verification flow
- **5 verification layers**: Functional → Code → Spec → Edge Cases → Integration
- **Failure patterns**: Common issues to catch
- **Report formats**: Detailed PASS/FAIL reports

### PROMPT-PLANNER.md
Strategic planning agent with:
- **Mermaid charts**: When planner is called
- **Root cause analysis**: Framework for diagnosis
- **Solution patterns**: Clarify, restructure, fix context, strategic
- **Decision framework**: When to split vs clarify

### Custom Agents

Create custom agents by adding `PROMPT-<NAME>.md`:

```yaml
# ralph.yaml
agents:
  security_scanner:
    prompt: PROMPT-SECURITY.md
    hooks:
      - phase.before_build
      - phase.after_build
```

## Plugin Development

### Plugin Structure
```python
# plugins/my_plugin.py
from ralph.plugins import Plugin, hook

class MyPlugin(Plugin):
    name = "my-plugin"
    version = "1.0.0"
    
    def __init__(self, config):
        self.config = config
    
    @hook("workflow.on_start")
    def on_start(self, context):
        """Called when loop starts"""
        print(f"Starting workflow: {context.workflow_name}")
    
    @hook("phase.after_build")
    def after_build(self, context):
        """Called after build phase"""
        if context.success:
            self.send_notification("Build successful!")
    
    @hook("workflow.on_failure")
    def on_failure(self, context):
        """Called on workflow failure"""
        self.escalate(context.error)
```

### Plugin Configuration
```yaml
# In ralph.yaml
plugins:
  - name: my-plugin
    entry: plugins.my_plugin.MyPlugin
    config:
      api_key: ${API_KEY}
      endpoint: https://api.example.com
```

### Available Context Objects

**Workflow Context:**
```python
{
    "workflow_name": "default",
    "iteration": 5,
    "started_at": "2024-03-08T10:30:15Z",
    "config": {...},  # Full ralph.yaml
}
```

**Phase Context:**
```python
{
    "phase": "build",
    "agent": "builder",
    "iteration": 5,
    "started_at": "2024-03-08T10:30:15Z",
    "duration_ms": 45000,
    "success": True,
    "output": "...",
    "metrics": {
        "tokens_used": 15000,
        "cost": 0.45
    }
}
```

**State Context:**
```python
{
    "from_state": "planning",
    "to_state": "building",
    "trigger": "plan_complete",
    "timestamp": "2024-03-08T10:30:15Z"
}
```

## Monitoring Dashboard

The skill provides a built-in monitoring dashboard:

```bash
# Start dashboard
python ralph-loop.py dashboard

# Open in browser
open http://localhost:8080
```

**Dashboard Views:**
- **Overview**: Current status, recent iterations, success rate
- **Timeline**: Phase execution timeline with traces
- **Metrics**: Token usage, costs, duration trends
- **Logs**: Structured logs with filtering
- **Agents**: Agent performance and health
- **Plugins**: Plugin status and metrics

## Advanced Features

### Human-in-the-Loop

```yaml
workflow:
  states:
    - id: human_review
      type: human
      
      notification:
        slack: "#reviews"
        email: ["reviewer@company.com"]
        mention: "@here"
      
      ui:
        type: web
        template: review_form.html
      
      timeout: 86400s
      reminder_interval: 3600s
      
      on_timeout:
        action: auto_approve
        notify: true
```

### Conditional Execution

```yaml
agents:
  security_scanner:
    condition: "file_changed: '*.py' and not file_changed: 'test_*'"
  
  performance_test:
    condition: "branch == 'main' and tag =~ 'v.*'"
```

### Parallel Execution

```yaml
workflow:
  type: dag
  
  nodes:
    - id: lint
      agent: linter
    
    - id: unit_tests
      agent: tester
      depends_on: [lint]
    
    - id: integration_tests
      agent: integration_tester
      depends_on: [lint]
    
    - id: security_scan
      agent: security_scanner
      depends_on: [lint]
    
    - id: build
      agent: builder
      depends_on: [unit_tests, integration_tests, security_scan]
```

### State Snapshots

```yaml
state:
  snapshots:
    enabled: true
    
    triggers:
      - phase_complete
      - iteration_complete
      - before_human_review
    
    retention:
      count: 100
      age: 30d
```

## Examples

### CI/CD Pipeline
```yaml
# .github/workflows/ralph.yaml
name: AI-Driven CI

on: [push, pull_request]

jobs:
  ralph:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Ralph Loop
        run: |
          pip install ralph-loop
          ralph-loop loop --workflow ci.yaml
```

### Custom Workflow
```yaml
# workflows/security-first.yaml
workflow:
  type: state_machine
  
  states:
    - security_scan
    - planning
    - building
    - verifying
    - complete
  
  transitions:
    - from: security_scan
      to: planning
      condition: security_passed
      else: stop
    
    - from: building
      to: verifying
      condition: build_success
    
    - from: verifying
      to: complete
      condition: verified
      else: building
```

## Notes

- **Reliability**: Durable execution with state persistence
- **Extensibility**: Plugin system without core modification
- **Observability**: OpenTelemetry standard for vendor flexibility
- **Failure Handling**: Classify errors, exponential backoff, circuit breakers
- **State Management**: Explicit state machines with persistence
- **Extensibility**: Clear extension points via plugins

## Resources

- **Documentation**: https://github.com/wojons/skills/tree/main/skills/ralph-wiggum-loop
- **Plugin Registry**: https://github.com/wojons/ralph-plugins
- **Examples**: https://github.com/wojons/ralph-examples
- **Community**: https://github.com/wojons/skills/discussions
