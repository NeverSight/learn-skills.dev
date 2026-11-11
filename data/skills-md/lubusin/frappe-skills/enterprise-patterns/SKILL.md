---
name: enterprise-patterns
description: Production-grade architectural patterns for building enterprise Frappe apps like CRM, Helpdesk, and HRMS. Use when designing complex multi-entity systems with workflows, SLAs, and integrations.
---

# Frappe Enterprise Patterns

Architectural patterns for building production-grade enterprise applications.

## When to use

- Building CRM, Helpdesk, HRMS, or similar multi-entity systems
- Designing SLA-driven workflows
- Implementing assignment and queue management
- Building audit trails and activity logs
- Integrating with external systems (email, telephony, CRM)

## Inputs required

- System type (CRM/Helpdesk/custom)
- Core entities and relationships
- SLA requirements
- Workflow states and transitions
- Integration points

## Procedure

### 0) Design data model

Start with clear, normalized DocTypes:

```
Ticket (parent)
├── customer (Link: Customer)
├── assigned_to (Link: User)
├── status (Select: Open, In Progress, Resolved, Closed)
├── priority (Link: Priority)
├── sla (Link: SLA)
├── activities (Table: Ticket Activity)
└── response_by, resolution_by (Datetime)
```

**Key patterns:**
- Use Link fields for relationships
- Use child tables for activities, timelines, line items
- Use Dynamic Link when target DocType varies

### 1) Implement state machine

**Option A: Workflow DocType**
- Create Workflow with states and role-based transitions
- Link to your DocType

**Option B: docstatus for submission flow**
| docstatus | Meaning |
|-----------|---------|
| 0 | Draft |
| 1 | Submitted |
| 2 | Cancelled |

**Option C: Custom status field with validation**
```python
def validate(self):
    allowed = self.get_allowed_transitions()
    if self.status not in allowed:
        frappe.throw(f"Cannot transition to {self.status}")
```

### 2) Set up permissions

**Row-level filtering:**
- Use User Permissions to restrict by entity
- Combine with Role Permissions

**Always re-check in RPC methods:**
```python
@frappe.whitelist()
def update_ticket(name, status):
    doc = frappe.get_doc("Ticket", name)
    if not frappe.has_permission("Ticket", "write", doc):
        frappe.throw("Not permitted", frappe.PermissionError)
    doc.status = status
    doc.save()
```

### 3) Build activity trail

Track changes using Activity Log or custom child table:

```python
def on_update(self):
    if self.has_value_changed("status"):
        self.append("activities", {
            "action": "Status Change",
            "old_value": self._doc_before_save.status,
            "new_value": self.status,
            "timestamp": frappe.utils.now()
        })
```

### 4) Implement SLA

**SLA DocType:**
```
SLA
├── entity_type (Link: DocType)
├── response_time (Duration)
├── resolution_time (Duration)
└── escalation_rules (Table: Escalation Rule)
```

**Apply SLA on creation:**
```python
def after_insert(self):
    sla = get_applicable_sla(self)
    if sla:
        self.response_by = add_to_date(self.creation, hours=sla.response_time)
        self.resolution_by = add_to_date(self.creation, hours=sla.resolution_time)
        self.db_update()
```

**Monitor breaches (scheduled job):**
```python
def check_sla_breaches():
    tickets = frappe.get_all("Ticket", 
        filters={"status": ["not in", ["Resolved", "Closed"]]},
        fields=["name", "resolution_by"]
    )
    for t in tickets:
        if frappe.utils.now_datetime() > t.resolution_by:
            mark_sla_breached(t.name)
```

### 5) Assignment and queues

**Round-robin assignment:**
```python
def assign_next_agent(queue):
    agents = frappe.get_all("Queue Member",
        filters={"queue": queue, "available": 1},
        fields=["user", "current_load"],
        order_by="current_load asc"
    )
    if agents:
        return agents[0].user
    return None
```

**Assignment Rules DocType** for automatic assignment.

### 6) Notifications and escalations

**Configure Notification DocType for:**
- SLA approaching breach
- Assignment changes
- Status transitions
- Customer replies

**Escalation chain:**
```
Level 1 (0h): Notify assigned agent
Level 2 (4h): Notify team lead
Level 3 (8h): Notify manager
Level 4 (24h): Notify department head
```

### 7) External integrations

**Centralize in `integrations/` module:**
```python
# my_app/integrations/email_connector.py
def sync_emails():
    # Fetch from Email Account
    # Create Communications
    # Link to Tickets
```

**Use background jobs for sync:**
```python
frappe.enqueue(
    "my_app.integrations.email_connector.sync_emails",
    queue="long",
    timeout=600
)
```

## Verification

- [ ] Workflow transitions work for all roles
- [ ] Permissions enforced at API level
- [ ] Activity log captures all changes
- [ ] SLA calculation correct
- [ ] Notifications fire appropriately
- [ ] Integration sync runs without errors

## Failure modes / debugging

- **Permission bypass**: Check RPC methods have explicit permission checks
- **SLA not applying**: Verify scheduled job is running
- **Activities not logging**: Check `has_value_changed` usage
- **Notifications not sending**: Check Notification rules and email queue

## Escalation

- For complex permission patterns, see [references/advanced-permissions.md](references/advanced-permissions.md)
- For queue optimization, see [references/queue-patterns.md](references/queue-patterns.md)
- For UI/UX patterns → `ui-patterns`

## References

- [references/workflow-patterns.md](references/workflow-patterns.md) - State machine design
- [references/sla-implementation.md](references/sla-implementation.md) - SLA details
- [references/integration-patterns.md](references/integration-patterns.md) - External systems

## Guardrails

- **Follow CRM/Helpdesk UI patterns**: For CRUD apps, follow `ui-patterns` skill which documents app shell, navigation, list views, and form patterns from official Frappe apps. This includes sidebar layouts, quick filters, Kanban views, and detail panels.
- **Use Frappe UI for frontends**: All custom enterprise frontends must use Frappe UI (Vue 3 + TailwindCSS) — never vanilla JS or jQuery
- **Design workflows carefully**: Map all states and transitions before implementation; consider rollback paths
- **Handle edge cases**: Plan for cancelled, on-hold, and exception states in workflows
- **Test performance early**: Run load tests for high-volume DocTypes and complex queries
- **Use background jobs for heavy operations**: Never block web requests with long-running tasks
- **Log critical operations**: Use `frappe.log_error()` and activity logs for auditability

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Over-complex workflows | Hard to maintain, user confusion | Keep workflows linear when possible; split complex flows |
| Missing error handling in integrations | Silent failures, data inconsistency | Wrap external calls in try/except; log errors; retry logic |
| Race conditions in document updates | Data corruption | Use `frappe.db.get_value(..., for_update=True)` for locks |
| SLA without timezone handling | Wrong calculations for global users | Store and compare in UTC; use `frappe.utils.convert_utc_to_timezone` |
| Not using queues for bulk operations | Timeouts, memory issues | Use `frappe.enqueue()` for operations on many records |
| Hardcoded role names | Breaks on role changes | Use constants or settings for role names |
| Custom UI patterns | Inconsistent UX, user confusion | Study and follow CRM/Helpdesk app shells |
| Using vanilla JS/jQuery for frontend | Maintenance burden, ecosystem mismatch | Always use Frappe UI with Vue 3 |
