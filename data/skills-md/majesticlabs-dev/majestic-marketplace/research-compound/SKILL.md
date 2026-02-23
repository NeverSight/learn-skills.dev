---
name: research-compound
description: Automatically check and update folder-specific AGENTS.md during research. Before investigating a domain, read nearest AGENTS.md for existing context. After discovering valuable patterns, append learnings to that file.
allowed-tools: Read Edit Glob
---

# Research Compound

Compound learnings into folder-specific AGENTS.md files during research work.

## Trigger Conditions

Activate this behavior when:
- Investigating a specific domain (jobs, models, services, controllers, etc.)
- Using research agents (repo-analyst, docs-researcher, etc.)
- Reading multiple files in the same folder hierarchy
- User asks to "understand", "investigate", or "research" a subsystem

## Pre-Research: Check Existing Context

**Before diving into code**, find and read the nearest AGENTS.md:

```bash
# From target folder, traverse up to find nearest AGENTS.md
# Example: researching app/jobs/cash_app/
# Check: app/jobs/cash_app/AGENTS.md
#        app/jobs/AGENTS.md
#        app/AGENTS.md
#        AGENTS.md (root)
```

### What to Extract

From existing AGENTS.md, note:
- Known patterns and conventions
- Documented gotchas
- File organization rules
- Testing approaches
- Previous learnings (avoid re-discovering)

### Pre-Research Output

Briefly acknowledge:
```
Found existing context in app/jobs/AGENTS.md:
- Jobs use Sidekiq with retry configuration
- Naming: *Job suffix required
- Testing: Use perform_inline in specs
```

## Post-Research: Evaluate Learnings

After research, evaluate each discovery:

### Worth Recording (YES)

| Criteria | Example |
|----------|---------|
| Applies to multiple files in domain | "All jobs inherit from ApplicationJob" |
| Non-obvious convention | "Jobs must call `super` before custom logic" |
| Gotcha that caused confusion | "CashApp jobs require merchant_id, not user_id" |
| Integration pattern | "Jobs trigger webhooks via WebhookService" |
| Testing insight | "Use `freeze_time` for scheduled job specs" |

### Skip Recording (NO)

| Criteria | Example |
|----------|---------|
| One-off implementation detail | "ProcessPaymentJob has 3 retries" |
| Already documented | Pattern exists in AGENTS.md |
| Too specific to single file | "Line 42 has a TODO" |
| Obvious from code | "Job processes payments" |

## Update Protocol

### Step 1: Locate Target AGENTS.md

Use **nearest-wins** hierarchy:
1. If `{domain}/AGENTS.md` exists → update it
2. If not, check parent folder
3. If no AGENTS.md in hierarchy → create at domain level

```bash
# Find existing AGENTS.md files
find . -name "AGENTS.md" -type f | head -20
```

### Step 2: Determine Section

Map learning type to section:

| Learning Type | Target Section |
|---------------|----------------|
| Pattern/Convention | `## Patterns` or `## Conventions` |
| Gotcha/Warning | `## Gotchas` or `## Common Issues` |
| File organization | `## Structure` |
| Testing approach | `## Testing` |
| Integration point | `## Integration` or `## Dependencies` |

If section doesn't exist, create it.

### Step 3: Format the Learning

```markdown
- **[Short title]**: [Concrete description]
  - Example: `path/to/example.rb:42`
```

Keep entries:
- Single bullet point (1-2 lines)
- Concrete, not vague
- With file reference when applicable

### Step 4: Append (Don't Replace)

Use Edit tool to append to appropriate section:

```markdown
## Gotchas

- **Existing gotcha**: Description
- **NEW: Merchant ID required**: CashApp jobs use `merchant_id`, not `user_id`
  - Example: `app/jobs/cash_app/process_payment_job.rb:15`
```

## Creating New AGENTS.md

If no AGENTS.md exists in the domain hierarchy, create one:

```markdown
# {Domain Name}

## Purpose

{One-line description of this domain}

## Patterns

- **Pattern name**: Description
  - Example: `path/to/file.rb`

## Gotchas

- **Gotcha name**: Description

## Testing

- **Testing approach**: Description
```

### Placement Rules

| Domain Depth | Create At |
|--------------|-----------|
| `app/jobs/` | `app/jobs/AGENTS.md` |
| `app/jobs/cash_app/` | `app/jobs/cash_app/AGENTS.md` (if 3+ files) |
| `app/services/payments/` | `app/services/payments/AGENTS.md` |

Only create subfolder AGENTS.md if:
- 3+ files in that specific folder
- Distinct patterns from parent domain
- Significant complexity warranting isolation

## Examples

### Example 1: Pre-Research Check

```
User: "Investigate how background jobs work in this app"

Claude:
1. Target domain: app/jobs/
2. Check for AGENTS.md...
   - Found: app/jobs/AGENTS.md
3. Read existing context:
   "Jobs use Sidekiq, ApplicationJob base class, *Job suffix"
4. Proceed with research, avoiding re-discovery of known patterns
```

### Example 2: Post-Research Update

```
After researching app/jobs/cash_app/:

Discovered:
- CashApp jobs require merchant_id (not user_id) ← WORTH RECORDING
- ProcessPaymentJob has 3 retries ← SKIP (too specific)
- All CashApp jobs log to separate channel ← WORTH RECORDING

Update app/jobs/cash_app/AGENTS.md:
## Gotchas
+ - **Merchant ID required**: Use `merchant_id`, not `user_id` for CashApp jobs
+   - Example: `app/jobs/cash_app/process_payment_job.rb:15`

## Patterns
+ - **Separate logging**: CashApp jobs use `CashAppLogger` channel
+   - Example: `app/jobs/cash_app/base_job.rb:8`
```

### Example 3: Creating New AGENTS.md

```
Researching app/services/webhooks/ (no existing AGENTS.md)

After research, create app/services/webhooks/AGENTS.md:

# Webhooks

## Purpose

Outbound webhook delivery and retry management.

## Patterns

- **Delivery service**: All webhooks go through `WebhookDeliveryService`
  - Example: `app/services/webhooks/delivery_service.rb`
- **Payload builders**: Each event type has a `*PayloadBuilder`
  - Example: `app/services/webhooks/payment_payload_builder.rb`

## Gotchas

- **Idempotency required**: Webhooks may retry; receivers must handle duplicates
- **Timeout**: 30-second timeout on delivery attempts
```

## Quality Checks

Before updating AGENTS.md, verify:

- [ ] Learning is generalizable (applies beyond single file)
- [ ] Not already documented
- [ ] Concrete enough to act on
- [ ] Has file reference for examples
- [ ] Matches existing AGENTS.md style/structure

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Dump all findings into AGENTS.md | Filter for generalizable patterns only |
| Create AGENTS.md for every folder | Only domains with distinct patterns |
| Write paragraphs | Single bullet points with examples |
| Duplicate root-level guidance | Only domain-specific additions |
| Update on every file read | Batch updates at research completion |
