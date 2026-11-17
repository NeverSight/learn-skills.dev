---
name: enterprise-agent-ops
description: Operate long-lived agent workloads with observability, security boundaries, and lifecycle management.
origin: ECC
---

# Enterprise Agent Ops

Operational controls for cloud-hosted or continuously-running agent systems that
need more than a single CLI session: observability, guardrails, audit, and
lifecycle management.

## Observability: What to Log Per Agent Run

Emit one structured event per run (and per tool call) with at least:

```json
{
  "run_id": "uuid",            "parent_run_id": "uuid|null",
  "agent": "name", "version": "git-sha",
  "started_at": "iso8601", "ended_at": "iso8601", "duration_ms": 1234,
  "status": "success|failed|timeout|killed",
  "model": "model-id", "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0,
  "tool_calls": 0, "retries": 0,
  "error_class": "none|rate_limit|tool_error|guardrail|timeout",
  "input_hash": "sha256",      // hash, not raw input (PII)
  "guardrail_blocks": []
}
```

- **Trace** the full tool-call chain (one span per model call and per tool call)
  so you can replay any run — wire OpenTelemetry to your collector.
- **Log hashes/IDs, not raw payloads** when input may contain secrets or PII.
- Alert on: failure-rate spike, cost-per-run spike, retry surge, latency p95
  breach, guardrail-block surge.

## Guardrail / Kill-Switch Pattern

Wrap every agent action behind a pre-flight check plus a global kill switch:

```python
def guarded_action(action, ctx):
    if read_flag("agent.kill_switch"):        # 1. global stop (config/Redis flag)
        raise Halted("kill switch active")
    if action.cost_estimate > ctx.budget_remaining:   # 2. budget cap
        raise Halted("budget exceeded")
    if not action.scope_allowed(ctx.allowed_scopes):  # 3. least-privilege scope
        raise Halted(f"scope {action.scope} not permitted")
    if action.is_destructive and not ctx.approved:    # 4. human-in-loop gate
        return request_approval(action)
    audit_log(action, ctx)                            # 5. record before executing
    return action.run()
```

- Kill switch is a single flag checked every iteration — flip it to halt the
  fleet without redeploying.
- Per-run budget (tokens/$/wall-clock) and a hard max-iteration cap prevent
  runaway loops.
- Destructive actions (deletes, payments, prod writes) require explicit approval
  or a dry-run-by-default mode.

## Audit-Log Schema

Append-only, tamper-evident, for every high-risk action:

```
ts | run_id | agent | actor(human/agent) | action | resource | params_hash
   | decision(allow/deny/approve) | approver | outcome | prev_hash
```

`prev_hash` chains entries (each row hashes the previous) so tampering is
detectable. Retain per compliance requirement; never store raw secrets/PII —
store hashes and references.

## Lifecycle Checklist

**Deploy** — [ ] immutable artifact (pinned image/sha) · [ ] least-privilege
creds, secrets injected from a manager (never baked in) · [ ] timeout + retry
budgets set · [ ] kill switch wired and tested · [ ] canary on a small traffic
slice before full rollout.

**Monitor** — [ ] dashboards for success rate, cost/run, retries, latency,
failure-class mix · [ ] alerts on each metric · [ ] periodic sample-replay of
real runs to catch silent quality drift.

**Retire** — [ ] drain in-flight runs before stop · [ ] revoke credentials and
scopes · [ ] archive audit logs per retention policy · [ ] remove flags/secrets
and document the decommission.

## Incident Response (failure spike)

1. Flip kill switch / freeze rollout. 2. Capture representative failing traces.
3. Isolate the failing route or tool. 4. Patch with the smallest safe change.
5. Run regression + security checks. 6. Resume via canary, then ramp.

## Pairs With

PM2 / systemd / container orchestrators (runtime) · CI/CD gates (rollout) ·
`agentic-engineering` (eval-first workflow) · `cost-aware-llm-pipeline` (budgets).
