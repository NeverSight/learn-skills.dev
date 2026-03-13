---
name: agent-e2e
description: Discover, record, and execute E2E test cases using browser exploration. Use when exploring test scenarios, recording user flows, organizing test structure, or executing YAML-based tests.
---

# E2E Test Discovery & Execution

You're here to discover E2E test scenarios, record them as YAML, or execute existing test cases.

## Core Principle: Semantic Selectors

**The problem**: Traditional selectors (testId, CSS classes) break when UI changes.

**The solution**: Use **semantic selectors** based on accessibility properties. These match what users see.

```yaml
# ❌ Fragile
{{dataTestId: "submit-btn"}}

# ✅ Stable
{{role: button, name: "Submit"}}
```

---

## Phase 1: Discovering Test Scenarios

Don't mechanically scan code/docs/UI. Use **risk-driven discovery**.

### High-Risk Indicators

When exploring a project, prioritize areas with these characteristics:

| Indicator                     | Why It's Risky                | Example                   |
| ----------------------------- | ----------------------------- | ------------------------- |
| **Multi-field forms**         | Validation, edge cases, state | Registration, checkout    |
| **Multi-step flows**          | State carries across steps    | Wizards, onboarding       |
| **Authentication boundaries** | Permissions, sessions         | Login, role-based access  |
| **External integrations**     | Dependencies can fail         | Payment, third-party APIs |
| **Data mutation**             | Side effects matter           | Create, update, delete    |

### Discovery Strategy

1. **Start from risk**, not from code structure
2. **Use multiple sources** (code, docs, browser) to verify each risk
3. **Stop when confident**, not when sources are exhausted

Ask yourself: "What would break that users would notice?" Start there.

---

## Phase 2: Recording Test Cases

### The Snapshot-Refs Pattern

```bash
# 1. Open page
agent-browser open http://localhost:3000 --headed

# 2. Snapshot to discover elements
agent-browser snapshot --json
# Returns: {"refs": {"e1": {"name": "Email", "role": "textbox"}, ...}}

# 3. Interact using refs
agent-browser fill @e1 "test@example.com"
agent-browser click @e2

# 4. Re-snapshot after DOM changes (refs get reassigned!)
agent-browser snapshot --json
```

**Critical**: Always re-snapshot after any action that changes DOM. Refs are temporary.

### Recording as YAML

Store **semantic selectors**, not refs:

```yaml
steps:
  - desc: Submit login form
    commands:
      - agent-browser fill {{role: textbox, name: "Email"}} "{{env.EMAIL}}"
      - agent-browser click {{role: button, name: "Sign In"}}
    expect:
      - url_contains: /dashboard
```

---

## Phase 3: Organizing Test Cases

Use **complexity gradient** to enable fast root-cause analysis:

```
foundations/     →     flows/          →     compositions/
(atomic ops)           (journeys)            (multi-session)

login.yaml            checkout.yaml          two-user-chat.yaml
logout.yaml           onboarding.yaml        order-and-fulfill.yaml
navigate.yaml         password-reset.yaml
```

### Why This Structure

When a composition fails:

1. Check which flow failed
2. Check which foundation in that flow failed
3. Fix the foundation → everything above it recovers

**Foundations** = building blocks (high reuse, must be stable)
**Flows** = complete user journeys (compose foundations)
**Compositions** = multi-session/multi-user scenarios (compose flows)

### Deciding the Category

Ask: "Can this be broken into smaller independent tests?"

- **Yes** → It's a flow or composition
- **No** → It's a foundation

---

## Phase 4: Executing Test Cases

### Intent-Driven Execution

YAML describes **intent + constraints**. You (the agent) fill in **execution details**.

```yaml
# YAML says WHAT and WHEN
- desc: Close popup if it appears
  commands:
    - agent-browser click {{role: button, name: "Close"}}
  optional: true  # Constraint: this can fail

# You decide HOW
# 1. Snapshot to check if button exists
# 2. If exists → click
# 3. If not → skip (because optional: true)
# 4. Record your decision for debugging
```

### Execution Rules

1. **For each step**: snapshot → match selector → execute → verify expect
2. **For optional steps**: skip if element not found, but record the decision
3. **For failures**: report which selector didn't match and what was found instead
4. **Always**: close browser when done

### Handling Complex Scenarios

**Conditional steps** (optional: true):

```yaml
- desc: Dismiss cookie banner
  commands:
    - agent-browser click {{role: button, name: /Accept|Close|×/}}
  optional: true
```

You try the selector. If not found, skip and continue.

**Data extraction**:

```yaml
- desc: Capture order ID from page
  extract:
    from: {{role: heading, name: /Order #\d+/}}
    pattern: "Order #(\\d+)"
    save_as: order_id
```

You find the element, extract the value, save it for later steps.

**Multi-session** (compositions):

```yaml
sessions:
  - name: alice
    lifecycle: persistent
  - name: bob
    lifecycle: persistent

steps:
  - desc: Alice sends message
    session: alice
    commands: [...]

  - desc: Verify Bob received it
    session: bob
    expect:
      - element_visible: { { role: paragraph, name: /Hello/ } }
```

You manage separate browser sessions and switch between them.

---

## YAML Format Reference

Minimal structure:

```yaml
id: case-name
title: Human-readable title
category: foundation # foundation | flow | composition

description: |
  What this tests and why it matters.

parameters:
  base_url: http://localhost:3000

steps:
  - desc: Step description
    commands:
      - agent-browser <action> {{selector}} [args]
    expect:
      - condition: value
    optional: false # default

exploration:
  status: validated # draft | explored | validated
```

See [FORMATS.md](FORMATS.md) for complete specification.

---

## Common Issues

**Empty snapshot**: Page hasn't loaded or lacks accessibility. Wait longer or check framework.

**Refs changed**: Expected. Always re-snapshot before interacting.

**Multiple matches**: Use index: `{{role: button, name: "Delete", index: 0}}`

**Static routing**: `/docs` may need `/docs.html`. Note in your test case.

**Rate limiting (429)**: Public sites limit unauthenticated requests. Consider:

- Adding delays between steps (`agent-browser wait 2000`)
- Using authenticated sessions when available
- Recording on local dev instances when possible

---

## Checklist

When discovering:

- [ ] Identified high-risk areas (forms, multi-step, auth, integrations)
- [ ] Verified risks from multiple sources
- [ ] Prioritized by user impact

When recording:

- [ ] Used semantic selectors, not refs
- [ ] Re-snapshot after DOM changes
- [ ] Added expect conditions for verification

When organizing:

- [ ] Categorized by complexity (foundation/flow/composition)
- [ ] Foundations are atomic and reusable
- [ ] Compositions reference flows, flows reference foundations

When executing:

- [ ] Followed intent, applied judgment for details
- [ ] Recorded decisions for debugging
- [ ] Closed all browser sessions
